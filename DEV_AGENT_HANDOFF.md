# Dev Agent Handoff - Jhapher Website

## Mission
Build and harden the Jhapher Malabanan website until it is ready for GitHub + Vercel preview.

## Current readiness
Draft build ready after first QA fixes.

## Project folder
`/home/al/Documents/Projects/Ideas and Management/wfw-business-plans-and-ideas/Main Branch/We Forge Web/WFW - Interested Clients/jhapher-malabanan-septic-tank-declogging-services/website-project`

## Business facts
- Business: Jhapher Malabanan Septic Tank & Declogging Services
- Main branch / center area: Pasig City
- Services: Septic tank siphoning, Pozo negro cleaning, Declogging / baradong CR
- Phone: 0999 744 2521
- Phone: 0977 206 8785
- Viber: 0927 437 4428

## Pages already drafted
- `index.html`
- `services.html`
- `service-areas.html`
- `contact.html`

## Dev priorities
1. Keep static site simple and Vercel-ready.
2. Do not create many city pages yet.
3. Improve completeness without overbuilding.
4. Keep copy conversational Taglish and customer-problem-led.
5. Make mobile contact path obvious.
6. Do not add fake ranking, 24/7, licensed, certified, #1, fake reviews, or fake address claims.
7. Keep generated assets labeled as concept until approved.

## Required checks
Run:
```bash
python3 -m unittest tests/test_site_content.py -v
```

Also check:
- all internal links work
- all local images exist
- HTML parses
- JSON files parse
- no placeholder/client-harmful copy remains
- `example.com` is still only temporary until final domain is given

## Blockers before production publish
- final domain missing
- GitHub repo missing
- Vercel project/account missing
- logo/photos not client-approved yet
- real proof photos still needed if available

## Readiness target
Return one label only:
- Draft build ready
- QA in progress
- Production-ready pending founder approval
- Final publish-ready
- Published and verified
