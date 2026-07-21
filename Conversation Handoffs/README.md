# Conversation Handoffs

## Purpose

This folder is for cheap recovery after Hermes is accidentally closed.

Do not store full transcripts here. Store short handoffs only.

## Recommended structure

- `LATEST_HANDOFF.md`
  - The only conversation handoff file a new session should read first.
  - Keep it short and current.
  - Contains latest done, remaining, blocker, and exact next action.

- `archive/`
  - Optional older handoff snapshots.
  - Read only if `LATEST_HANDOFF.md` is missing or unclear.

- `templates/SESSION_HANDOFF_TEMPLATE.md`
  - Copy this format when making a new handoff.

## New conversation startup rule

At the start of a reopened project conversation, read only:

1. `AGENTS.md`
2. `PROJECT_STATUS.md`
3. `Conversation Handoffs/LATEST_HANDOFF.md`

Do not read old session transcripts unless these files are missing, stale, or conflicting.

## During work

For any task that takes more than a few steps, update `LATEST_HANDOFF.md` after meaningful progress.

If the task is important enough to survive accidental close, also update `PROJECT_STATUS.md`.
