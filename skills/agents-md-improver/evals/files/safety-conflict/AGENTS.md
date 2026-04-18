# Repository Agent Guide

## Safety

- Never expose secrets or commit credential-bearing files.
- Do not run production deploy or release commands from agent sessions.

## Commands

- Dev: `pnpm dev`
- Targeted tests: `pnpm test --filter release`
