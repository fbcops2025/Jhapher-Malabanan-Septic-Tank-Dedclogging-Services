# Project Status

## Project goal

Centralize the Jhapher Malabanan NCR website build, project records, final audit, and audit evidence in the requested GitHub repository so website development and preview deployment can continue from one place.

## Current state

The complete static website is now at the repository root. Client project records, the final NCR audit PDF, and audit evidence are under `project-docs/`. The workspace is connected to the requested GitHub repository. Local website checks pass; commit and push are the current working item.

## Current working item

- [ ] Commit and push the centralized project to GitHub.

## Checklist

- [x] Copy the deployable website to the repository root.
- [x] Copy all client-level project records to `project-docs/`.
- [x] Add the final NCR audit PDF and supporting evidence.
- [x] Run website content and static integrity checks.
- [ ] Commit and push the centralized project to GitHub.
- [ ] Replace `example.com` after the final domain is confirmed.
- [ ] Obtain final approval for concept assets and contact/service-area assumptions.

## Completed and verified

- Six website content tests pass.
- HTML and JSON-LD parse checks pass for all five pages.
- JSON, XML, internal-link, local-image, and harmful-placeholder checks pass.
- Final NCR audit PDF copied to `project-docs/audits/`.
- Ten audit evidence files copied to `project-docs/audit-evidence/`.

## Decisions made

- Keep deployable website files at repository root for simple Vercel setup.
- Keep supporting business records and audit materials under `project-docs/`.
- Retain the original source files in the WFW vault as a safety backup rather than deleting them.

## Blockers

- Final production domain is not confirmed, so `example.com` remains a temporary marker.
- Concept assets, primary contact hierarchy, and the `Barado` versus `Baras` service-area wording still need final confirmation before production publication.

## Exact next action

Commit the verified centralized files and push branch `main` to the requested GitHub repository.

## Important files

- `AGENTS.md`: project working rules
- `PROJECT_STATUS.md`: durable recovery state and incomplete checklist
- `Conversation Handoffs/LATEST_HANDOFF.md`: latest short session handoff
- `README.md`: website preview and checks
- `BUILD_STATUS.md`: website build readiness and launch blockers
- `project-docs/README.md`: project record and audit index

## Update rule

Update this file after meaningful progress, decisions, failures, or checklist changes. Keep it short. Never store secrets here.
