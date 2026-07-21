# Deployment QA Gates

## Gate 1: Facts and claims
Pass only if:
- business name is consistent
- phone numbers match everywhere
- Viber number matches everywhere
- services are correct
- service areas are confirmed or clearly softened
- no fake `#1`, `best`, guaranteed, licensed/certified, or 24/7 claims

Blocker: wrong number, fake claim, unconfirmed service area presented as guaranteed.

## Gate 2: Design and brand
Pass only if:
- homepage looks credible above the fold
- headline, service, trust signal, and CTA are clear
- images do not misrepresent real work
- no placeholder sections remain

## Gate 3: Mobile UX
Pass only if:
- tested at 360, 390, 430, and 768px widths
- no horizontal scrolling
- tap targets are easy
- phone/Viber CTA visible early

## Gate 4: SEO
Pass only if:
- unique title/meta/H1 per page
- sitemap and robots exist
- Open Graph image exists
- no duplicate spam city pages
- schema has no fake reviews or fake address

## Gate 5: Technical
Pass only if:
- clean install works
- build passes
- no console errors on key pages
- links work
- no exposed secrets
- Vercel preview deploy succeeds

## Gate 6: Performance and accessibility
Minimum:
- Lighthouse mobile performance 85+
- Accessibility 95+
- Best Practices 95+
- SEO 95+

## Gate 7: Final review
Before production publish:
- all P0/P1 fixed
- Vercel preview checked
- founder/Topic General approval ready

## Readiness labels
Use only:
- Draft build ready
- QA in progress
- Production-ready pending founder approval
- Final publish-ready
- Published and verified
