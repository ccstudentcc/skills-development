# Repository Agent Guide

## Project Overview

This product helps finance teams reconcile daily transactions across many providers. New contributors should start by reading the full onboarding guide, understanding the product story, and learning the history of how the service grew from a spreadsheet workflow into a distributed system.

## Architecture Background

The API layer talks to workers, which talk to event queues, which then flush into storage. Historically the queue topology changed twice, and the current approach exists because the second rewrite reduced operational variance during quarter-end spikes.

## Commands

- Dev: `pnpm dev`
- Lint: `pnpm lint`

## Agent Notes

- Prefer targeted checks before full validation.
