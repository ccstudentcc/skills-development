# Repository Agent Guide

## Scope

- This repository contains the event ingestion service.
- Keep rules durable and execution-oriented.

## Commands

- Dev: `pnpm dev`
- Targeted tests: `pnpm test --filter ingest`

## Durable Rules

- Do not print `.env` values.
- Regenerate derived client files after editing `schema/`.
