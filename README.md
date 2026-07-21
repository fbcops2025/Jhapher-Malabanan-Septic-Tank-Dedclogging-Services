# Jhapher Malabanan website project

Simple static website draft for Jhapher Malabanan Septic Tank & Declogging Services.

## Current status
Draft build ready for GitHub + Vercel preview setup. Concept assets are not final client-approved brand assets yet.

## Local preview
```bash
python3 -m http.server 4173
```
Then open `http://localhost:4173`.

## Checks
```bash
python3 -m unittest tests/test_site_content.py -v
python3 scripts/check_static_site.py
```
Or, if using npm scripts:
```bash
npm run check
```

## Folders
- `assets/brand/` - logo and brand concepts
- `assets/social-covers/` - Facebook and Google Business Profile cover concepts
- `assets/marketing-photos/` - marketing/social post image concepts
- `research/` - audit and business context
- `content/` - website copy and SEO content
- `qa/` - quality checks before publish
- `scripts/` - local QA utilities
- `tests/` - content checks

## Deployment notes
- Vercel can serve this as a static site; no build command is needed.
- `example.com` is temporary in canonical tags, `sitemap.xml`, and `robots.txt` until the final domain is confirmed.
- Do not deploy final production until GitHub repo, Vercel project, final domain, and founder/client approval are ready.

## Rule
Use generated images as concept assets until founder/client approval. Do not present them as final logo, final brand identity, real service photos, or real customer proof.
