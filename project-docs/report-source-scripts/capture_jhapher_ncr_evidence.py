"""Fresh live capture for Jhapher Malabanan NCR/Rizal proposal evidence.

This is for the new Metro Manila / Rizal / nearby provinces proposal, not the
older Cagayan de Oro portfolio case study.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

OUT = Path(__file__).resolve().parent / "assets" / "Jhapher NCR Evidence"
OUT.mkdir(parents=True, exist_ok=True)

URLS = {
    "current_cdo_home": "https://cdosepticservices.com/",
    "current_cdo_declogging": "https://cdosepticservices.com/services/toilet-declogging",
    "facebook_pasig_page": "https://www.facebook.com/104199985500619/",
    "facebook_jhapher_post_metro": "https://www.facebook.com/100077168727790/posts/jhapher-malabanan-habwasuyop-septic-tank-sipsip-pozo-negro-servicescontact-numbe/775617388353878/",
    "maps_pasig_query": "https://www.google.com/maps/search/Jhapher+Malabanan+Pozo+Negro+Excavating+Septic+Tank+Declogging+Services+Pasig",
    "rose_competitor": "https://rosemalabanansiphoning.com/services/septic-tank-siphoning/",
    "wix_competitor": "https://247malabanan.wixsite.com/malabanan",
    "rtg_competitor": "https://www.malabanansiphoningrtg.com/services",
}


async def dismiss_overlays(page) -> None:
    for sel in [
        'button:has-text("Accept all")',
        'button:has-text("I agree")',
        'button:has-text("Reject all")',
        "#L2AGLb",
        'button:has-text("Not now")',
        'button:has-text("No thanks")',
        'button[aria-label="Close"]',
        '[aria-label="Close"]',
    ]:
        try:
            btn = page.locator(sel).first
            if await btn.count() and await btn.is_visible(timeout=1000):
                await btn.click(timeout=2000)
                await page.wait_for_timeout(700)
        except Exception:
            pass


async def capture(page, key: str, filename: str, *, wait: int = 4500, full_page: bool = False) -> dict:
    url = URLS[key]
    result = {"key": key, "url": url, "file": filename, "status": "ok"}
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=90000)
        await page.wait_for_timeout(wait)
        await dismiss_overlays(page)
        await page.screenshot(path=str(OUT / filename), full_page=full_page)
        print(f"captured {filename}")
    except Exception as exc:  # noqa: BLE001
        result["status"] = f"failed: {type(exc).__name__}: {exc}"
        print(f"failed {filename}: {exc}")
    return result


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()
        results = []
        results.append(await capture(page, "current_cdo_home", "01-current-cdo-homepage.png"))
        results.append(await capture(page, "current_cdo_declogging", "02-current-cdo-declogging-page.png"))
        results.append(await capture(page, "facebook_pasig_page", "03-facebook-pasig-page-attempt.png", wait=5500))
        results.append(await capture(page, "facebook_jhapher_post_metro", "04-facebook-metro-service-area-post-attempt.png", wait=5500))
        results.append(await capture(page, "maps_pasig_query", "05-google-maps-pasig-query.png", wait=7000))
        results.append(await capture(page, "rose_competitor", "06-competitor-rose-service-page.png"))
        results.append(await capture(page, "wix_competitor", "07-competitor-wix-malabanan-page.png"))
        results.append(await capture(page, "rtg_competitor", "08-competitor-rtg-services-page.png"))

        (OUT / "00-capture-log.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        await browser.close()
        print("DONE ->", OUT)


if __name__ == "__main__":
    asyncio.run(main())
