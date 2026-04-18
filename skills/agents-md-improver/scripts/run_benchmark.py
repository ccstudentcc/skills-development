#!/usr/bin/env python3
"""Run a safe-first comparative benchmark workflow for the agents-md-improver skill.

Default behavior is `prepare`, which only:
- copies fixture trees into isolated run directories,
- materializes prompts and run metadata,
- prepares optional local skill context for `with_skill`,
- writes instructions for later execution.

Execution is separated from preparation:
- `prepare`: no nested executor runs
- `safe-run`: attempts sandboxed `codex exec` runs
- `grade-benchmark`: grade completed runs, aggregate results, generate review HTML
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = REPO_ROOT / "skills" / "agents-md-improver"
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"
DEFAULT_WORKSPACE_ROOT = REPO_ROOT / "tmp" / "agents-md-improver-workspace"
ITERATION_METADATA_NAME = "iteration_metadata.json"
EVAL_SET_PRESETS: dict[str, set[int]] = {
    "informative": {2, 5, 6, 9, 10, 11, 12},
    "executor-health": {8},
    "low-discrimination": {1, 3, 4, 7, 8},
}


@dataclass
class EvalCase:
    eval_id: int
    eval_name: str
    prompt: str
    expected_output: str
    files: list[str]
    expectations: list[str]
    fixture_root: Path


@dataclass
class RunSnapshot:
    eval_id: int
    eval_name: str
    configuration: str
    run_dir: Path
    status: str
    final_response_exists: bool
    grading_exists: bool


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def ps_quote(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def contains_any(text: str, needles: list[str]) -> bool:
    haystack = normalize_text(text)
    return any(normalize_text(needle) in haystack for needle in needles)


def contains_all(text: str, needles: list[str]) -> bool:
    haystack = normalize_text(text)
    return all(normalize_text(needle) in haystack for needle in needles)


def summarize_expectations(expectations: list[dict[str, object]]) -> dict[str, object]:
    passed = sum(1 for exp in expectations if exp["passed"])
    total = len(expectations)
    failed = total - passed
    return {
        "passed": passed,
        "failed": failed,
        "total": total,
        "pass_rate": round((passed / total) if total else 0.0, 4),
    }


def calculate_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    count = len(values)
    mean = sum(values) / count
    if count > 1:
        variance = sum((value - mean) ** 2 for value in values) / (count - 1)
        stddev = variance**0.5
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def find_skill_creator_dir(explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))

    env_path = os.environ.get("SKILL_CREATOR_DIR")
    if env_path:
        candidates.append(Path(env_path))

    home = Path.home()
    candidates.extend(
        [
            home / ".cc-switch" / "skills" / "skill-creator",
            home / ".codex" / "skills" / ".system" / "skill-creator",
        ]
    )

    for candidate in candidates:
        if (candidate / "scripts" / "aggregate_benchmark.py").exists():
            return candidate.resolve()

    searched = "\n".join(str(path) for path in candidates)
    raise FileNotFoundError(
        "Could not locate skill-creator. Pass --skill-creator-dir or set SKILL_CREATOR_DIR.\n"
        f"Searched:\n{searched}"
    )


def load_evals(selected_ids: set[int] | None) -> list[EvalCase]:
    data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
    cases: list[EvalCase] = []

    for item in data["evals"]:
        eval_id = int(item["id"])
        if selected_ids and eval_id not in selected_ids:
            continue

        rel_paths = [Path(rel_path) for rel_path in item["files"]]
        common_root = Path(os.path.commonpath([str(path.parent) for path in rel_paths]))
        cases.append(
            EvalCase(
                eval_id=eval_id,
                eval_name=slugify_eval_name(common_root.name),
                prompt=item["prompt"],
                expected_output=item["expected_output"],
                files=item["files"],
                expectations=item["expectations"],
                fixture_root=SKILL_ROOT / common_root,
            )
        )

    return sorted(cases, key=lambda case: case.eval_id)


def default_eval_set_for_mode(mode: str) -> str | None:
    if mode in {"prepare", "safe-run"}:
        return "informative"
    return None


def resolve_requested_eval_ids(eval_ids: list[int] | None, eval_set: str | None, mode: str) -> tuple[set[int] | None, str]:
    if eval_ids:
        return set(eval_ids), "explicit_ids"
    if eval_set == "all":
        return None, "all"
    if eval_set:
        return set(EVAL_SET_PRESETS[eval_set]), eval_set

    default_eval_set = default_eval_set_for_mode(mode)
    if default_eval_set:
        return set(EVAL_SET_PRESETS[default_eval_set]), default_eval_set
    return None, "all"


def load_iteration_metadata(iteration_dir: Path) -> dict[str, object]:
    metadata_path = iteration_dir / ITERATION_METADATA_NAME
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def infer_iteration_eval_ids(iteration_dir: Path) -> set[int] | None:
    eval_ids: set[int] = set()
    for eval_dir in iteration_dir.glob("eval-*"):
        if not eval_dir.is_dir():
            continue
        match = re.match(r"eval-(\d+)-", eval_dir.name)
        if match:
            eval_ids.add(int(match.group(1)))
    return eval_ids or None


def resolve_existing_iteration_eval_ids(iteration_dir: Path, eval_ids: list[int] | None, eval_set: str | None) -> tuple[set[int] | None, str]:
    if eval_ids or eval_set:
        return resolve_requested_eval_ids(eval_ids, eval_set, mode="status")

    metadata = load_iteration_metadata(iteration_dir)
    stored_eval_ids = metadata.get("eval_ids")
    if isinstance(stored_eval_ids, list) and stored_eval_ids:
        return {int(item) for item in stored_eval_ids}, str(metadata.get("eval_selection", "stored_iteration_selection"))

    inferred = infer_iteration_eval_ids(iteration_dir)
    if inferred:
        return inferred, "inferred_from_iteration_dirs"
    return None, "all"


def benchmark_style_for_eval_selection(eval_selection: str) -> str:
    if eval_selection == "executor-health":
        return "executor-health-smoke"
    if eval_selection == "low-discrimination":
        return "diagnostic-comparative"
    return "production-like-comparative"


def slugify_eval_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def strip_skill_invocation(prompt: str) -> str:
    updated = prompt
    updated = updated.replace("Use $agents-md-improver to ", "")
    updated = updated.replace("Use $agents-md-improver ", "")
    updated = updated.replace("使用 $agents-md-improver ", "")
    updated = updated.replace("$agents-md-improver", "the current instructions")
    return updated


def normalize_prompt_for_run(prompt: str, eval_name: str, use_skill: bool) -> str:
    fixture_path = f"evals/files/{eval_name}/"
    normalized = prompt.replace(fixture_path, "outputs/")
    normalized = normalized.replace(fixture_path.rstrip("/"), "outputs")
    if not use_skill:
        normalized = strip_skill_invocation(normalized)
    return normalized


def build_executor_prompt(case: EvalCase, use_skill: bool) -> str:
    requested_prompt = normalize_prompt_for_run(case.prompt, case.eval_name, use_skill=False)
    if use_skill:
        opener = (
            "Before editing anything, read `skills/agents-md-improver/SKILL.md` and any referenced files under "
            "`skills/agents-md-improver/references/` that you need, then follow that guidance for this task."
        )
        read_scope = (
            "- You may read files under `outputs/` and `skills/agents-md-improver/`.\n"
            "- If you need shell for local inspection, use it only for read-only file inspection inside those paths.\n"
        )
    else:
        opener = "Handle this task without loading any external AGENTS-improver skill instructions."
        read_scope = (
            "- You may read files under `outputs/`.\n"
            "- If you need shell for local inspection, use it only for read-only file inspection inside `outputs/`.\n"
        )
    return (
        f"{opener}\n\n"
        "Execution constraints:\n"
        "- Work only inside `outputs/`.\n"
        f"{read_scope}"
        "- Modify files only under `outputs/`.\n"
        "- Do not create or edit files outside `outputs/`.\n"
        "- Do not rely on global memories, plugins, or any context outside this prepared run directory.\n"
        "- Never use shell commands to modify files; use the normal file-editing path for any edits.\n"
        "- Make the smallest correct change for the request.\n"
        "- If the right destination is `README.md`, `ARCHITECTURE.md`, or a task doc inside `outputs/`, update that file instead of forcing `AGENTS.md`.\n"
        "- Finish with a short explanation of what changed and why.\n\n"
        f"Task:\n{requested_prompt}\n"
    )


def copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, dirs_exist_ok=True)


def prepare_run_dir(case: EvalCase, run_dir: Path, use_skill: bool) -> None:
    outputs_dir = run_dir / "outputs"
    copy_tree(case.fixture_root, outputs_dir)
    if use_skill:
        copy_tree(SKILL_ROOT, run_dir / "skills" / "agents-md-improver")


def write_final_response_template(run_dir: Path, case: EvalCase) -> None:
    template = [
        "# Final Response Template",
        "",
        "Use this file only as a reminder for the shape of `final_response.md`.",
        "Delete or ignore it after the real run completes.",
        "",
        "Suggested structure:",
        "",
        "- What changed",
        "- Why this layer or destination was chosen",
        "- What was intentionally left unchanged",
        "",
        "Eval goal:",
        f"- {case.expected_output}",
        "",
    ]
    (run_dir / "FINAL_RESPONSE_TEMPLATE.md").write_text("\n".join(template), encoding="utf-8")


def build_safe_exec_command(run_dir: Path, model: str | None) -> str:
    prompt_path = run_dir / "prompt.md"
    final_response_path = run_dir / "final_response.md"
    command = (
        f"Get-Content -Raw -LiteralPath {ps_quote(str(prompt_path))} | "
        f"codex --disable memories --disable plugins --disable shell_snapshot "
        f"-a never exec --skip-git-repo-check --sandbox workspace-write "
        f"--ephemeral --color never --json "
        f"-C {ps_quote(str(run_dir))} -o {ps_quote(str(final_response_path))} -"
    )
    if model:
        command += f" --model {ps_quote(model)}"
    return command


def write_run_instructions(run_dir: Path, use_skill: bool, model: str | None) -> None:
    prompt_path = run_dir / "prompt.md"
    final_response_path = run_dir / "final_response.md"
    command = build_safe_exec_command(run_dir, model)
    run_notes = [
        "# Run Instructions",
        "",
        f"- Configuration: `{'with_skill' if use_skill else 'without_skill'}`",
        f"- Prompt file: `{prompt_path.name}`",
        f"- Expected final response path: `{final_response_path.name}`",
        "- A reminder template is available at `FINAL_RESPONSE_TEMPLATE.md`.",
        "- This is the safe-first path: the command below uses `codex --disable memories --disable plugins --disable shell_snapshot -a never exec --sandbox workspace-write` and does not use `--dangerously-bypass-approvals-and-sandbox`.",
        "- If the nested executor still fails under Windows sandboxing, stop here and keep this run as prepared-only rather than escalating automatically.",
        "",
        "```powershell",
        command,
        "```",
        "",
    ]
    (run_dir / "RUN_INSTRUCTIONS.md").write_text("\n".join(run_notes), encoding="utf-8")


def parse_jsonl_usage(stdout_text: str) -> dict[str, int]:
    usage: dict[str, int] = {}
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("type") == "turn.completed":
            usage = item.get("usage", {}) or {}
    return {
        "input_tokens": int(usage.get("input_tokens", 0)),
        "cached_input_tokens": int(usage.get("cached_input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
    }


def run_codex_exec(run_dir: Path, prompt: str, model: str | None, timeout_seconds: int) -> dict[str, object]:
    final_response_path = run_dir / "final_response.md"
    stdout_path = run_dir / "codex_stdout.jsonl"
    stderr_path = run_dir / "codex_stderr.log"
    prompt_path = run_dir / "prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    cmd = [
        "codex",
        "--disable",
        "memories",
        "--disable",
        "plugins",
        "--disable",
        "shell_snapshot",
        "-a",
        "never",
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "--ephemeral",
        "--color",
        "never",
        "--json",
        "-C",
        str(run_dir),
        "-o",
        str(final_response_path.resolve()),
        prompt,
    ]
    if model:
        cmd.extend(["--model", model])

    started = time.time()
    completed = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout_seconds,
    )
    duration = round(time.time() - started, 3)

    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    usage = parse_jsonl_usage(completed.stdout)
    total_tokens = usage["input_tokens"] + usage["cached_input_tokens"] + usage["output_tokens"]

    timing = {
        "total_tokens": total_tokens,
        "duration_ms": int(duration * 1000),
        "total_duration_seconds": duration,
        "executor_duration_seconds": duration,
        "executor_exit_code": completed.returncode,
    }
    write_json(run_dir / "timing.json", timing)

    if completed.returncode != 0:
        raise RuntimeError(
            f"codex exec failed in {run_dir} with exit code {completed.returncode}. "
            f"See {stderr_path} and {stdout_path}."
        )

    if not final_response_path.exists():
        raise RuntimeError(f"codex exec did not write {final_response_path}")

    return {
        "timing": timing,
        "stdout_path": stdout_path,
        "stderr_path": stderr_path,
        "final_response_path": final_response_path,
    }


def write_executor_status(run_dir: Path, data: dict[str, object]) -> None:
    write_json(run_dir / "executor_status.json", data)


def load_executor_status(run_dir: Path) -> dict[str, object]:
    status_path = run_dir / "executor_status.json"
    if not status_path.exists():
        return {"status": "missing_status"}
    return json.loads(status_path.read_text(encoding="utf-8"))


def collect_run_snapshots(iteration_dir: Path, cases: list[EvalCase]) -> list[RunSnapshot]:
    snapshots: list[RunSnapshot] = []
    for case in cases:
        eval_dir = iteration_dir / f"eval-{case.eval_id}-{case.eval_name}"
        for configuration in ("with_skill", "without_skill"):
            run_dir = eval_dir / configuration / "run-1"
            status = str(load_executor_status(run_dir).get("status", "missing_status"))
            snapshots.append(
                RunSnapshot(
                    eval_id=case.eval_id,
                    eval_name=case.eval_name,
                    configuration=configuration,
                    run_dir=run_dir,
                    status=status,
                    final_response_exists=(run_dir / "final_response.md").exists(),
                    grading_exists=(run_dir / "grading.json").exists(),
                )
            )
    return snapshots


def write_iteration_status(iteration_dir: Path, cases: list[EvalCase]) -> list[RunSnapshot]:
    snapshots = collect_run_snapshots(iteration_dir, cases)
    status_json = {
        "iteration": iteration_dir.name,
        "runs": [
            {
                "eval_id": snap.eval_id,
                "eval_name": snap.eval_name,
                "configuration": snap.configuration,
                "run_dir": str(snap.run_dir),
                "status": snap.status,
                "final_response_exists": snap.final_response_exists,
                "grading_exists": snap.grading_exists,
            }
            for snap in snapshots
        ],
    }
    write_json(iteration_dir / "status.json", status_json)

    lines = [
        "# Iteration Status",
        "",
        f"- Iteration: `{iteration_dir.name}`",
        "",
        "| Eval | Config | Status | final_response.md | grading.json |",
        "|------|--------|--------|-------------------|--------------|",
    ]
    for snap in snapshots:
        lines.append(
            f"| `{snap.eval_id}-{snap.eval_name}` | `{snap.configuration}` | `{snap.status}` | "
            f"{'yes' if snap.final_response_exists else 'no'} | {'yes' if snap.grading_exists else 'no'} |"
        )
    (iteration_dir / "STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return snapshots


def expectation(text: str, passed: bool, evidence: str) -> dict[str, object]:
    return {"text": text, "passed": passed, "evidence": evidence}


def grade_eval_1(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    root_agents = read_text(outputs_dir / "AGENTS.md")
    local_agents_path = outputs_dir / "packages" / "payments" / "AGENTS.md"
    local_agents = read_text(local_agents_path)

    return [
        expectation(
            expectations[0],
            contains_all(root_agents, ["repository", "pnpm install", "pnpm dev"]),
            "outputs/AGENTS.md keeps repository scope plus shared install/dev commands."
            if contains_all(root_agents, ["repository", "pnpm install", "pnpm dev"])
            else "outputs/AGENTS.md no longer shows clear repository-wide scope and shared commands.",
        ),
        expectation(
            expectations[1],
            local_agents_path.exists()
            and contains_any(local_agents, ["pnpm test --filter payments", "pnpm payments:fixtures"])
            and not contains_any(root_agents, ["payments rules", "pnpm payments:fixtures"]),
            "outputs/packages/payments/AGENTS.md exists with payments-only commands, and outputs/AGENTS.md no longer carries a payments-only rules block."
            if local_agents_path.exists()
            and contains_any(local_agents, ["pnpm test --filter payments", "pnpm payments:fixtures"])
            and not contains_any(root_agents, ["payments rules", "pnpm payments:fixtures"])
            else "Payments-only guidance did not cleanly move to outputs/packages/payments/AGENTS.md.",
        ),
        expectation(
            expectations[2],
            contains_any(final_response, ["inherited", "root"])
            and contains_any(final_response, ["local", "payments", "package"]),
            "final_response.md distinguishes inherited/root guidance from the payments-local change."
            if contains_any(final_response, ["inherited", "root"])
            and contains_any(final_response, ["local", "payments", "package"])
            else "final_response.md does not clearly separate inherited guidance from the payments-local delta.",
        ),
    ]


def grade_eval_2(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    agents = read_text(outputs_dir / "AGENTS.md")
    plan = read_text(outputs_dir / "IMPLEMENTATION_PLAN.md")
    status = read_text(outputs_dir / "TASK_STATUS.md")
    checklist_added = contains_any(plan + "\n" + status, ["migration checklist", "migrate one ingest path", "v2-to-v3", "rollback notes"])

    return [
        expectation(
            expectations[0],
            not contains_any(agents, ["migration checklist", "migrate one ingest path", "v2-to-v3"]),
            "outputs/AGENTS.md stays focused on durable instructions and does not absorb the migration checklist."
            if not contains_any(agents, ["migration checklist", "migrate one ingest path", "v2-to-v3"])
            else "outputs/AGENTS.md still contains migration-only checklist content.",
        ),
        expectation(
            expectations[1],
            checklist_added,
            "outputs/IMPLEMENTATION_PLAN.md or outputs/TASK_STATUS.md now holds the migration checklist."
            if checklist_added
            else "No migration checklist was found in outputs/IMPLEMENTATION_PLAN.md or outputs/TASK_STATUS.md.",
        ),
        expectation(
            expectations[2],
            contains_any(
                final_response,
                [
                    "not the correct destination",
                    "does not belong in agents",
                    "no durable agents",
                    "no agents.md change",
                    "not the right destination",
                    "没有改",
                    "不适合",
                    "临时任务推进信息",
                    "不是稳定、长期",
                    "不应改 ag",
                    "不属于 agents",
                ],
            ),
            "final_response.md explicitly says AGENTS.md was not the right durable destination."
            if contains_any(
                final_response,
                [
                    "not the correct destination",
                    "does not belong in agents",
                    "no durable agents",
                    "no agents.md change",
                    "not the right destination",
                    "没有改",
                    "不适合",
                    "临时任务推进信息",
                    "不是稳定、长期",
                    "不应改 ag",
                    "不属于 agents",
                ],
            )
            else "final_response.md does not clearly reject AGENTS.md as the destination.",
        ),
    ]


def grade_eval_3(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    global_agents = read_text(outputs_dir / "global" / "AGENTS.md")
    website_agents = read_text(outputs_dir / "website" / "AGENTS.md")

    return [
        expectation(
            expectations[0],
            not contains_any(global_agents, ["next.js", "pnpm install", "pnpm dev", "website commands"]),
            "outputs/global/AGENTS.md no longer carries the repo-specific website command block."
            if not contains_any(global_agents, ["next.js", "pnpm install", "pnpm dev", "website commands"])
            else "outputs/global/AGENTS.md still contains website-specific command guidance.",
        ),
        expectation(
            expectations[1],
            contains_all(website_agents, ["pnpm install", "pnpm dev", "pnpm lint"]),
            "outputs/website/AGENTS.md still owns the repository-level Next.js commands."
            if contains_all(website_agents, ["pnpm install", "pnpm dev", "pnpm lint"])
            else "outputs/website/AGENTS.md does not retain the expected repository commands.",
        ),
        expectation(
            expectations[2],
            contains_any(final_response, ["global", "cross-repository", "cross repository"])
            and contains_any(final_response, ["website", "repository-specific", "repo-specific"]),
            "final_response.md explains the global-vs-repository split."
            if contains_any(final_response, ["global", "cross-repository", "cross repository"])
            and contains_any(final_response, ["website", "repository-specific", "repo-specific"])
            else "final_response.md does not clearly explain why the global layer was trimmed.",
        ),
    ]


def grade_eval_4(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    agents = read_text(outputs_dir / "AGENTS.md")

    return [
        expectation(
            expectations[0],
            contains_any(agents, ["仓库级", "已有约束", "开发", "定向测试"]),
            "outputs/AGENTS.md keeps the surrounding Chinese structure and wording."
            if contains_any(agents, ["仓库级", "已有约束", "开发", "定向测试"])
            else "outputs/AGENTS.md drifted away from the existing Chinese style.",
        ),
        expectation(
            expectations[1],
            contains_any(agents, ["修改 `schema/` 后", "schema/` 后", "schema/ 后"])
            and contains_any(agents, ["pnpm db:generate"]),
            "outputs/AGENTS.md includes both the trigger condition and the concrete `pnpm db:generate` command."
            if contains_any(agents, ["修改 `schema/` 后", "schema/` 后", "schema/ 后"])
            and contains_any(agents, ["pnpm db:generate"])
            else "outputs/AGENTS.md does not include a concrete Chinese rule with trigger + command.",
        ),
        expectation(
            expectations[2],
            contains_any(final_response, ["仓库级"])
            and contains_any(final_response, ["重复", "多次", "两次", "review-notes"]),
            "final_response.md explains the repository layer and ties it to repeated failures."
            if contains_any(final_response, ["仓库级"])
            and contains_any(final_response, ["重复", "多次", "两次", "review-notes"])
            else "final_response.md does not explain the repo layer and repeated-trigger rationale clearly enough.",
        ),
    ]


def grade_eval_5(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    root_agents = read_text(outputs_dir / "AGENTS.md")
    local_agents = read_text(outputs_dir / "packages" / "release" / "AGENTS.md")
    local_blocks_prod = contains_any(
        local_agents,
        [
            "do not run `pnpm release:prod`",
            "do not run pnpm release:prod",
            "don't run `pnpm release:prod`",
            "leave production releases to the human release flow",
            "human-operated workflow",
            "ask the release owner to run `pnpm release:prod`",
            "ask the release owner to run pnpm release:prod",
            "release owner to run `pnpm release:prod`",
            "release owner to run pnpm release:prod",
            "do not run production release commands from agent sessions",
            "do not run production deploy or release commands from agent sessions",
            "production releases must be started by a human outside the agent session",
            "由 release owner 执行",
            "请 release owner 运行",
            "由人工运行 `pnpm release:prod`",
            "不要运行 `pnpm release:prod`",
        ],
    )

    return [
        expectation(
            expectations[0],
            contains_any(root_agents, ["do not run production deploy or release commands"]),
            "outputs/AGENTS.md preserves the root safety boundary against production deploy/release commands."
            if contains_any(root_agents, ["do not run production deploy or release commands"])
            else "outputs/AGENTS.md no longer preserves the root production-deploy safety rule.",
        ),
        expectation(
            expectations[1],
            local_blocks_prod or not contains_any(local_agents, ["pnpm release:prod"]),
            "outputs/packages/release/AGENTS.md no longer instructs the agent to run `pnpm release:prod`."
            if local_blocks_prod or not contains_any(local_agents, ["pnpm release:prod"])
            else "outputs/packages/release/AGENTS.md still tells the agent to run `pnpm release:prod`.",
        ),
        expectation(
            expectations[2],
            contains_any(
                final_response,
                [
                    "cannot override",
                    "can't override",
                    "higher-priority safety",
                    "higher priority safety",
                    "root safety",
                    "inherited safety",
                    "release owner",
                    "human release flow",
                    "human-operated",
                    "agent sessions",
                    "继承",
                    "根层安全",
                    "仓库级安全",
                    "不能覆盖",
                    "不能绕过",
                    "上层明确禁止",
                    "上层安全规则",
                    "安全规则冲突",
                    "不适合继续留在本地",
                    "人工",
                    "由人工",
                    "release owner",
                    "agent 会话里执行 production release",
                ],
            ),
            "final_response.md explains that the local file cannot override the higher-priority safety boundary."
            if contains_any(
                final_response,
                [
                    "cannot override",
                    "can't override",
                    "higher-priority safety",
                    "higher priority safety",
                    "root safety",
                    "inherited safety",
                    "release owner",
                    "human release flow",
                    "human-operated",
                    "agent sessions",
                    "继承",
                    "根层安全",
                    "仓库级安全",
                    "不能覆盖",
                    "不能绕过",
                    "上层明确禁止",
                    "上层安全规则",
                    "安全规则冲突",
                    "不适合继续留在本地",
                    "人工",
                    "由人工",
                    "release owner",
                    "agent 会话里执行 production release",
                ],
            )
            else "final_response.md does not explain the inherited safety precedence clearly enough.",
        ),
    ]


def grade_eval_6(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    agents = read_text(outputs_dir / "AGENTS.md")
    status = read_text(outputs_dir / "TASK_STATUS.md")

    return [
        expectation(
            expectations[0],
            not contains_any(
                agents,
                [
                    "reporting exports",
                    "reporting export",
                    "extra careful with reporting exports",
                    "export destination",
                    "export path",
                    "output location",
                ],
            ),
            "outputs/AGENTS.md does not add a new permanent reporting-export rule."
            if not contains_any(
                agents,
                [
                    "reporting exports",
                    "reporting export",
                    "extra careful with reporting exports",
                    "export destination",
                    "export path",
                    "output location",
                ],
            )
            else "outputs/AGENTS.md still adds a permanent reminder from a weak signal.",
        ),
        expectation(
            expectations[1],
            contains_any(
                status,
                [
                    "keep tracking whether this repeats",
                    "before promoting",
                    "observation log",
                    "watch for repetition",
                    "重复出现",
                    "再次出现",
                    "再升级",
                    "promote it",
                    "specific rule then",
                    "具体规则",
                    "keep this in task tracking",
                    "unless the same confusion repeats",
                    "if the same confusion repeats",
                    "同类问题再次出现",
                    "暂不新增永久",
                    "先作为任务跟踪",
                    "not enough evidence",
                    "do not add a permanent",
                    "one recent review note is not enough evidence",
                    "等问题重复出现",
                    "不够证据",
                    "only one review note",
                    "promote to `agents.md` only if",
                    "becomes a concrete path or command boundary",
                    "还没有足够证据",
                    "没有足够证据",
                    "证据还不够强",
                ],
            ),
            "outputs/TASK_STATUS.md records the observation as a non-durable note."
            if contains_any(
                status,
                [
                    "keep tracking whether this repeats",
                    "before promoting",
                    "observation log",
                    "watch for repetition",
                    "重复出现",
                    "再次出现",
                    "再升级",
                    "promote it",
                    "specific rule then",
                    "具体规则",
                    "keep this in task tracking",
                    "unless the same confusion repeats",
                    "if the same confusion repeats",
                    "同类问题再次出现",
                    "暂不新增永久",
                    "先作为任务跟踪",
                    "not enough evidence",
                    "do not add a permanent",
                    "one recent review note is not enough evidence",
                    "等问题重复出现",
                    "不够证据",
                    "only one review note",
                    "promote to `agents.md` only if",
                    "becomes a concrete path or command boundary",
                    "还没有足够证据",
                    "没有足够证据",
                    "证据还不够强",
                ],
            )
            else "outputs/TASK_STATUS.md does not record the one-off observation as a non-durable note.",
        ),
        expectation(
            expectations[2],
            contains_any(
                final_response,
                [
                    "not durable enough",
                    "not strong enough",
                    "one-off",
                    "one off",
                    "single note",
                    "not enough evidence",
                    "不适合加永久",
                    "不足以沉淀成长期",
                    "一次性观察",
                    "不够支撑持久仓库规则",
                    "单次评论",
                    "单次反馈",
                    "不足以升格",
                    "永久指令",
                    "先作为任务跟踪项",
                    "还没有足够证据",
                    "没有足够证据",
                    "证据还不够强",
                    "不够强",
                    "升格成永久",
                    "reviewer 单次备注",
                ],
            ),
            "final_response.md says the trigger evidence is not durable enough yet."
            if contains_any(
                final_response,
                [
                    "not durable enough",
                    "not strong enough",
                    "one-off",
                    "one off",
                    "single note",
                    "not enough evidence",
                    "不适合加永久",
                    "不足以沉淀成长期",
                    "一次性观察",
                    "不够支撑持久仓库规则",
                    "单次评论",
                    "单次反馈",
                    "不足以升格",
                    "永久指令",
                    "先作为任务跟踪项",
                    "还没有足够证据",
                    "没有足够证据",
                    "证据还不够强",
                    "不够强",
                    "升格成永久",
                    "reviewer 单次备注",
                ],
            )
            else "final_response.md does not clearly reject the weak signal as insufficient.",
        ),
    ]


def grade_eval_7(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    agents = read_text(outputs_dir / "AGENTS.md")
    readme = read_text(outputs_dir / "README.md")
    architecture = read_text(outputs_dir / "ARCHITECTURE.md")

    return [
        expectation(
            expectations[0],
            not contains_any(agents, ["project overview", "new contributors should start"])
            and contains_any(readme, ["overview", "product helps finance teams"]),
            "Human onboarding moved out of outputs/AGENTS.md and into outputs/README.md."
            if not contains_any(agents, ["project overview", "new contributors should start"])
            and contains_any(readme, ["overview", "product helps finance teams"])
            else "Human onboarding content still dominates outputs/AGENTS.md.",
        ),
        expectation(
            expectations[1],
            not contains_any(agents, ["queue topology changed twice", "operational variance during quarter-end spikes"])
            and contains_any(architecture, ["background", "queue topology changed twice", "operational variance"]),
            "Architecture explanation moved to outputs/ARCHITECTURE.md."
            if not contains_any(agents, ["queue topology changed twice", "operational variance during quarter-end spikes"])
            and contains_any(architecture, ["background", "queue topology changed twice", "operational variance"])
            else "Architecture explanation still lives in outputs/AGENTS.md instead of outputs/ARCHITECTURE.md.",
        ),
        expectation(
            expectations[2],
            contains_any(final_response, ["README.md", "ARCHITECTURE.md", "AGENTS.md"])
            and contains_any(final_response, ["execution rules", "onboarding", "architecture"]),
            "final_response.md explains the document-boundary split between AGENTS.md, README.md, and ARCHITECTURE.md."
            if contains_any(final_response, ["README.md", "ARCHITECTURE.md", "AGENTS.md"])
            and contains_any(final_response, ["execution rules", "onboarding", "architecture"])
            else "final_response.md does not clearly explain the document-boundary cleanup.",
        ),
    ]


def grade_eval_12(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    agents = read_text(outputs_dir / "AGENTS.md")
    readme = read_text(outputs_dir / "README.md")
    architecture = read_text(outputs_dir / "ARCHITECTURE.md")

    onboarding_removed_from_agents = not contains_any(
        agents,
        [
            "project overview",
            "new contributors should start",
            "understanding the product story",
            "spreadsheet workflow into a distributed system",
        ],
    )
    readme_or_routing_owns_onboarding = contains_any(
        readme,
        [
            "overview",
            "product helps finance teams",
            "new contributors should start",
            "spreadsheet workflow",
        ],
    ) or contains_any(
        agents,
        [
            "read `README.md`",
            "keep human onboarding in `README.md`",
            "human onboarding in `README.md`",
            "do not duplicate either document here",
        ],
    )

    architecture_removed_from_agents = not contains_any(
        agents,
        [
            "queue topology changed twice",
            "operational variance during quarter-end spikes",
            "the api layer talks to workers",
            "historically the queue topology changed twice",
        ],
    )
    architecture_or_routing_owns_background = contains_any(
        architecture,
        [
            "background",
            "queue topology changed twice",
            "operational variance",
            "current modules",
        ],
    ) or contains_any(
        agents,
        [
            "read `ARCHITECTURE.md`",
            "keep architecture background in `ARCHITECTURE.md`",
            "architecture background in `ARCHITECTURE.md`",
            "do not duplicate either document here",
        ],
    )

    return [
        expectation(
            expectations[0],
            onboarding_removed_from_agents and readme_or_routing_owns_onboarding,
            "Human onboarding no longer dominates outputs/AGENTS.md, and onboarding ownership stays with README.md."
            if onboarding_removed_from_agents and readme_or_routing_owns_onboarding
            else "Human onboarding content still dominates outputs/AGENTS.md.",
        ),
        expectation(
            expectations[1],
            architecture_removed_from_agents and architecture_or_routing_owns_background,
            "Architecture explanation no longer lives in outputs/AGENTS.md, and ARCHITECTURE.md remains the owning document."
            if architecture_removed_from_agents and architecture_or_routing_owns_background
            else "Architecture explanation still lives in outputs/AGENTS.md instead of outputs/ARCHITECTURE.md.",
        ),
        expectation(
            expectations[2],
            contains_any(final_response, ["README.md", "ARCHITECTURE.md", "AGENTS.md"])
            and contains_any(
                final_response,
                [
                    "execution rules",
                    "onboarding",
                    "architecture",
                    "single file",
                    "one file",
                    "不应",
                    "不能为了",
                    "不应该为了",
                ],
            ),
            "final_response.md explains the document-boundary split between AGENTS.md, README.md, and ARCHITECTURE.md."
            if contains_any(final_response, ["README.md", "ARCHITECTURE.md", "AGENTS.md"])
            and contains_any(
                final_response,
                [
                    "execution rules",
                    "onboarding",
                    "architecture",
                    "single file",
                    "one file",
                    "不应",
                    "不能为了",
                    "不应该为了",
                ],
            )
            else "final_response.md does not clearly explain why the single-file request should not override document boundaries.",
        ),
    ]


def grade_eval_8(outputs_dir: Path, final_response: str, expectations: list[str]) -> list[dict[str, object]]:
    agents = read_text(outputs_dir / "AGENTS.md")

    return [
        expectation(
            expectations[0],
            contains_any(agents, ["pnpm preflight"]) and not contains_any(agents, ["pnpm verify-all"]),
            "outputs/AGENTS.md now points to `pnpm preflight` and no longer references `pnpm verify-all`."
            if contains_any(agents, ["pnpm preflight"]) and not contains_any(agents, ["pnpm verify-all"])
            else "outputs/AGENTS.md still keeps the stale validation command.",
        ),
        expectation(
            expectations[1],
            contains_any(final_response, ["package.json", "README.md", "current repository command surface", "current repo evidence"]),
            "final_response.md cites current repo evidence such as package.json/README.md for the updated command."
            if contains_any(final_response, ["package.json", "README.md", "current repository command surface", "current repo evidence"])
            else "final_response.md does not ground the cleanup in current repository evidence.",
        ),
        expectation(
            expectations[2],
            contains_any(final_response, ["stale-rule cleanup", "stale rule cleanup", "stale", "current command surface"]),
            "final_response.md frames the change as stale-rule cleanup."
            if contains_any(final_response, ["stale-rule cleanup", "stale rule cleanup", "stale", "current command surface"])
            else "final_response.md does not describe this as stale-rule cleanup.",
        ),
    ]


GRADERS: dict[int, Callable[[Path, str, list[str]], list[dict[str, object]]]] = {
    1: grade_eval_1,
    2: grade_eval_2,
    3: grade_eval_3,
    4: grade_eval_4,
    5: grade_eval_5,
    6: grade_eval_6,
    7: grade_eval_7,
    8: grade_eval_8,
    9: grade_eval_3,
    10: grade_eval_5,
    11: grade_eval_6,
    12: grade_eval_12,
}


def grade_run(case: EvalCase, run_dir: Path) -> dict[str, object]:
    outputs_dir = run_dir / "outputs"
    final_response_path = run_dir / "final_response.md"
    final_response = read_text(final_response_path)
    expectations = GRADERS[case.eval_id](outputs_dir, final_response, case.expectations)
    summary = summarize_expectations(expectations)
    timing = json.loads((run_dir / "timing.json").read_text(encoding="utf-8"))
    executor_total_tokens = int(timing.get("total_tokens", 0))
    final_response_chars = len(final_response)

    output_chars = 0
    for path in outputs_dir.rglob("*"):
        if path.is_file():
            output_chars += len(read_text(path))

    grading = {
        "expectations": expectations,
        "summary": summary,
        "execution_metrics": {
            "tool_calls": {},
            "total_tool_calls": 0,
            "total_steps": 0,
            "errors_encountered": 0,
            "executor_total_tokens": executor_total_tokens,
            "executor_total_tokens_recorded": executor_total_tokens > 0,
            "final_response_chars": final_response_chars,
            "output_chars": output_chars,
            "transcript_chars": len(read_text(run_dir / "codex_stdout.jsonl")),
        },
        "timing": {
            "executor_total_tokens": executor_total_tokens,
            "executor_duration_seconds": timing["executor_duration_seconds"],
            "total_duration_seconds": timing["total_duration_seconds"],
        },
        "claims": [],
        "user_notes_summary": {
            "uncertainties": [],
            "needs_review": [],
            "workarounds": [],
        },
        "eval_feedback": {
            "suggestions": [],
            "overall": "No deterministic eval-gap suggestions were generated in this run.",
        },
    }
    write_json(run_dir / "grading.json", grading)
    return grading


def load_benchmark_run_result(case: EvalCase, configuration: str, run_dir: Path) -> dict[str, object]:
    grading = json.loads((run_dir / "grading.json").read_text(encoding="utf-8"))
    timing = json.loads((run_dir / "timing.json").read_text(encoding="utf-8"))
    execution_metrics = grading.get("execution_metrics", {})
    notes_summary = grading.get("user_notes_summary", {})
    executor_total_tokens = int(timing.get("total_tokens", 0))
    final_response_chars = int(execution_metrics.get("final_response_chars", len(read_text(run_dir / "final_response.md"))))

    notes: list[str] = []
    notes.extend(notes_summary.get("uncertainties", []))
    notes.extend(notes_summary.get("needs_review", []))
    notes.extend(notes_summary.get("workarounds", []))

    return {
        "eval_id": case.eval_id,
        "configuration": configuration,
        "run_number": 1,
        "result": {
            "pass_rate": grading["summary"]["pass_rate"],
            "passed": grading["summary"]["passed"],
            "failed": grading["summary"]["failed"],
            "total": grading["summary"]["total"],
            "time_seconds": timing.get("total_duration_seconds", 0.0),
            "executor_total_tokens": executor_total_tokens,
            "final_response_chars": final_response_chars,
            "tokens": executor_total_tokens,
            "tool_calls": execution_metrics.get("total_tool_calls", 0),
            "errors": execution_metrics.get("errors_encountered", 0),
        },
        "expectations": grading.get("expectations", []),
        "notes": notes,
    }


def build_precise_benchmark_stats(iteration_dir: Path, cases: list[EvalCase]) -> tuple[list[dict[str, object]], dict[str, object], dict[str, dict[str, int]]]:
    runs: list[dict[str, object]] = []
    config_names = ("with_skill", "without_skill")
    token_usage_counts: dict[str, dict[str, int]] = {
        config_name: {"recorded": 0, "missing": 0} for config_name in config_names
    }

    for case in cases:
        eval_dir = iteration_dir / f"eval-{case.eval_id}-{case.eval_name}"
        for configuration in config_names:
            run_dir = eval_dir / configuration / "run-1"
            run_result = load_benchmark_run_result(case, configuration, run_dir)
            runs.append(run_result)
            if run_result["result"]["executor_total_tokens"] > 0:
                token_usage_counts[configuration]["recorded"] += 1
            else:
                token_usage_counts[configuration]["missing"] += 1

    run_summary: dict[str, object] = {}
    for configuration in config_names:
        config_runs = [run for run in runs if run["configuration"] == configuration]
        pass_rates = [float(run["result"]["pass_rate"]) for run in config_runs]
        time_seconds = [float(run["result"]["time_seconds"]) for run in config_runs]
        final_response_chars = [float(run["result"]["final_response_chars"]) for run in config_runs]
        executor_total_tokens = [
            float(run["result"]["executor_total_tokens"])
            for run in config_runs
            if float(run["result"]["executor_total_tokens"]) > 0
        ]

        run_summary[configuration] = {
            "pass_rate": calculate_stats(pass_rates),
            "time_seconds": calculate_stats(time_seconds),
            "executor_total_tokens": calculate_stats(executor_total_tokens),
            "final_response_chars": calculate_stats(final_response_chars),
            "tokens": calculate_stats(executor_total_tokens),
            "token_usage": {
                "recorded_runs": token_usage_counts[configuration]["recorded"],
                "missing_runs": token_usage_counts[configuration]["missing"],
            },
        }

    with_skill = run_summary["with_skill"]
    without_skill = run_summary["without_skill"]

    run_summary["delta"] = {
        "pass_rate": f"{with_skill['pass_rate']['mean'] - without_skill['pass_rate']['mean']:+.2f}",
        "time_seconds": f"{with_skill['time_seconds']['mean'] - without_skill['time_seconds']['mean']:+.1f}",
        "executor_total_tokens": f"{with_skill['executor_total_tokens']['mean'] - without_skill['executor_total_tokens']['mean']:+.0f}",
        "final_response_chars": f"{with_skill['final_response_chars']['mean'] - without_skill['final_response_chars']['mean']:+.0f}",
        "tokens": f"{with_skill['executor_total_tokens']['mean'] - without_skill['executor_total_tokens']['mean']:+.0f}",
    }

    return runs, run_summary, token_usage_counts


def build_eval_metadata(case: EvalCase) -> dict[str, object]:
    return {
        "eval_id": case.eval_id,
        "eval_name": case.eval_name,
        "prompt": case.prompt,
        "assertions": case.expectations,
    }


def write_iteration_metadata(
    iteration_dir: Path,
    cases: list[EvalCase],
    eval_selection: str,
    model: str | None,
    max_parallel: int,
) -> None:
    write_json(
        iteration_dir / ITERATION_METADATA_NAME,
        {
            "iteration": iteration_dir.name,
            "eval_ids": [case.eval_id for case in cases],
            "eval_selection": eval_selection,
            "benchmark_style": benchmark_style_for_eval_selection(eval_selection),
            "model": model,
            "max_parallel": max_parallel,
            "with_skill_context_mode": "explicit_local_skill_copy",
            "default_nested_execution_policy": "workspace-write + approval never + disable memories/plugins/shell_snapshot",
            "shell_inspection_policy": "read-only local shell inspection allowed",
        },
    )


def update_benchmark_metadata(
    iteration_dir: Path,
    benchmark_path: Path,
    cases: list[EvalCase],
    runs_per_configuration: int,
    eval_selection: str,
) -> None:
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    runs, run_summary, token_usage_counts = build_precise_benchmark_stats(iteration_dir, cases)
    benchmark["runs"] = runs
    benchmark["run_summary"] = run_summary
    benchmark["metadata"]["skill_name"] = "agents-md-improver"
    benchmark["metadata"]["skill_path"] = str(SKILL_ROOT)
    benchmark["metadata"]["executor_model"] = "codex-exec"
    benchmark["metadata"]["analyzer_model"] = "deterministic-local-grading"
    benchmark["metadata"]["evals_run"] = [case.eval_id for case in cases]
    benchmark["metadata"]["eval_selection"] = eval_selection
    benchmark["metadata"]["benchmark_style"] = benchmark_style_for_eval_selection(eval_selection)
    benchmark["metadata"]["with_skill_context_mode"] = "explicit_local_skill_copy"
    benchmark["metadata"]["shell_inspection_policy"] = "read-only local shell inspection allowed"
    benchmark["metadata"]["primary_interpretation"] = "absolute end-to-end pass rates first; with-vs-without delta second"
    benchmark["metadata"]["runs_per_configuration"] = runs_per_configuration
    benchmark["metadata"]["metric_definitions"] = {
        "executor_total_tokens": "Per-run executor token usage from timing.json.total_tokens when codex exec usage is available.",
        "final_response_chars": "Character length of final_response.md.",
    }
    benchmark["notes"] = [
        "This benchmark was executed automatically with `codex exec` on copied fixtures.",
        "Grading is deterministic and eval-specific; it does not rely on a freeform reviewer pass.",
        f"Executor total-token usage was recorded for with_skill {token_usage_counts['with_skill']['recorded']}/{token_usage_counts['with_skill']['recorded'] + token_usage_counts['with_skill']['missing']} runs.",
        f"Executor total-token usage was recorded for without_skill {token_usage_counts['without_skill']['recorded']}/{token_usage_counts['without_skill']['recorded'] + token_usage_counts['without_skill']['missing']} runs.",
    ]
    benchmark_path.write_text(json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rewrite_benchmark_markdown(iteration_dir: Path) -> None:
    benchmark = json.loads((iteration_dir / "benchmark.json").read_text(encoding="utf-8"))
    run_summary = benchmark["run_summary"]
    notes = benchmark.get("notes", [])
    lines = [
        "# Skill Benchmark: agents-md-improver",
        "",
        f"**Model**: {benchmark['metadata']['executor_model']}",
        f"**Date**: {benchmark['metadata']['timestamp']}",
        f"**Benchmark Style**: {benchmark['metadata'].get('benchmark_style', 'unknown')}",
        f"**Eval Selection**: {benchmark['metadata'].get('eval_selection', 'unknown')}",
        f"**Evals**: {', '.join(str(item) for item in benchmark['metadata']['evals_run'])} (1 run each per configuration)",
        "",
        "## Summary",
        "",
        "| Metric | With Skill | Without Skill | Delta |",
        "|--------|------------|---------------|-------|",
        f"| Pass Rate | {run_summary['with_skill']['pass_rate']['mean']*100:.0f}% ± {run_summary['with_skill']['pass_rate']['stddev']*100:.0f}% | {run_summary['without_skill']['pass_rate']['mean']*100:.0f}% ± {run_summary['without_skill']['pass_rate']['stddev']*100:.0f}% | {run_summary['delta']['pass_rate']} |",
        f"| Time | {run_summary['with_skill']['time_seconds']['mean']:.1f}s ± {run_summary['with_skill']['time_seconds']['stddev']:.1f}s | {run_summary['without_skill']['time_seconds']['mean']:.1f}s ± {run_summary['without_skill']['time_seconds']['stddev']:.1f}s | {run_summary['delta']['time_seconds']}s |",
        f"| Executor Total Tokens | {run_summary['with_skill']['executor_total_tokens']['mean']:.0f} ± {run_summary['with_skill']['executor_total_tokens']['stddev']:.0f} | {run_summary['without_skill']['executor_total_tokens']['mean']:.0f} ± {run_summary['without_skill']['executor_total_tokens']['stddev']:.0f} | {run_summary['delta']['executor_total_tokens']} |",
        f"| Final Response Chars | {run_summary['with_skill']['final_response_chars']['mean']:.0f} ± {run_summary['with_skill']['final_response_chars']['stddev']:.0f} | {run_summary['without_skill']['final_response_chars']['mean']:.0f} ± {run_summary['without_skill']['final_response_chars']['stddev']:.0f} | {run_summary['delta']['final_response_chars']} |",
        "",
        "## Reading Guide",
        "",
        "- Read this as a production-like `with_skill` vs `without_skill` comparison first: both sides can inspect the prepared repository copy with read-only shell access.",
        "- Treat the absolute pass rates for `with_skill` and `without_skill` as the primary result.",
        "- Treat the delta as secondary context rather than the only success metric.",
        "- Treat `Executor Total Tokens` as executor usage from `timing.json.total_tokens`, not as response length.",
        "- Treat `Final Response Chars` as the size of `final_response.md`, not as token usage.",
        "- `with_skill` currently uses explicit local skill-file loading inside the run directory, not native nested skill discovery.",
        "",
        "## Notes",
        "",
    ]
    for note in notes:
        lines.append(f"- {note}")
    (iteration_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_results_summary(iteration_dir: Path, cases: list[EvalCase]) -> None:
    benchmark = json.loads((iteration_dir / "benchmark.json").read_text(encoding="utf-8"))
    runs = benchmark["runs"]
    run_summary = benchmark["run_summary"]

    by_eval: dict[int, dict[str, object]] = {}
    for run in runs:
        eval_id = int(run["eval_id"])
        by_eval.setdefault(eval_id, {"eval_id": eval_id, "eval_name": next(case.eval_name for case in cases if case.eval_id == eval_id)})
        by_eval[eval_id][run["configuration"]] = {
            "passed": run["result"]["passed"],
            "failed": run["result"]["failed"],
            "total": run["result"]["total"],
            "pass_rate": run["result"]["pass_rate"],
        }

    results_json = {
        "skill_name": "agents-md-improver",
        "configuration": "production_like_comparative_automatic_benchmark",
        "benchmark_path": "benchmark.json",
        "benchmark_style": benchmark["metadata"].get("benchmark_style", "unknown"),
        "eval_selection": benchmark["metadata"].get("eval_selection", "unknown"),
        "evals": [by_eval[case.eval_id] for case in cases],
        "summary": {
            "with_skill": {
                "passed": sum(run["result"]["passed"] for run in runs if run["configuration"] == "with_skill"),
                "failed": sum(run["result"]["failed"] for run in runs if run["configuration"] == "with_skill"),
                "total": sum(run["result"]["total"] for run in runs if run["configuration"] == "with_skill"),
                "pass_rate": round(run_summary["with_skill"]["pass_rate"]["mean"], 4),
            },
            "without_skill": {
                "passed": sum(run["result"]["passed"] for run in runs if run["configuration"] == "without_skill"),
                "failed": sum(run["result"]["failed"] for run in runs if run["configuration"] == "without_skill"),
                "total": sum(run["result"]["total"] for run in runs if run["configuration"] == "without_skill"),
                "pass_rate": round(run_summary["without_skill"]["pass_rate"]["mean"], 4),
            },
            "delta": {"pass_rate": run_summary["delta"]["pass_rate"]},
        },
        "notes": [
            "This file summarizes the current production-like comparative benchmark artifacts for the iteration.",
            "Interpret absolute with_skill and without_skill pass rates first, then compare the delta.",
            "Executor total-token fields come from timing.json.total_tokens when codex exec usage is available.",
            "Final-response length fields come from final_response.md character counts and are not token metrics.",
        ],
    }
    write_json(iteration_dir / "results.json", results_json)

    lines = [
        "# AGENTS.md Improver Benchmark Summary",
        "",
        "## Scope",
        "",
        "- Run type: production-like automatic comparative benchmark",
        f"- Skill under test: `{SKILL_ROOT.relative_to(REPO_ROOT)}`",
        f"- Benchmark style: `{benchmark['metadata'].get('benchmark_style', 'unknown')}`",
        f"- Eval selection: `{benchmark['metadata'].get('eval_selection', 'unknown')}`",
        "- Benchmark artifact: [benchmark.json](benchmark.json)",
        "",
        "## Results",
        "",
    ]
    for case in cases:
        eval_result = by_eval[case.eval_id]
        with_skill = eval_result["with_skill"]
        without_skill = eval_result["without_skill"]
        lines.append(
            f"- `eval-{case.eval_id}-{case.eval_name}`: "
            f"with skill `{with_skill['passed']}/{with_skill['total']}`, "
            f"without skill `{without_skill['passed']}/{without_skill['total']}`"
        )

    lines.extend(
        [
            "",
            "## Aggregate",
            "",
            f"- With skill: `{results_json['summary']['with_skill']['passed']}/{results_json['summary']['with_skill']['total']}` expectations passed, "
            f"pass rate `{results_json['summary']['with_skill']['pass_rate']}`",
            f"- Without skill: `{results_json['summary']['without_skill']['passed']}/{results_json['summary']['without_skill']['total']}` expectations passed, "
            f"pass rate `{results_json['summary']['without_skill']['pass_rate']}`",
            f"- Delta (secondary): `{results_json['summary']['delta']['pass_rate']}`",
            "",
            "## Notes",
            "",
            "- This summary reflects a production-like `with_skill` vs `without_skill` run on copied fixtures with read-only local shell inspection allowed.",
            "- Grading is deterministic and eval-specific rather than freeform manual review.",
            "- `with_skill` currently uses explicit local skill-file loading rather than native nested skill discovery.",
        ]
    )
    (iteration_dir / "run-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_review_html(skill_creator_dir: Path, iteration_dir: Path) -> str | None:
    review_script = skill_creator_dir / "eval-viewer" / "generate_review.py"
    review_path = iteration_dir / "review.html"
    error_path = iteration_dir / "review_generation_error.log"
    cmd = [
        sys.executable,
        "-X",
        "utf8",
        str(review_script),
        str(iteration_dir),
        "--skill-name",
        "agents-md-improver",
        "--benchmark",
        str(iteration_dir / "benchmark.json"),
        "--static",
        str(review_path),
    ]
    try:
        subprocess.run(cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
    except subprocess.CalledProcessError as exc:
        error_lines = [
            "review.html generation failed, but benchmark artifacts were still produced.",
            "",
            f"Command: {' '.join(cmd)}",
            f"Exit code: {exc.returncode}",
            "",
            "STDOUT:",
            exc.stdout or "",
            "",
            "STDERR:",
            exc.stderr or "",
        ]
        error_path.write_text("\n".join(error_lines), encoding="utf-8")
        return str(error_path)
    if error_path.exists():
        error_path.unlink()
    return None


def prepare_iteration(
    iteration_name: str,
    cases: list[EvalCase],
    model: str | None,
    eval_selection: str,
    max_parallel: int,
) -> Path:
    iteration_dir = DEFAULT_WORKSPACE_ROOT / iteration_name
    if iteration_dir.exists():
        raise FileExistsError(
            f"Iteration directory already exists: {iteration_dir}. "
            "Choose a new --iteration-name instead of deleting it automatically."
        )
    iteration_dir.mkdir(parents=True, exist_ok=True)

    for case in cases:
        eval_dir = iteration_dir / f"eval-{case.eval_id}-{case.eval_name}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        write_json(eval_dir / "eval_metadata.json", build_eval_metadata(case))

        for config_name, use_skill in (("with_skill", True), ("without_skill", False)):
            run_dir = eval_dir / config_name / "run-1"
            run_dir.mkdir(parents=True, exist_ok=True)
            prepare_run_dir(case, run_dir, use_skill)
            prompt = build_executor_prompt(case, use_skill)
            (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
            write_final_response_template(run_dir, case)
            write_run_instructions(run_dir, use_skill, model)
            write_executor_status(
                run_dir,
                {
                    "status": "prepared",
                    "configuration": config_name,
                    "uses_local_skill_context": use_skill,
                    "eval_selection": eval_selection,
                    "execution_mode": "safe_first_prepare_only",
                },
            )

    write_iteration_metadata(iteration_dir, cases, eval_selection, model, max_parallel)
    write_iteration_instructions(iteration_dir, cases, model, eval_selection, max_parallel)
    write_iteration_status(iteration_dir, cases)
    return iteration_dir


def write_iteration_instructions(
    iteration_dir: Path,
    cases: list[EvalCase],
    model: str | None,
    eval_selection: str,
    max_parallel: int,
) -> None:
    lines = [
        "# Safe-First Benchmark Workflow",
        "",
        "This iteration was prepared without executing nested `codex exec` runs.",
        "",
        "## What Is Ready",
        "",
        "- Each run directory already contains copied fixtures under `outputs/`.",
        "- Each run directory already has `prompt.md`, `RUN_INSTRUCTIONS.md`, and `executor_status.json`.",
        "- `with_skill` runs contain a local copy of `skills/agents-md-improver/` for explicit skill-context loading.",
        f"- Eval selection for this iteration: `{eval_selection}`.",
        f"- Benchmark style for this iteration: `{benchmark_style_for_eval_selection(eval_selection)}`.",
        f"- Default safe-run max parallelism captured for this iteration: `{max_parallel}`.",
        "",
        "## Safe Paths",
        "",
        "1. Use `--mode safe-run` from this script to let it attempt sandboxed nested execution.",
        "2. Or open an individual run directory and follow its `RUN_INSTRUCTIONS.md` manually.",
        "3. After runs finish, use `--mode grade-benchmark` on the same iteration to generate `benchmark.json`, `results.json`, and `review.html`.",
        "",
        "## Strategy Notes",
        "",
        "- `informative` is the default production-like comparative subset for automatic runs because it avoids the lowest-discrimination evals while preserving real repo exploration.",
        "- `executor-health` is the smoke subset for proving the nested executor can still complete an isolated run.",
        "- `low-discrimination` is kept only for diagnosis or regression checks, not for default skill-lift claims.",
        "- In the comparative path, both `with_skill` and `without_skill` may inspect the prepared repo copy with read-only shell access; the intended main variable is whether the skill is available, not whether local inspection is possible.",
        "",
        "## Prepared Evals",
        "",
    ]
    for case in cases:
        lines.append(f"- `eval-{case.eval_id}-{case.eval_name}`")

    if model:
        lines.extend(["", f"- Model hint captured for prepared commands: `{model}`"])

    (iteration_dir / "RUN_INSTRUCTIONS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def safe_execute_iteration(
    iteration_dir: Path,
    cases: list[EvalCase],
    model: str | None,
    timeout_seconds: int,
    max_parallel: int,
) -> None:
    work_items: list[tuple[EvalCase, str, Path, str]] = []
    for case in cases:
        eval_dir = iteration_dir / f"eval-{case.eval_id}-{case.eval_name}"
        for config_name in ("with_skill", "without_skill"):
            run_dir = eval_dir / config_name / "run-1"
            prompt_path = run_dir / "prompt.md"
            prompt = read_text(prompt_path)
            if not prompt:
                raise RuntimeError(f"Missing prompt for {run_dir}")
            work_items.append((case, config_name, run_dir, prompt))

    failures: list[str] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel) as executor:
        future_map = {
            executor.submit(run_codex_exec, run_dir, prompt, model, timeout_seconds): (case, config_name, run_dir)
            for case, config_name, run_dir, prompt in work_items
        }

        for future in concurrent.futures.as_completed(future_map):
            case, config_name, run_dir = future_map[future]
            try:
                result = future.result()
                write_executor_status(
                    run_dir,
                    {
                        "status": "executed",
                        "configuration": config_name,
                        "execution_mode": "workspace_write_approval_never",
                        "final_response_path": str(result["final_response_path"]),
                    },
                )
            except Exception as exc:
                write_executor_status(
                    run_dir,
                    {
                        "status": "execution_failed",
                        "configuration": config_name,
                        "execution_mode": "workspace_write_approval_never",
                        "error": str(exc),
                    },
                )
                failures.append(f"eval-{case.eval_id}-{case.eval_name}/{config_name}: {exc}")
    write_iteration_status(iteration_dir, cases)
    if failures:
        raise RuntimeError("One or more nested runs failed:\n" + "\n".join(failures))


def grade_and_benchmark_iteration(
    iteration_dir: Path,
    cases: list[EvalCase],
    skill_creator_dir: Path,
    execution_label: str,
    eval_selection: str,
) -> Path:
    aggregate_script = skill_creator_dir / "scripts" / "aggregate_benchmark.py"
    missing_runs: list[str] = []

    for case in cases:
        eval_dir = iteration_dir / f"eval-{case.eval_id}-{case.eval_name}"
        for config_name in ("with_skill", "without_skill"):
            run_dir = eval_dir / config_name / "run-1"
            if not (run_dir / "final_response.md").exists():
                missing_runs.append(str(run_dir))
                continue
            grade_run(case, run_dir)

    if missing_runs:
        write_iteration_status(iteration_dir, cases)
        raise FileNotFoundError(
            "Some runs are not ready for grading yet. Check STATUS.md in the iteration root.\n"
            + "\n".join(missing_runs)
        )

    subprocess.run(
        [
            sys.executable,
            str(aggregate_script),
            str(iteration_dir),
            "--skill-name",
            "agents-md-improver",
            "--skill-path",
            str(SKILL_ROOT),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    update_benchmark_metadata(
        iteration_dir,
        iteration_dir / "benchmark.json",
        cases,
        runs_per_configuration=1,
        eval_selection=eval_selection,
    )
    benchmark = json.loads((iteration_dir / "benchmark.json").read_text(encoding="utf-8"))
    benchmark["metadata"]["executor_model"] = execution_label
    benchmark["notes"] = [
        f"This benchmark used the `{execution_label}` execution path on copied fixtures.",
        f"The active eval selection was `{eval_selection}`.",
        f"The benchmark style was `{benchmark_style_for_eval_selection(eval_selection)}`.",
        "This is intended to approximate real `with_skill` vs `without_skill` use on a prepared repository copy, not a no-evidence controlled experiment.",
        "with_skill uses explicit local skill-context loading rather than relying on nested native skill discovery.",
        "Grading is deterministic and eval-specific; it does not rely on a freeform reviewer pass.",
    ]
    (iteration_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rewrite_benchmark_markdown(iteration_dir)
    generate_results_summary(iteration_dir, cases)
    review_error = generate_review_html(skill_creator_dir, iteration_dir)
    if review_error:
        benchmark = json.loads((iteration_dir / "benchmark.json").read_text(encoding="utf-8"))
        benchmark["notes"].append(
            f"`review.html` generation failed; see `{Path(review_error).name}` for details. Benchmark JSON and summaries are still valid."
        )
        (iteration_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rewrite_benchmark_markdown(iteration_dir)
        generate_results_summary(iteration_dir, cases)
    write_iteration_status(iteration_dir, cases)
    return iteration_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a safe-first comparative benchmark workflow for agents-md-improver.")
    parser.add_argument(
        "--mode",
        choices=["prepare", "safe-run", "grade-benchmark", "status"],
        default="prepare",
        help="`prepare` only materializes workspaces and prompts. `safe-run` prepares and attempts sandboxed nested execution. `grade-benchmark` grades completed runs and builds benchmark artifacts. `status` refreshes STATUS.md and status.json for an existing iteration.",
    )
    parser.add_argument(
        "--iteration-name",
        default="iteration-auto",
        help="Workspace iteration directory name under tmp/agents-md-improver-workspace/",
    )
    parser.add_argument(
        "--eval-ids",
        nargs="*",
        type=int,
        help="Optional subset of eval IDs to run.",
    )
    parser.add_argument(
        "--eval-set",
        choices=["all", "informative", "executor-health", "low-discrimination"],
        help="Named eval subset. `informative` is the default production-like comparative subset for `prepare` and `safe-run` when no explicit IDs are provided.",
    )
    parser.add_argument(
        "--skill-creator-dir",
        help="Path to the local skill-creator installation. Defaults to SKILL_CREATOR_DIR or common home-directory locations.",
    )
    parser.add_argument(
        "--model",
        help="Optional Codex model override passed to `codex exec`.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=300,
        help="Timeout per `codex exec` run.",
    )
    parser.add_argument(
        "--max-parallel",
        type=int,
        default=2,
        help="Maximum number of nested runs to execute in parallel during `safe-run`. Default is 2.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_parallel < 1:
        raise SystemExit("--max-parallel must be at least 1.")
    iteration_dir = DEFAULT_WORKSPACE_ROOT / args.iteration_name

    if args.mode == "prepare":
        selected_ids, eval_selection = resolve_requested_eval_ids(args.eval_ids, args.eval_set, args.mode)
        cases = load_evals(selected_ids)
        if not cases:
            raise SystemExit("No evals selected.")
        iteration_dir = prepare_iteration(args.iteration_name, cases, args.model, eval_selection, args.max_parallel)
        print(f"Prepared safe-first benchmark workspace at: {iteration_dir}")
        return

    if args.mode == "status":
        if not iteration_dir.exists():
            raise SystemExit(f"Iteration directory not found: {iteration_dir}")
        selected_ids, _ = resolve_existing_iteration_eval_ids(iteration_dir, args.eval_ids, args.eval_set)
        cases = load_evals(selected_ids)
        if not cases:
            raise SystemExit("No evals selected.")
        write_iteration_status(iteration_dir, cases)
        print(f"Updated iteration status at: {iteration_dir}")
        return

    if args.mode == "safe-run":
        selected_ids, eval_selection = resolve_requested_eval_ids(args.eval_ids, args.eval_set, args.mode)
        cases = load_evals(selected_ids)
        if not cases:
            raise SystemExit("No evals selected.")
        if iteration_dir.exists():
            raise SystemExit(
                f"Iteration already exists: {iteration_dir}. "
                "Use a new --iteration-name for `safe-run`, or use `--mode grade-benchmark` on an existing prepared iteration."
            )
        iteration_dir = prepare_iteration(args.iteration_name, cases, args.model, eval_selection, args.max_parallel)
        safe_execute_iteration(iteration_dir, cases, args.model, args.timeout_seconds, args.max_parallel)
        skill_creator_dir = find_skill_creator_dir(args.skill_creator_dir)
        grade_and_benchmark_iteration(
            iteration_dir,
            cases,
            skill_creator_dir,
            execution_label="codex-exec-workspace-write-approval-never",
            eval_selection=eval_selection,
        )
        print(f"Generated safe-run benchmark at: {iteration_dir}")
        return

    if not iteration_dir.exists():
        raise SystemExit(f"Iteration directory not found: {iteration_dir}")
    selected_ids, eval_selection = resolve_existing_iteration_eval_ids(iteration_dir, args.eval_ids, args.eval_set)
    cases = load_evals(selected_ids)
    if not cases:
        raise SystemExit("No evals selected.")
    skill_creator_dir = find_skill_creator_dir(args.skill_creator_dir)
    grade_and_benchmark_iteration(
        iteration_dir,
        cases,
        skill_creator_dir,
        execution_label="manual-or-safe-first-exec",
        eval_selection=eval_selection,
    )
    print(f"Generated benchmark artifacts for existing iteration: {iteration_dir}")


if __name__ == "__main__":
    main()
