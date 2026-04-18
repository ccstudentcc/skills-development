# Repository Agent Guide

## Scope

- This repository contains a billing dashboard and its background jobs.
- Prefer targeted validation before full preflight.

## Commands

- Install: `pnpm install`
- Dev: `pnpm dev`
- Full validation: `pnpm preflight`

## Payments Rules

- Changes under `packages/payments/` should start with `pnpm test --filter payments`.
- Refresh payment fixtures with `pnpm payments:fixtures`.
- Do not edit generated files under `packages/payments/gen/` directly.

## Notes

- Keep rules short and specific.
