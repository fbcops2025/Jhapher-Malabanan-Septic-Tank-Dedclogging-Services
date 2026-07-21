"""
We Forge Web -- Brand Presence Audit + Proposal generator.

Renders a warm, conversational Taglish client report as an editorial/magazine
document, not a generic SaaS deck: a running folio (page number + section
name) on every inner page, a three-act color arc (see brand_kit.py "Editorial
design system" -- cool/restrained diagnosis pages, vivid color-block vision
pages, clean white decision pages), oversized pull-quotes, and full-bleed
evidence photography. Structure follows the value/dream/action proposal
format: quick snapshot, executive verdict, audit findings, the real root
cause, what happens if nothing changes, a "sell the dream" section (sample
Google result, multi-keyword coverage, website dream, optional GBP dream for
local service businesses), real proof from past clients, the build
blueprint, a plain-language technical glossary, the investment value pitch,
pricing, payment terms, and a soft close.

Writing rules enforced throughout (see the source spec doc): Taglish,
conversational, no em dashes, no double hyphens, no fake promises.

This file is a single edit-in-place report for ONE client at a time
(currently PH Gadget Picks). See README.md for how to reuse it for the next
client, including how to configure CLIENT["business_type"] for the GBP
decision logic.

Usage:
    python generate_audit_report.py [--out PATH]

Requires: pip install -r requirements.txt && playwright install chromium
"""

from __future__ import annotations

import argparse
from pathlib import Path

from brand_kit import BASE_CSS, BRAND, CONTACT, LOGO_SVG, TOOL_DIR, asset, build_cover_v2, page_shell, qr_data_uri, render_pdf
from generate_portfolio import CASE_STUDIES

OUTPUT_DIR = TOOL_DIR / "output"


def shell(content: str, **kwargs) -> str:
    kwargs.setdefault("footer_left", "We Forge Web | Built to Be Found. Built to Last.")
    kwargs.setdefault("footer_right", CONTACT["site"])
    return page_shell(content, **kwargs)


# ---------------------------------------------------------------------------
# CLIENT BLOCK -- Jhapher Malabanan NCR website proposal
# ---------------------------------------------------------------------------

# business_type drives the GBP decision logic (see README "GBP business types"):
#   "physical_location" -> customers visit a real address. GBP dream page shows the address.
#   "service_area"       -> business travels to the customer. GBP dream page hides the address,
#                            shows service areas instead.
#   "hybrid"              -> has an address AND serves nearby areas. GBP dream page shows both.
#   "online_only"         -> no physical customer-facing location or local service area
#                            (affiliate, media, SaaS, ecommerce with no showroom). GBP dream page
#                            is skipped entirely, not just downplayed.
CLIENT = {
    "business_name": "Jhapher Malabanan Septic Tank & Declogging Services",
    "domain": "NCR Website Proposal | Call 0999 744 2521 | 0977 206 8785 | Viber 0927 437 4428",
    # Future-owned domain placeholder, used only in the sample Google result.
    "dream_domain": "jhaphermalabanan-ncr.com",
    "date": "July 18, 2026",
    "business_type": "service_area",
    "skip_gbp": True,
    "city": "Pasig City main branch / center area, serving NCR, Rizal, nearby provinces, CDO, and Misamis Occidental",
    "service_areas_display": "Main branch / center area: Pasig City. Service areas: Metro Manila/NCR including Makati, Taguig, Mandaluyong, Greenhills, Quezon City, Caloocan, Pasig City, Marikina City, and Las Pinas; nearby provinces Bulacan, Cavite, Laguna, Cagayan de Oro, and Misamis Occidental; Rizal areas including Antipolo City, Taytay, Cainta, Angono, Binangonan, Cardona, Morong, Baras, Teresa, Tanay, Pililla, San Mateo, and Montalban",
    "service_keyword": "Septic tank siphoning and declogging",
    "search_query": "septic tank siphoning Metro Manila",
    "meta_title": "Jhapher Malabanan NCR - Septic Tank Siphoning & Declogging Services",
    "meta_desc": "Septic tank siphoning, pozo negro cleaning, and declogging services for Metro Manila, Rizal, Cavite, Laguna, and nearby areas. Clear service areas, proof, and fast contact path.",
    "sitelinks": ["Septic Siphoning", "Declogging", "Service Areas", "Book Service"],
    "reference": "Separate NCR website proposal, Facebook public proof, and competitor benchmarks",
}

STATUS_CARDS = [
    {"label": "Current status", "title": "May proof at demand na", "body": "May public Facebook proof at malinaw ang services: septic siphoning, pozo negro, at declogging.", "tone": "teal"},
    {"label": "Main gap", "title": "Kailangan ng NCR website", "body": "Separate ang NCR service area, kaya kailangan ng sariling website foundation na hindi CDO-focused.", "tone": "orange"},
    {"label": "Best next move", "title": "Website-first proposal", "body": "Mobile-first site, service pages, area pages, proof gallery, at mabilis na booking/contact path.", "tone": "muted"},
]

EXEC_VERDICT = (
    "Malinaw ang opportunity ng Jhapher Malabanan Septic Tank & Declogging Services para sa NCR at "
    "nearby service areas. May public proof na sa Facebook at malinaw ang services, pero kailangan "
    "ng sariling NCR website foundation para hindi malito ang customer sa ibang area, competitor page, "
    "o social-only proof. Kaya ang recommended next step namin ay Website Foundation + Service Area Pages."
)

EXEC_VERDICT_2 = (
    "Hindi ito tungkol sa hype. Ang goal nito ay gawing mas madaling makita, maintindihan, "
    "pagkatiwalaan, at kontakin ang business kapag may urgent septic tank, pozo negro, o baradong "
    "linya problem ang customer."
)

EXEC_INTRO = (
    "Ang proposal na ito ay ginawa para makita ninyo kung ano ang problema, bakit ito importante, "
    "paano namin ito aayusin, at pinaka importante, ano talaga ang makikita niyo kapag tumuloy tayo."
)

OPPORTUNITY_INTRO = (
    "May malinaw na demand ang septic at declogging services sa Metro Manila, Rizal, Cavite, Laguna, "
    "at Bulacan dahil urgent ang customer need. Kapag barado ang CR, puno ang septic tank, o kailangan "
    "ng pozo negro service, gusto ng customer makita agad kung available kayo sa area nila at paano "
    "tumawag."
)

RECOMMENDED_PATH = {
    "name": "Website Foundation + Service Area Pages",
    "body": (
        "Isang polished, mobile first na website ang magbibigay sa Jhapher Malabanan NCR ng malinaw "
        "na homepage, service pages, service-area structure, proof section, booking CTA, at basic SEO "
        "foundation. Ito ang official hub para sa NCR customers, hiwalay at mas malinaw kaysa umasa "
        "lang sa Facebook posts."
    ),
}

BENEFITS = [
    "Magkakaroon kayo ng professional NCR website hub, hindi lang Facebook post ang unang hahawakan ng customer.",
    "Mas malinaw ang services: septic tank siphoning, pozo negro cleaning, at declogging.",
    "Mas madaling makita ang served areas, kasama ang Pasig as center area, NCR, Rizal, Bulacan, Cavite, Laguna, Cagayan de Oro, at Misamis Occidental.",
    "Mas mabilis ang contact path: call, message, at book service.",
    "Mas handa ang website para sa Google Search at future service-area content.",
    "Mas mababawasan ang confusion sa ibang Malabanan pages dahil consistent ang brand, phone, at location coverage.",
]

BOUNDARIES = [
    "Walang guaranteed na number one sa Google.",
    "Walang guarantee na calls, leads, traffic, o immediate ranking. Gusto naming totoo ang inaasahan niyo.",
    "Walang fake reviews, gawa gawang project photos, o unverified license claims.",
    "Website-first ang proposal na ito: build, content structure, proof section, and launch readiness.",
]

AUDIT_FINDINGS = [
    {"area": "Facebook proof", "status": "Found", "tone": "teal", "impact": "May public post na nagpapakita ng septic/pozo negro services at phone.", "reco": "Gamitin bilang support proof, pero hindi ito dapat ang only hub."},
    {"area": "NCR website", "status": "Missing", "tone": "orange", "impact": "Separate ang NCR service, pero wala pang dedicated website path na nakita.", "reco": "Gumawa ng mobile-first NCR website foundation."},
    {"area": "Service areas", "status": "Confirmed by founder", "tone": "teal", "impact": "Malawak ang coverage, kailangan lang ayusin ang structure para hindi magmukhang kalat.", "reco": "Gumamit ng hub pages para sa Metro Manila, Rizal, at nearby provinces."},
    {"area": "Competitors", "status": "Active", "tone": "orange", "impact": "May competitors na may service pages at broad coverage messaging.", "reco": "Gumawa ng mas malinaw, mas trusted, at mas direct na website."},
    {"area": "Website scope", "status": "Focused", "tone": "teal", "impact": "Confirmed na website ang current priority, not a listing cleanup project.", "reco": "Keep the proposal centered on the NCR website foundation."},
    {"area": "Project proof", "status": "Allowed", "tone": "teal", "impact": "Pwede gamitin ang Facebook screenshots/video stills sa final PDF.", "reco": "Ilagay sa proof section with honest source labels."},
]

# Open questions from the audit that need the owner's confirmation before final
# delivery. Empty by default (nothing to show). Fill in per client -- this is
# what keeps the report honest about what was verified by live observation
# versus what still needs a human answer.
NEEDS_CONFIRMATION: list[str] = [
    "Final logo or brand asset for the separate NCR website.",
    "Final website domain name, if already purchased.",
    "Confirm if 0999 744 2521 is the main call number, 0977 206 8785 is secondary, and 0927 437 4428 is Viber-only or also a regular call/SMS number.",
]

# Real screenshots from the live audit, shown as evidence on their own page(s)
# instead of just described in the findings table. Each item needs "file"
# (path inside assets/), "label", and "caption". "fit" is "cover-top" (for
# very tall full-page screenshots, crops to the top) or "contain" (shows the
# whole image, for landscape-ish screenshots like Maps or Facebook). Empty by
# default -- only clients with real audit screenshots get an evidence page.
EVIDENCE_LARGE: list[dict] = [
    {
        "file": "Jhapher NCR Evidence/04-facebook-metro-service-area-post-attempt.png",
        "label": "Public service proof from Facebook",
        "caption": (
            "A public Facebook post shows septic tank, pozo negro, and cleaning services with contact "
            "numbers. Good proof exists, but it needs a cleaner website hub for NCR customers."
        ),
        "fit": "contain",
        "height_mm": 78,
    },
]
EVIDENCE_PAIRED: list[dict] = [
    {
        "file": "Jhapher NCR Evidence/03-facebook-pasig-page-attempt.png",
        "label": "Facebook is useful, but gated",
        "caption": (
            "The Facebook page is partly visible but login-gated. Customers should not need Facebook "
            "login just to understand services, areas, and contact details."
        ),
        "fit": "contain",
        "height_mm": 40,
    },
]

OPPORTUNITY_EVIDENCE_LARGE: list[dict] = [
    {
        "file": "Jhapher NCR Evidence/06-competitor-rose-service-page.png",
        "label": "Competitors already structure septic service pages",
        "caption": (
            "Competitor pages already explain septic tank siphoning services with visible phone numbers "
            "and service messaging. Jhapher NCR needs a cleaner, dedicated version."
        ),
        "fit": "contain",
        "height_mm": 78,
    },
]
OPPORTUNITY_EVIDENCE_PAIRED: list[dict] = [
    {
        "file": "Jhapher NCR Evidence/07-competitor-wix-malabanan-page.png",
        "label": "Broad-area competitors are visible",
        "caption": (
            "Other Malabanan pages are already presenting services and broad coverage online. This raises "
            "the trust bar for customers comparing providers."
        ),
        "fit": "contain",
        "height_mm": 40,
    },
    {
        "file": "Jhapher NCR Evidence/08-competitor-rtg-services-page.png",
        "label": "Service pages are the competitive baseline",
        "caption": (
            "Competitors list service types like septic tank siphoning, manual cleaning, and declogging. "
            "Jhapher's NCR website should answer these same urgent intents better."
        ),
        "fit": "contain",
        "height_mm": 40,
    },
]

ROOT_CAUSE_LEAD = "Ang issue ay hindi kakulangan ng proof."
ROOT_CAUSE_STATEMENT = (
    "May public proof na, pero wala pang malinaw na NCR website hub kung saan madaling makita ng "
    "customer ang services, service areas, proof, at booking path."
)
ROOT_CAUSE_BODY = (
    "Dahil separate ang NCR service, hindi dapat umasa sa CDO-focused website o Facebook posts lang. "
    "Kapag may sariling NCR website, mas malinaw ang coverage, mas direct ang tawag, at mas madaling "
    "ikumpara ang Jhapher laban sa ibang Malabanan competitors."
)

RISK_INTRO = "Kung walang mababago, narito ang mangyayari."
RISKS = [
    "Mananatiling Facebook-first ang customer journey.",
    "Pwedeng malito ang NCR customers sa CDO/Mindanao website positioning.",
    "Hindi malinaw agad kung aling areas ang served.",
    "Mas mauuna ang competitors na may service pages at area pages.",
    "Mawawala ang urgent customers na gusto lang tumawag agad.",
    "Hindi masusulit ang demand sa septic siphoning, pozo negro, at declogging searches.",
]
RISK_CLOSER = (
    "Hindi ibig sabihin nito na late na. Ibig sabihin lang, ito ang tamang oras para ayusin ang "
    "foundation bago pa lumaki ang effort sa marketing."
)

# One concrete, representative buyer moment, not a testimonial or a review, just a
# plain "here's who actually searches for this" illustration. Keep it to ONE scenario,
# not three, picked for whichever search behavior is most common for this client's
# real inquiries. Always closes with a "sample direction" disclaimer, same rule as the
# dream pages below.
SCENARIO = {
    "title": "Ang urgent septic customer",
    "story": (
        "Isipin natin. May homeowner o restaurant owner sa Pasig, Makati, o Antipolo na barado ang CR "
        "o puno ang septic tank. Urgent ito, kaya ang hinahanap nila ay mabilis kausap, malinaw ang "
        "service area, at may proof na marunong talaga sa trabaho."
    ),
    "today": (
        "Makakakita sila ng Facebook proof at ibang competitor pages, pero wala pang dedicated NCR "
        "website na mabilis magpakita ng services, areas, proof, at tawag button."
    ),
    "after": (
        "Makikita nila ang NCR service page, phone number, service-area list, proof section, at booking "
        "steps. Mas madali silang tumawag agad."
    ),
    "search_query": "septic tank siphoning Pasig",
}

DREAM_INTRO = (
    "I imagine natin. May naghahanap ng septic tank siphoning o declogging sa Metro Manila o Rizal. "
    "Sa halip na malito sa maraming Malabanan pages, may malinaw na NCR website result na nagpapakita "
    "ng services, coverage, at contact path."
)
DREAM_BOUNDARY = (
    "Ito ay direction at visibility strategy, hindi guaranteed ranking promise. Maraming factor ang "
    "nakakaapekto sa Google placement, pero kailangan munang tama ang pages, structure, at trust "
    "foundation ng website bago ito makipag compete."
)

SERP_FIELDS = [
    ("Search example", f'"{CLIENT["search_query"]}"'),
    ("Possible result direction", CLIENT["meta_title"]),
    ("Sample description", CLIENT["meta_desc"]),
    ("Suggested page links", ", ".join(CLIENT["sitelinks"])),
]

KEYWORD_DOORS = [
    ("septic tank siphoning Metro Manila", "Metro Manila Service Hub"),
    ("baradong CR Pasig", "Declogging Page"),
    ("pozo negro cleaning Quezon City", "Pozo Negro Page"),
    ("septic tank service Antipolo", "Rizal Service Hub"),
    ("Malabanan septic tank Makati", "NCR Booking Page"),
]
KEYWORD_DOORS_INTRO = (
    "Hindi lang isang keyword ang magiging daan papunta sa inyo. Bawat importanteng page ay maaaring "
    "maging sariling entry point."
)
KEYWORD_DOORS_QUOTE = "Iba-ibang tanong, magkakaibang pinto, pero <span class=\"accent\">iisang</span> brand sa bawat sagot."
KEYWORD_DOORS_CLOSER = (
    "Ang goal ay itigil ang pag asa sa iisang page lang. Iba ibang customer, iba ibang tanong, iba "
    "ibang page ang sasagot, pero lahat babalik sa isang malinaw at kapani paniwalang brand."
)

WEBSITE_DREAM_INTRO = "Kapag binisita ng customer ang website ninyo, dapat malinaw agad."
WEBSITE_DREAM_QUESTIONS = [
    "Available ba kayo sa area ko?",
    "Septic siphoning ba ito, declogging, o pozo negro cleaning?",
    "Paano tumawag o mag-book agad?",
    "May proof ba ng field work?",
    "Ano ang kailangan kong ihanda bago dumating ang team?",
]

TRUST_PAGES = [
    ("Services", "Septic tank siphoning, pozo negro cleaning, at declogging."),
    ("Service Areas", "Pasig City as center area, NCR, Rizal, Bulacan, Cavite, Laguna, Cagayan de Oro, Misamis Occidental, at listed cities."),
    ("Proof", "Approved Facebook screenshots or field-work visuals with honest labels."),
    ("Book Service", "Phone number, message path, and what details to send before service."),
]

PROOF_INTRO = (
    "We Forge Web ay tumutulong sa Philippine service businesses na maging Google ready ang brand "
    "presence nila, based sa Davao City pero nationwide ang saklaw. Hindi ito ang unang beses naming "
    "gawin ito. Iba ibang negosyo, iba ibang industriya, pero parehong goal: ayusin ang online "
    "presence para mas malinaw, mas searchable, at mas madaling pagkatiwalaan."
)
PROOF_NOTE = "Buong company portfolio, kasama ang lahat ng project, available bilang hiwalay na attachment o sa kahilingan."
PROOF_CASE_SLUGS = ["Jhapher Malabanan Septic Services", "Jeff Lipa Construction Services", "Rose Malabanan Siphoning Septic Tank Services"]

BLUEPRINT = {
    "goal": (
        "Gagawa kami ng professional, mobile first na NCR website na magpapaliwanag ng septic, "
        "pozo negro, at declogging services, magpapakita ng approved proof, at gagabay sa customers "
        "papunta sa mabilis na tawag o booking. Simple ang goal: mas madaling makita, maintindihan, "
        "pagkatiwalaan, at kontakin."
    ),
    "phases": [
        {
            "tag": "P0",
            "title": "Confirm and build the foundation",
            "items": [
                "Gagamitin ang confirmed business name, phone number, at served areas.",
                "Gagawa ng mobile first homepage para sa Jhapher Malabanan NCR service.",
                "Idadagdag ang clear service pages para sa septic siphoning, pozo negro cleaning, at declogging.",
                "Gagawa ng proof section gamit ang approved Facebook screenshots o field visuals.",
                "Ihahanda ang SEO title/meta patterns, sitemap, robots, at Search Console setup.",
            ],
        },
        {
            "tag": "P1",
            "title": "Organize service areas",
            "items": [
                "Gagawa ng service-area structure for Pasig center area, NCR, Rizal, nearby provinces, Cagayan de Oro, at Misamis Occidental.",
                "Iha-highlight ang Makati, Taguig, Pasig, Quezon City, Antipolo, Cainta, Taytay, at other listed areas.",
                "Maglalagay ng FAQ content para sa urgent calls, access, scheduling, at service preparation.",
                "Ihahanda ang internal links para hindi manipis o spammy ang city pages.",
            ],
        },
        {
            "tag": "P2",
            "title": "Later optimization",
            "items": [
                "Magdagdag ng completed-job photos kapag may owner-approved assets.",
                "Magdagdag ng city/service pages kung may enough real detail for each area.",
                "Magdagdag ng maintenance tips at emergency-prep guides para sa future SEO content.",
            ],
        },
    ],
}

TECH_GLOSSARY = [
    ("Sitemap", "Listahan ng mahahalagang pages sa website na tumutulong sa Google malaman kung ano ang dapat i-check."),
    ("Robots file", "Simpleng instruction file na nagsasabi sa search engines kung anong public pages ang pwede nilang bisitahin."),
    ("Canonical link", "Ang opisyal na version ng isang page link, para hindi malito ang Google sa magkaparehong pages."),
    ("Metadata", "Ang title at description na tumutulong ipaliwanag ang bawat page sa Google."),
    ("Schema", "Karagdagang labels sa likod ng website na tumutulong sa search engines maintindihan ang business, services, FAQs, at contact details."),
    ("Search Console", "Google tool na ginagamit para i-submit at bantayan ang website pagkatapos mag launch."),
]

INVESTMENT_VALUE_INTRO = "Hindi lang kayo nagbabayad para sa pages o design lang."
INVESTMENT_VALUE_LEAD = "Ito ay investment sa:"
INVESTMENT_VALUE_ITEMS = [
    "Propesyonal na NCR service website",
    "Mas malinaw na service message",
    "Mas mabilis na call or booking path",
    "Google ready na page structure",
    "Mas matibay na trust foundation",
    "Mas organisadong service-area coverage",
    "Website na pwedeng i-share sa Facebook at customers",
    "Foundation para sa future SEO, ads, and service-area content",
]
INVESTMENT_VALUE_CLOSER = (
    "Kapag may customer na may septic or declogging emergency, hindi sapat na makita lang ang phone "
    "number. Kailangan nilang maintindihan kung anong service ang offer ninyo, available ba kayo sa "
    "area nila, at bakit kayo ang dapat tawagan."
)

PRICING_INTRO = (
    "Sadyang focused ang rekomendasyon namin. Hindi kailangan ng bloated launch. Kailangan ay "
    "isang credible website foundation: service pages, service-area structure, contact path, at "
    "proof section."
)

PRICING_TIERS = [
    {
        "name": "Visibility Review",
        "price": "Complimentary",
        "timeline": "Delivered",
        "badge": None,
        "items": [
            "Brand presence audit at priority action list.",
            "Paliwanag sa simpleng salita kung ano ang gumagana at ano ang humahadlang sa growth.",
        ],
    },
    {
        "name": "Standard Project Value",
        "price": "PHP 30,000",
        "timeline": "Normal WFW rate",
        "badge": None,
        "items": [
            "Base website foundation: PHP 18,000.",
            "Strategic service-area and SEO-ready structure: PHP 7,500.",
            "Basic logo cleanup + website cover graphic: PHP 4,500.",
            "This is the normal value for this scope before the approved discount.",
        ],
    },
    {
        "name": "Founder-Supported Website Foundation Rate",
        "price": "PHP 14,800",
        "price_note": "Approved strategic support rate from PHP 30,000 standard value. WFW support: PHP 15,200.",
        "timeline": "~14 working days",
        "badge": "RECOMMENDED",
        "items": [
            "Premium homepage at clear service positioning.",
            "Core service pages for septic siphoning, pozo negro, and declogging.",
            "Service-area section for Pasig center area, NCR, Rizal, Bulacan, Cavite, Laguna, Cagayan de Oro, and Misamis Occidental.",
            "Basic SEO ready title/meta structure, sitemap/robots, at launch guidance.",
            "Call, message, and booking CTA placement.",
            "2 substantive revision rounds pagkatapos ng unang usable scaffold.",
            "14 day post launch bugfix support para sa delivered scope.",
        ],
    },
    {
        "name": "Foundation + Local Service Pages",
        "price": "Future upgrade",
        "timeline": "~21 working days",
        "badge": None,
        "items": [
            "Lahat ng nasa Foundation.",
            "Deeper city/service pages for high-priority areas.",
            "Expanded FAQ and emergency-prep content.",
            "More proof/gallery sections kapag may approved assets.",
        ],
    },
    {
        "name": "Care & Updates",
        "price": "PHP 1,800 / month",
        "timeline": "Monthly after launch",
        "badge": None,
        "items": [
            "Basic care and update support after launch.",
            "Minor page/content updates within agreed monthly scope.",
            "Content refreshes kapag may bagong photos, proof, or offers.",
        ],
    },
]

# Priced separately from the packages above -- extras a client can add on top
# of whichever tier they pick, not full standalone packages.
ADDONS = [
    ("Basic logo cleanup + website cover graphic", "Included in founder-supported rate", "Standard value: PHP 4,500"),
    ("Marketing Images for posting", "PHP 850 each", None),
    ("Additional service pages beyond the bundled set", "Pricing upon request", None),
]

PAYMENT = {
    "total": "PHP 14,800",
    "standard_value": "PHP 30,000",
    "discount_savings": "PHP 15,200",
    "downpayment": "PHP 10,000 deposit received",
    "balance": "PHP 4,800",
    "included": [
        "Premium NCR website foundation for Jhapher Malabanan Septic Tank & Declogging Services.",
        "Core page structure, service sections, service-area section, proof section, and launch readiness setup.",
        "Standard WFW value: PHP 30,000. Approved founder-supported project rate: PHP 14,800.",
        "Call/message/booking CTA placement using 0999 744 2521, 0977 206 8785, and Viber 0927 437 4428.",
        "Dalawang substantive revision rounds pagkatapos ng unang usable scaffold.",
        "Labing apat na araw na post launch bugfix support para sa delivered scope.",
    ],
    "not_included": [
        "Paid ads, ad budget, o ad campaign management.",
        "Unlimited revisions o trabahong labas sa agreed scope.",
        "Guaranteed na rankings, calls, leads, o instant Google results.",
        "Photography, legal registration checks, permits, o unverified warranty claims.",
    ],
    "accounts": [
        ("GCash", "0970 251 2809"),
        ("GoTyme Bank", "0111 4554 4110"),
        ("MariBank", "1315 9252 920"),
    ],
    "terms_url": "https://weforgeweb.com/terms-and-conditions",
    "next_steps": [
        "Confirmed founder-supported project rate: PHP 14,800 from PHP 30,000 standard project value.",
        "PHP 10,000 deposit received.",
        "Settle remaining PHP 4,800 before launch / final handover.",
        "Monthly care/update support: PHP 1,800 per month after launch, subject to final scope confirmation.",
        "Ipadala ang final logo/domain details kung meron, plus approved project photos kung available.",
        "Sisimulan na namin ang build.",
        "Ipapadala ang unang working version para sa review niyo.",
    ],
}

SOFT_CLOSE = (
    "Kapag ready na kayo, simple lang ang next step. I-confirm natin ang recommended package, "
    "i-finalize ang scope at pricing, settle ang downpayment, at sisimulan na namin ang build."
)
SOFT_CLOSE_2 = (
    "Hindi ito tungkol sa hype. Ito ay tungkol sa pagbibigay sa business ninyo ng mas professional na "
    "online foundation, isang presence na mas madaling makita, maintindihan, pagkatiwalaan, at kontakin "
    "ng customers."
)
SOFT_CLOSE_3 = "Kasama namin kayo sa bawat hakbang."

# ---------------------------------------------------------------------------
# Icons -- small inline SVGs, no external icon library.
# ---------------------------------------------------------------------------

ICON_SEARCH = '<svg viewBox="0 0 24 24" class="ic"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><line x1="21" y1="21" x2="16.2" y2="16.2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" class="ic"><line x1="4" y1="12" x2="20" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><polyline points="14 6 20 12 14 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" class="ic"><polyline points="4 13 9 18 20 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_STAR = '<svg viewBox="0 0 24 24" class="ic"><polygon points="12 2 15 9 22 9.5 16.5 14 18.5 21 12 17 5.5 21 7.5 14 2 9.5 9 9" fill="currentColor"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" class="ic"><path d="M12 22s7-7.4 7-12.5A7 7 0 1 0 5 9.5C5 14.6 12 22 12 22z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="9.5" r="2.3" fill="currentColor"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1.1-.2 1.2.4 2.4.6 3.7.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.9 21 3 13.1 3 3.9c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.7.1.4 0 .8-.2 1.1L6.6 10.8z" fill="#fff"/></svg>'

# Generic, reusable across every client. Frames the same four outcomes any
# business gets from a proper brand presence foundation, no client-specific
# claims, so this needs no per-client edits. The icon slot is unused by the
# current mag-cover rendering (numbered 01-04 instead), kept for structural
# parity with older covers and in case a future layout wants it back.
COVER_BENEFITS = [
    (ICON_SEARCH, "Mas Madaling Mahanap", "Visibility sa Google Search at Maps."),
    (ICON_CHECK, "Mas Madaling Pagkatiwalaan", "Mas malakas na trust mula sa unang impression."),
    (ICON_PIN, "Mas Madaling Kontakin", "Consistent na details, isang click lang makaka-connect."),
    (ICON_ARROW, "Mas Malaking Oportunidad", "Mas handa ang brand para sa susunod na inquiry at project."),
]

# ---------------------------------------------------------------------------
# Page-specific CSS (on top of brand_kit.BASE_CSS). Act backgrounds, the
# folio, and the pull-quote component live in brand_kit.py since they're
# generic; everything below is specific to this document's components.
# ---------------------------------------------------------------------------

EXTRA_CSS = f"""
.ic {{ width: 12px; height: 12px; display: inline-block; vertical-align: -1.5px; }}

/* ---------- formal cover: taller band + prepared for/by panel ---------- */
.cover-band-tall {{ height: 138mm; }}
.prepared-panel {{
  display: flex; gap: 0; margin-top: 4mm;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.16);
  border-radius: 12px; padding: 5mm 6mm;
}}
.prepared-panel .col {{ flex: 1; padding: 0 6mm; border-left: 1px solid rgba(255,255,255,0.14); }}
.prepared-panel .col:first-child {{ padding-left: 0; border-left: none; }}
.prepared-panel .col.narrow {{ flex: 0 0 34mm; }}
.prepared-panel .k {{ font-family: 'JetBrains Mono', monospace; font-size: 8px; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(244,241,234,0.55); }}
.prepared-panel .v-name {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 12.5px; color: #fff; margin-top: 1.5mm; }}
.prepared-panel .v-sub {{ font-size: 9px; color: rgba(244,241,234,0.7); margin-top: 1mm; line-height: 1.5; }}
.cover-issue-line {{ font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(244,241,234,0.55); margin-top: 3mm; padding-top: 3mm; border-top: 1px solid rgba(255,255,255,0.16); }}

/* ---------- status cards ---------- */
.status-cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; margin: 8mm 0; }}
.status-card {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-left: 3px solid {BRAND['teal']}; border-radius: 10px; padding: 6mm; }}
.status-card.tone-orange {{ border-left-color: {BRAND['orange']}; }}
.status-card.tone-muted {{ border-left-color: {BRAND['muted']}; }}
.status-card .label {{ font-family: 'JetBrains Mono', monospace; font-size: 8px; text-transform: uppercase; letter-spacing: 0.1em; color: {BRAND['muted']}; }}
.status-card .title {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 14px; margin: 2mm 0; color: {BRAND['ink']}; }}
.status-card p {{ font-size: 9.5px; line-height: 1.5; color: {BRAND['muted']}; }}

/* ---------- callout boxes ---------- */
.callout {{ border-radius: 12px; padding: 6mm 7mm; border-left: 3px solid {BRAND['orange']}; background: {BRAND['card_peach']}; margin: 4mm 0; }}
.callout h4 {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 12.5px; margin-bottom: 2mm; color: {BRAND['ink']}; }}
.callout p {{ font-size: 10.5px; line-height: 1.6; color: {BRAND['ink']}; }}
.callout p + p {{ margin-top: 2.5mm; }}
.callout.teal {{ border-left-color: {BRAND['teal']}; background: {BRAND['card_mint']}; }}

.body-text {{ font-size: 11px; line-height: 1.7; color: {BRAND['muted']}; max-width: 165mm; }}
.body-text + .body-text {{ margin-top: 3mm; }}

/* ---------- section opener (bigger, editorial headline treatment) ---------- */
.opener-title {{ font-size: 30px; line-height: 1.12; margin-top: 4mm; max-width: 160mm; }}

/* ---------- checklist ---------- */
.checklist {{ display: flex; flex-direction: column; gap: 2.5mm; margin-top: 3mm; }}
.checklist li {{ list-style: none; display: flex; gap: 3mm; font-size: 10.5px; line-height: 1.55; color: {BRAND['ink']}; }}
.checklist .dot {{ flex-shrink: 0; width: 5mm; height: 5mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 0.5mm; }}
.checklist.good .dot {{ background: {BRAND['card_mint']}; color: {BRAND['teal']}; }}
.checklist.warn .dot {{ background: {BRAND['card_peach']}; color: {BRAND['orange_dark']}; font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: 700; }}

/* ---------- numbered step list ---------- */
.num-list {{ display: flex; flex-direction: column; gap: 3mm; margin-top: 4mm; counter-reset: step; }}
.num-list li {{ list-style: none; display: flex; gap: 3.5mm; align-items: baseline; font-size: 10.5px; color: {BRAND['ink']}; }}
.num-list li::before {{ counter-increment: step; content: counter(step); flex-shrink: 0; width: 5.5mm; height: 5.5mm; border-radius: 50%; background: {BRAND['teal']}; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: 700; display: flex; align-items: center; justify-content: center; }}

/* ---------- findings table ---------- */
.findings-table {{ width: 100%; border-collapse: collapse; margin-top: 4mm; font-size: 9.5px; }}
.findings-table th {{ background: {BRAND['teal']}; color: #fff; text-align: left; padding: 3mm 3.5mm; font-family: 'JetBrains Mono', monospace; font-size: 8px; text-transform: uppercase; letter-spacing: 0.06em; }}
.findings-table td {{ padding: 3.5mm; border-bottom: 1px solid rgba(24,53,43,0.08); vertical-align: top; color: {BRAND['ink']}; }}
.findings-table tr:nth-child(even) td {{ background: rgba(23,107,80,0.04); }}
.status-pill {{ display: inline-block; padding: 1.5mm 2.5mm; border-radius: 999px; font-size: 8px; font-weight: 700; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; }}
.status-pill.teal {{ background: {BRAND['card_mint']}; color: {BRAND['teal']}; }}
.status-pill.orange {{ background: {BRAND['card_peach']}; color: {BRAND['orange_dark']}; }}
.status-pill.muted {{ background: #e4e7e2; color: {BRAND['muted']}; }}

/* ---------- root cause statement ---------- */
.root-cause-box {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 14px; padding: 8mm 9mm; margin: 5mm 0; }}
.root-cause-box .lead {{ font-size: 10.5px; color: {BRAND['muted']}; }}

/* ---------- live evidence: full-bleed photo spread ---------- */
.evidence-bleed {{ flex-shrink: 0; overflow: hidden; background: #e9e5dc; }}
.evidence-bleed img {{ width: 100%; height: 100%; display: block; }}
.evidence-bleed.cover-top img {{ object-fit: cover; object-position: top; }}
.evidence-bleed.contain img {{ object-fit: contain; }}
.evidence-cap {{ padding: 4mm 18mm 6mm; flex-shrink: 0; border-bottom: 1px solid rgba(24,53,43,0.08); }}
.evidence-cap .label {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 11.5px; color: {BRAND['teal']}; }}
.evidence-cap p {{ font-size: 9.5px; line-height: 1.5; color: {BRAND['muted']}; margin-top: 1.5mm; font-style: italic; }}
.evidence-card {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 14px; overflow: hidden; box-shadow: 0 10px 26px rgba(24,53,43,0.05); }}
.evidence-card .img-wrap {{ background: #f2efe8; overflow: hidden; }}
.evidence-card .img-wrap img {{ width: 100%; height: 100%; display: block; }}
.evidence-card.cover-top .img-wrap img {{ object-fit: cover; object-position: top; }}
.evidence-card.contain .img-wrap img {{ object-fit: contain; padding: 3mm; }}
.evidence-card .cap {{ padding: 4mm 5.5mm; }}
.evidence-card .cap .label {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 11.5px; color: {BRAND['teal']}; }}
.evidence-card .cap p {{ font-size: 9.5px; line-height: 1.55; color: {BRAND['muted']}; margin-top: 1.5mm; }}
.evidence-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }}

/* ---------- glossary table ---------- */
.term-table {{ width: 100%; border-collapse: collapse; margin-top: 4mm; }}
.term-table td {{ padding: 4mm; border-bottom: 1px solid rgba(24,53,43,0.08); font-size: 10px; vertical-align: top; }}
.term-table td:first-child {{ width: 42mm; font-family: 'Manrope', sans-serif; font-weight: 800; color: {BRAND['teal']}; }}
.term-table td:last-child {{ color: {BRAND['ink']}; line-height: 1.55; }}

/* ---------- SERP / dream mockups ---------- */
.mock-label {{ font-size: 9.5px; color: {BRAND['muted']}; margin-top: 3mm; font-style: italic; line-height: 1.5; }}
.serp-card {{ background: #fff; border: 1px solid rgba(24,53,43,0.1); border-radius: 14px; padding: 6mm; box-shadow: 0 14px 40px rgba(24,53,43,0.08); }}
.serp-bar {{ display: flex; align-items: center; gap: 2.5mm; background: {BRAND['mint']}; border-radius: 999px; padding: 3mm 4mm; font-size: 10.5px; color: {BRAND['ink']}; margin-bottom: 6mm; }}
.serp-bar .ic {{ color: {BRAND['teal']}; width: 13px; height: 13px; }}
.serp-result {{ padding-left: 1mm; }}
.serp-favicon {{ width: 16px; height: 16px; border-radius: 4px; background: {BRAND['teal']}; display: inline-flex; align-items: center; justify-content: center; vertical-align: -3px; margin-right: 2mm; }}
.serp-url {{ font-size: 10px; color: {BRAND['ink']}; opacity: 0.65; }}
.serp-title {{ font-family: 'Manrope', sans-serif; font-weight: 700; font-size: 15px; color: {BRAND['teal']}; margin: 1.5mm 0; }}
.serp-desc {{ font-size: 10px; line-height: 1.6; color: {BRAND['muted']}; max-width: 150mm; }}
.serp-sitelinks {{ display: flex; flex-wrap: wrap; gap: 3mm; margin-top: 4mm; padding-top: 4mm; border-top: 1px solid rgba(24,53,43,0.08); }}
.serp-sitelinks span {{ font-size: 9.5px; color: {BRAND['teal']}; font-weight: 600; }}

.field-list {{ margin-top: 5mm; display: flex; flex-direction: column; gap: 2mm; }}
.field-list .row {{ display: flex; gap: 4mm; font-size: 9.5px; }}
.field-list .k {{ width: 48mm; flex-shrink: 0; font-family: 'JetBrains Mono', monospace; color: {BRAND['muted']}; text-transform: uppercase; letter-spacing: 0.04em; font-size: 8.5px; padding-top: 0.5mm; }}
.field-list .v {{ color: {BRAND['ink']}; line-height: 1.5; }}

/* ---------- keyword doors ---------- */
.keyword-rows {{ display: flex; flex-direction: column; gap: 3mm; margin-top: 6mm; }}
.keyword-row {{ display: flex; align-items: center; gap: 4mm; background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 12px; padding: 4mm 5mm; box-shadow: 0 10px 24px rgba(7,9,8,0.15); }}
.keyword-row .q {{ display: flex; align-items: center; gap: 2.5mm; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: {BRAND['ink']}; flex: 1; }}
.keyword-row .q .ic {{ color: {BRAND['muted']}; }}
.keyword-row .arrow {{ color: {BRAND['muted']}; flex-shrink: 0; }}
.keyword-row .dest {{ flex-shrink: 0; }}

/* ---------- trust page strip ---------- */
.trust-strip {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin-top: 5mm; }}
.trust-pill {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 12px; padding: 5mm; text-align: left; }}
.trust-pill .name {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 11.5px; color: {BRAND['teal']}; }}
.trust-pill p {{ font-size: 9px; line-height: 1.5; color: {BRAND['muted']}; margin-top: 1.5mm; }}

/* ---------- GBP dream card (local service clients only) ---------- */
.gbp-card {{ background: #fff; border: 1px solid rgba(24,53,43,0.1); border-radius: 14px; padding: 6mm; box-shadow: 0 14px 40px rgba(7,9,8,0.18); }}
.gbp-top {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.gbp-name {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 15px; color: {BRAND['ink']}; }}
.gbp-stars {{ color: {BRAND['orange']}; margin-top: 1.5mm; font-size: 10px; }}
.gbp-photos {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.5mm; margin: 4mm 0; }}
.gbp-photos div {{ height: 16mm; border-radius: 8px; background: linear-gradient(135deg, {BRAND['card_mint']}, {BRAND['card_peach']}); }}
.gbp-meta {{ display: flex; flex-direction: column; gap: 2mm; font-size: 9.5px; color: {BRAND['muted']}; }}
.gbp-meta .row {{ display: flex; align-items: center; gap: 2.5mm; }}
.gbp-meta .ic {{ color: {BRAND['teal']}; }}
.gbp-actions {{ display: flex; gap: 3mm; margin-top: 5mm; }}
.gbp-actions span {{ font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: 700; text-transform: uppercase; padding: 2.5mm 5mm; border-radius: 999px; }}
.gbp-actions .call {{ background: {BRAND['teal']}; color: #fff; }}
.gbp-actions .visit {{ border: 1px solid rgba(24,53,43,0.15); color: {BRAND['ink']}; }}

/* act2-teal used to be a full dark background (needed light-text overrides for
   every component here); it's cream now with just a top accent bar, so the
   default light-page component styles already apply correctly, no overrides needed. */

/* ---------- proof mini tiles ---------- */
.proof-mini-grid {{ display: flex; flex-direction: column; gap: 4mm; margin-top: 5mm; }}
.proof-mini {{ display: flex; gap: 5mm; background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 14px; overflow: hidden; box-shadow: 0 10px 26px rgba(24,53,43,0.05); }}
.proof-mini img {{ width: 42mm; height: 30mm; object-fit: cover; object-position: top; flex-shrink: 0; }}
.proof-mini .body {{ padding: 4mm 5mm 4mm 0; display: flex; flex-direction: column; justify-content: center; }}
.proof-mini .client {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 12px; color: {BRAND['ink']}; }}
.proof-mini .loc {{ font-size: 9px; color: {BRAND['muted']}; margin: 1mm 0 2mm; }}
.proof-mini .result {{ font-size: 10px; line-height: 1.5; color: {BRAND['ink']}; }}

/* ---------- blueprint phases ---------- */
.phase {{ margin-bottom: 6mm; }}
.phase-head {{ display: flex; align-items: center; gap: 3mm; margin-bottom: 3mm; }}
.phase-tag {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 11px; color: #fff; background: {BRAND['teal']}; border-radius: 6px; padding: 1mm 2.5mm; }}
.phase-title {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 13.5px; color: {BRAND['ink']}; }}

/* ---------- pricing tiers ---------- */
.tier {{ position: relative; background: #fff; border: 1px solid rgba(24,53,43,0.08); border-left: 4px solid {BRAND['muted']}; border-radius: 12px; padding: 3mm 6mm; margin-bottom: 1.5mm; }}
.tier.recommended {{
  border-left: none; border: 2px solid {BRAND['orange']}; background: {BRAND['card_peach']};
  padding: 4mm 7mm; box-shadow: 0 20px 46px rgba(242,106,61,0.22);
}}
.tier.skip {{ border-left-color: #cfd8d2; opacity: 0.7; }}
.tier-badge {{ position: absolute; top: 5mm; right: 6mm; font-family: 'JetBrains Mono', monospace; font-size: 8px; font-weight: 700; letter-spacing: 0.06em; padding: 1.5mm 3mm; border-radius: 999px; background: {BRAND['orange']}; color: #fff; }}
.tier.recommended .tier-badge {{ top: 7mm; right: 8mm; font-size: 8.5px; padding: 2mm 3.5mm; }}
.tier-badge.skip {{ background: #cfd8d2; color: {BRAND['ink']}; }}
.tier-name {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 13.5px; color: {BRAND['ink']}; }}
.tier.recommended .tier-name {{ font-size: 16px; }}
.tier-price {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 16px; color: {BRAND['orange_dark']}; margin: 1mm 0; }}
.tier.recommended .tier-price {{ font-size: 22px; }}
.tier-price-note {{ font-size: 9px; color: {BRAND['muted']}; margin-top: -0.5mm; margin-bottom: 1mm; }}
.tier-timeline {{ font-size: 9px; color: {BRAND['muted']}; }}
.tier ul {{ margin-top: 2mm; }}
.tier li {{ list-style: none; font-size: 9.5px; line-height: 1.4; color: {BRAND['ink']}; padding-left: 4mm; position: relative; margin-top: 1mm; }}
.tier li::before {{ content: "\\2022"; position: absolute; left: 0; color: {BRAND['teal']}; }}

/* ---------- add-ons (priced extras, not full packages) ---------- */
.addon-box {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 12px; padding: 5mm 6mm; margin-top: 2mm; }}
.addon-box .addon-label {{ font-family: 'JetBrains Mono', monospace; font-size: 8.5px; text-transform: uppercase; letter-spacing: 0.1em; color: {BRAND['muted']}; margin-bottom: 2.5mm; }}
.addon-row {{ display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; padding: 2mm 0; border-top: 1px solid rgba(24,53,43,0.06); }}
.addon-row:first-of-type {{ border-top: none; }}
.addon-row .name {{ font-size: 10px; color: {BRAND['ink']}; }}
.addon-row .name .note {{ display: block; font-size: 8.5px; color: {BRAND['muted']}; font-style: italic; }}
.addon-row .price {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 10px; color: {BRAND['orange_dark']}; white-space: nowrap; }}

/* ---------- payment ---------- */
.payment-box {{ background: {BRAND['card_mint']}; border-radius: 12px; padding: 6mm 7mm; margin: 4mm 0 6mm; }}
.payment-box .amounts {{ display: flex; gap: 8mm; font-size: 11px; font-weight: 700; color: {BRAND['ink']}; flex-wrap: wrap; }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; margin-top: 3mm; }}
.two-col h4 {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 12px; margin-bottom: 2mm; }}
.accounts-table {{ width: 100%; margin-top: 4mm; border-collapse: collapse; }}
.accounts-table td {{ padding: 3mm 4mm; border: 1px solid rgba(24,53,43,0.1); font-size: 10.5px; }}
.accounts-table td:first-child {{ font-weight: 700; color: {BRAND['teal']}; width: 40mm; }}
.accounts-table td:last-child {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; }}

/* ---------- platform badges (closing page "we're online here" row) ---------- */
.platform-row {{ display: flex; align-items: center; gap: 3.5mm; margin-top: 4mm; }}
.platform-row .platform-label {{ font-family: 'JetBrains Mono', monospace; font-size: 8.5px; text-transform: uppercase; letter-spacing: 0.1em; color: {BRAND['muted']}; margin-right: 1mm; }}
.platform-badge {{ display: inline-flex; align-items: center; gap: 1.5mm; }}
.platform-badge .ic {{ width: 18px; height: 18px; border-radius: 5px; display: flex; align-items: center; justify-content: center; }}
.platform-badge .ic svg {{ width: 10px; height: 10px; }}
.platform-badge .name {{ font-family: 'Manrope', sans-serif; font-weight: 700; font-size: 9.5px; color: {BRAND['ink']}; }}

/* ---------- closing page logo (bigger + present -- close-invite-mast has no logo by default) ---------- */
.close-invite-mast .brand-lock {{ display: inline-flex; align-items: center; gap: 3mm; }}
.close-invite-mast .brand-lock .logo-mark {{ width: 40px; height: 40px; border-radius: 11px; }}

/* ---------- closing headline (this client's own copy, stacked + color-coded) ---------- */
.rud-close-headline {{ font-style: normal; }}
.rud-close-headline .ln {{ display: block; }}
.rud-close-headline .ln.soft {{ font-style: italic; color: {BRAND['orange']}; }}
.rud-close-headline .ln.teal {{ color: {BRAND['teal']}; }}
.close-invite-body.emphasis {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 15px; color: {BRAND['ink']}; font-style: normal; }}

"""


def build_exec_verdict(page_no: int) -> str:
    cards = "".join(
        f"""
        <div class="status-card tone-{c['tone']}">
          <div class="label">{c['label']}</div>
          <div class="title">{c['title']}</div>
          <p>{c['body']}</p>
        </div>
        """
        for c in STATUS_CARDS
    )
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Where things stand</span>
      <h2 class="display opener-title">Ang totoong status, sa isang tingin lang.</h2>
      {cards}
      <div class="callout" style="margin-top:2mm;">
        <h4>Executive verdict</h4>
        <p>{EXEC_VERDICT}</p>
        <p>{EXEC_VERDICT_2}</p>
      </div>
      <p class="body-text" style="margin-top:4mm;">{EXEC_INTRO}</p>
      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:24px; margin:0;">{STATUS_CARDS[0]['title']}. <span class="accent">{STATUS_CARDS[-1]['title']}</span> na ang susunod.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act1", page_no=page_no, section_label="The Verdict")


def build_opportunity(page_no: int) -> str:
    benefits = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{b}</span></li>' for b in BENEFITS)
    boundaries = "".join(f'<li><span class="dot">!</span><span>{b}</span></li>' for b in BOUNDARIES)
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Client opportunity</span>
      <h2 class="display opener-title">Executive summary</h2>
      <p class="body-text" style="margin-top:3mm;">{OPPORTUNITY_INTRO}</p>

      <div class="callout teal">
        <h4>Recommended path: {RECOMMENDED_PATH['name']}</h4>
        <p>{RECOMMENDED_PATH['body']}</p>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10mm; margin-top:5mm;">
        <div>
          <span class="tag tag-teal">Benefits</span>
          <h3 style="font-size:13.5px; margin-top:2.5mm;">Ano ang makukuha niyo dito</h3>
          <ul class="checklist good">{benefits}</ul>
        </div>
        <div>
          <span class="tag tag-orange">No fake promises</span>
          <h3 style="font-size:13.5px; margin-top:2.5mm;">Honest boundaries</h3>
          <ul class="checklist warn">{boundaries}</ul>
        </div>
      </div>
      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:24px; margin:0;">Isang malinaw na plano, isang malinaw na simula para sa <span class="accent">buong foundation</span>.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act1", page_no=page_no, section_label="The Opportunity")


def build_findings(page_no: int) -> str:
    flagged_count = sum(1 for f in AUDIT_FINDINGS if f["tone"] == "orange")
    rows = "".join(
        f"""
        <tr>
          <td style="font-weight:700;">{f['area']}</td>
          <td><span class="status-pill {f['tone']}">{f['status']}</span></td>
          <td>{f['impact']}</td>
          <td>{f['reco']}</td>
        </tr>
        """
        for f in AUDIT_FINDINGS
    )
    confirmation_html = ""
    if NEEDS_CONFIRMATION:
        items = "".join(f'<li><span class="dot">!</span><span>{i}</span></li>' for i in NEEDS_CONFIRMATION)
        confirmation_html = f"""
        <div class="callout" style="margin-top:6mm;">
          <h4>Kailangan pang kumpirmahin</h4>
          <p style="margin-bottom:2mm;">Base ito sa live public research lang. Bago namin gamitin ang mga sumusunod bilang panghuling claim sa publiko, kailangan muna ng kumpirmasyon niyo:</p>
          <ul class="checklist warn">{items}</ul>
        </div>
        """
    content = f"""
    <style>
      /* Scoped to this page only: 6 findings rows + the confirmation callout
         run right up against the page edge at the shared component's default
         spacing (borderline overflow observed on some font-load timings), so
         this page gets its own tighter rhythm instead of shrinking the
         shared .findings-table/.callout/.checklist used elsewhere. */
      .findings-tight .findings-table td {{ padding: 2.6mm 3.5mm; }}
      .findings-tight .callout {{ padding: 4.5mm 6mm; margin: 4mm 0 0; }}
      .findings-tight .checklist {{ gap: 1.8mm; margin-top: 2mm; }}
    </style>
    <div class="pad findings-tight">
      <span class="tag tag-teal">Live audit findings</span>
      <h2 class="display opener-title">Ano ang nakita namin sa audit.</h2>
      <p class="body-text" style="margin-top:3mm;">Isinalarawan namin ito sa simpleng client language: ano ang ibig sabihin ng bawat status, bakit ito mahalaga, at ano ang dapat sundan pagkatapos.</p>
      <table class="findings-table">
        <thead><tr><th>Area</th><th>Status</th><th>Client impact</th><th>We Forge Web recommendation</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {confirmation_html}
      <div style="margin-top:4mm; padding-top:4mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:22px; margin:0;"><span class="accent">{flagged_count} sa {len(AUDIT_FINDINGS)}</span> checkpoint ang kailangan ng aksyon ngayon.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act1", page_no=page_no, section_label="The Diagnosis")


def evidence_bleed(item: dict) -> str:
    fit_class = item.get("fit", "cover-top")
    height = item.get("height_mm", 118)
    return f"""
    <div class="evidence-bleed {fit_class}" style="height:{height}mm;"><img src="{asset(item['file'])}" alt="{item['label']}" /></div>
    <div class="evidence-cap"><div class="label">{item['label']}</div><p>{item['caption']}</p></div>
    """


def evidence_card(item: dict) -> str:
    fit_class = item.get("fit", "cover-top")
    height = item.get("height_mm", 58)
    return f"""
    <div class="evidence-card {fit_class}">
      <div class="img-wrap" style="height:{height}mm;"><img src="{asset(item['file'])}" alt="{item['label']}" /></div>
      <div class="cap"><div class="label">{item['label']}</div><p>{item['caption']}</p></div>
    </div>
    """


def build_evidence_page(*, eyebrow: str, title: str, lede: str, large: list[dict] | None = None, paired: list[dict] | None = None, page_no: int | None = None) -> str:
    intro = f"""
    <div class="pad" style="flex:none; padding-bottom:5mm;">
      <span class="tag tag-teal">{eyebrow}</span>
      <h2 class="display opener-title" style="font-size:26px;">{title}</h2>
      <p class="body-text" style="margin-top:3mm;">{lede}</p>
    </div>
    """
    bleed_html = "".join(evidence_bleed(i) for i in (large or []))
    paired_html = ""
    if paired:
        paired_html = f'<div class="pad" style="flex:none; padding-top:6mm;"><div class="evidence-row">' + "".join(evidence_card(i) for i in paired) + "</div></div>"
    content = intro + bleed_html + paired_html
    return shell(content, klass="page-act1", page_no=page_no, section_label="The Evidence")


def build_root_cause(page_no: int) -> str:
    risks = "".join(f'<li><span class="dot">!</span><span>{r}</span></li>' for r in RISKS)
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">The real root cause</span>
      <h2 class="display opener-title" style="font-size:26px;">Hindi lang ito tungkol sa isang blangkong domain.</h2>
      <div class="root-cause-box">
        <div class="lead">{ROOT_CAUSE_LEAD} Ang totoong dahilan ay ito.</div>
        <p class="pull-quote" style="font-size:28px; margin:3mm 0;">{ROOT_CAUSE_STATEMENT}</p>
        <p class="body-text">{ROOT_CAUSE_BODY}</p>
      </div>

      <span class="tag tag-teal" style="margin-top:6mm;">Kung walang mababago</span>
      <h3 style="font-size:14px; margin-top:3mm;">{RISK_INTRO}</h3>
      <ul class="checklist warn">{risks}</ul>
      <p class="body-text" style="margin-top:5mm;">{RISK_CLOSER}</p>
    </div>
    """
    return shell(content, klass="page-act1", page_no=page_no, section_label="The Real Problem")


def build_scenario(page_no: int) -> str:
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Isipin natin</span>
      <h2 class="display opener-title" style="font-size:26px;">{SCENARIO['title']}</h2>
      <p class="body-text" style="margin-top:3mm;">{SCENARIO['story']}</p>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10mm; margin-top:6mm;">
        <div>
          <span class="tag tag-orange">Ngayon</span>
          <p class="body-text" style="margin-top:2.5mm;">{SCENARIO['today']}</p>
        </div>
        <div>
          <span class="tag tag-teal">Pagkatapos ng foundation</span>
          <p class="body-text" style="margin-top:2.5mm;">{SCENARIO['after']}</p>
        </div>
      </div>

      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:24px; margin:0;">Search: <span class="accent">&ldquo;{SCENARIO['search_query']}&rdquo;</span></p>
        <p class="mock-label" style="margin-top:3mm;">Sample direction ito para maipakita ang klase ng customer na naghahanap. Hindi ito guaranteed ranking, lead, o traffic promise.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act1", page_no=page_no, section_label="Imagine This")


def build_dream_serp(page_no: int) -> str:
    sitelinks = "".join(f"<span>{s}</span>" for s in CLIENT["sitelinks"])
    fields = "".join(f'<div class="row"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in SERP_FIELDS)
    content = f"""
    <div class="pad" style="justify-content:center;">
      <span class="tag tag-orange">Ang visibility dream</span>
      <h2 class="display opener-title">Ganito namin gustong makita kayo ng customers online.</h2>
      <p class="body-text" style="margin-top:3mm;">{DREAM_INTRO}</p>
      <p class="body-text" style="margin-top:2.5mm; font-style:italic;">{DREAM_BOUNDARY}</p>

      <div class="serp-card" style="margin-top:6mm;">
        <div class="serp-bar">{ICON_SEARCH}<span>{CLIENT['search_query']}</span></div>
        <div class="serp-result">
          <span class="serp-url"><span class="serp-favicon"></span>{CLIENT['dream_domain']} &rsaquo; home</span>
          <div class="serp-title">{CLIENT['meta_title']}</div>
          <p class="serp-desc">{CLIENT['meta_desc']}</p>
          <div class="serp-sitelinks">{sitelinks}</div>
        </div>
      </div>
      <div class="field-list">{fields}</div>
      <p class="mock-label">Sample visualization lang po ito. Hindi ito actual Google screenshot at hindi ito pangako ng exact ranking o placement.</p>
    </div>
    """
    return shell(content, klass="page-act2-peach", page_no=page_no, section_label="The Vision")


def build_dream_keywords(page_no: int) -> str:
    rows = "".join(
        f"""
        <div class="keyword-row">
          <span class="q">{ICON_SEARCH}<span>"{q}"</span></span>
          <span class="arrow">{ICON_ARROW}</span>
          <span class="dest tag tag-teal">{dest}</span>
        </div>
        """
        for q, dest in KEYWORD_DOORS
    )
    content = f"""
    <div class="pad">
      <span class="tag tag-orange">Isang website, maraming pinto</span>
      <h2 class="display opener-title" style="font-size:26px;">Hindi lang isang keyword ang pagkakakitaan niyo.</h2>
      <p class="pull-quote" style="font-size:30px; margin-top:5mm;">{KEYWORD_DOORS_QUOTE}</p>
      <p class="body-text">{KEYWORD_DOORS_INTRO}</p>
      <div class="keyword-rows">{rows}</div>
      <p class="body-text" style="margin-top:5mm;">{KEYWORD_DOORS_CLOSER}</p>
    </div>
    """
    return shell(content, klass="page-act2-teal", page_no=page_no, section_label="Many Doors")


def build_website_dream(page_no: int) -> str:
    questions = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{q}</span></li>' for q in WEBSITE_DREAM_QUESTIONS)
    trust = "".join(f'<div class="trust-pill"><div class="name">{n}</div><p>{d}</p></div>' for n, d in TRUST_PAGES)
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Ang website dream</span>
      <h2 class="display opener-title">{WEBSITE_DREAM_INTRO}</h2>
      <p class="body-text" style="margin-top:3mm;">Dapat masagot agad ng website ang mga totoong tanong ng shopper bago pa sila mag alinlangan.</p>
      <ul class="checklist good">{questions}</ul>

      <span class="tag tag-orange" style="margin-top:7mm;">Bakit sila magtitiwala</span>
      <h3 style="font-size:14px; margin-top:3mm;">Apat na page na nagsasabing totoo kami, malinaw kami, kausapin niyo kami.</h3>
      <div class="trust-strip">{trust}</div>
      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.12);">
        <p class="pull-quote" style="font-size:24px; margin:0;"><span class="accent">{len(TRUST_PAGES)} trust page.</span> Isang malinaw na dahilan para magtiwala.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act2-peach", page_no=page_no, section_label="The Experience")


# Per-type copy for the GBP dream page, matching the GBP decision logic: a physical
# location shows its address, a service-area business hides it and shows coverage
# instead, and a hybrid business shows both. Not used for PH Gadget Picks (online_only,
# their own audit marks GBP as Skip v1 for this version) but kept ready for the next
# local client. See README "GBP business types" for how to configure CLIENT for each.
GBP_TYPE_COPY = {
    "physical_location": {
        "eyebrow": "May physical location kayo",
        "intro": (
            "Kapag may customer na naghahanap sa Google Maps, makikita ang address ninyo dahil may "
            "totoong lokasyon kayo na pwedeng bisitahin. Dapat kumpleto at propesyonal ang profile "
            "bago pa sila magdesisyon pumunta."
        ),
        "location_label": "Address",
        "setup_items": [
            "Tamang primary at secondary business category",
            "Kumpletong services o products list",
            "Business hours",
            "Photos ng location at services",
            "Website link at call button",
            "Review request strategy",
        ],
    },
    "service_area": {
        "eyebrow": "Service area business kayo",
        "intro": (
            "Kayo ang pumupunta sa customer, kaya hindi ipapakita ang isang fixed address. Sa halip, "
            "ilalagay ang totoong mga lugar na sinasakupan ninyo, para malinaw kung sino ang pwede "
            "ninyong asikasuhin."
        ),
        "location_label": "Service areas",
        "setup_items": [
            "I setup as service area business, hindi ipapakita ang address",
            "Totoong service areas lang, hindi manipis na duplicate list",
            "Tamang category at service descriptions",
            "Real work photos, before and after kung meron",
            "Call at message options",
            "Review request strategy",
        ],
    },
    "hybrid": {
        "eyebrow": "May office kayo at may service areas",
        "intro": (
            "May opisina o store kayo na pwedeng bisitahin, pero umaabot din kayo sa nearby areas. "
            "Ipapakita ang address, kasabay ng totoong mga lugar na sinasakupan ninyo."
        ),
        "location_label": "Address at service areas",
        "setup_items": [
            "Address, ipapakita dahil bukas ito sa customers",
            "Service areas na naka align sa website location pages",
            "Services, photos, at posts",
            "Review request strategy",
        ],
    },
}


def build_dream_gbp(page_no: int) -> str:
    copy = GBP_TYPE_COPY[CLIENT["business_type"]]
    service = CLIENT.get("service_keyword", "service")
    if CLIENT["business_type"] == "service_area":
        location_value = CLIENT.get("service_areas_display", CLIENT.get("city", "your service areas"))
    elif CLIENT["business_type"] == "hybrid":
        location_value = f"{CLIENT.get('address', 'Business address')} (sakop din ang {CLIENT.get('city', 'nearby areas')})"
    else:
        location_value = CLIENT.get("address", "Business address, ipapakita dahil bukas ito sa customers")
    setup_items = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{i}</span></li>' for i in copy["setup_items"])
    content = f"""
    <div class="pad" style="justify-content:center;">
      <span class="tag tag-orange">{copy['eyebrow']}</span>
      <h2 class="display opener-title" style="font-size:26px;">Hindi lang website ang kailangan. Kailangan din propesyonal ang Google Business Profile.</h2>
      <p class="body-text" style="margin-top:3mm;">{copy['intro']}</p>

      <div class="gbp-card" style="margin-top:6mm;">
        <div class="gbp-top">
          <div>
            <div class="gbp-name">{CLIENT['business_name']}</div>
            <div class="gbp-stars">{ICON_STAR}{ICON_STAR}{ICON_STAR}{ICON_STAR}{ICON_STAR} Sample rating display</div>
          </div>
          <span class="tag tag-teal">{service}</span>
        </div>
        <div class="gbp-photos"><div></div><div></div><div></div><div></div></div>
        <div class="gbp-meta">
          <div class="row">{ICON_PIN}<span>{copy['location_label']}: {location_value}</span></div>
          <div class="row"><span class="mono">Open now &middot; Hours sample</span></div>
        </div>
        <div class="gbp-actions"><span class="call">Call now</span><span class="visit">Visit website</span></div>
      </div>
      <p class="mock-label">Sample visualization lang po ito. Hindi ito actual Google Business Profile screenshot at hindi ito pangako ng Google Maps ranking o placement.</p>

      <h3 style="font-size:13.5px; margin-top:6mm;">Ito ang aayusin o irerekomenda namin</h3>
      <ul class="checklist good">{setup_items}</ul>
    </div>
    """
    return shell(content, klass="page-act2-teal", page_no=page_no, section_label="Local Trust")


def build_proof(page_no: int) -> str:
    tiles = [cs for cs in CASE_STUDIES if cs.client in PROOF_CASE_SLUGS]
    rows = "".join(
        f"""
        <div class="proof-mini">
          <img src="{asset(cs.hero)}" alt="{cs.client}" />
          <div class="body">
            <div class="client">{cs.client}</div>
            <div class="loc">{cs.industry}</div>
            <p class="result">{cs.outcomes[0]}</p>
          </div>
        </div>
        """
        for cs in tiles
    )
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Proof and confidence</span>
      <h2 class="display opener-title">Hindi pangako, may foundation na kaming nagawa for other businesses.</h2>
      <p class="body-text" style="margin-top:3mm;">{PROOF_INTRO}</p>
      <div class="proof-mini-grid">{rows}</div>
      <p class="mock-label">{PROOF_NOTE}</p>
      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:24px; margin:0;"><span class="accent">{len(tiles)} negosyo,</span> {len(tiles)} magkaibang industriya, isang parehong resulta: mas malinaw na presence.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act3", page_no=page_no, section_label="The Proof")


def build_blueprint(page_no: int) -> str:
    total_items = sum(len(p["items"]) for p in BLUEPRINT["phases"])
    phases = "".join(
        f"""
        <div class="phase">
          <div class="phase-head"><span class="phase-tag">{p['tag']}</span><span class="phase-title">{p['title']}</span></div>
          <ul class="checklist good">{"".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{item}</span></li>' for item in p['items'])}</ul>
        </div>
        """
        for p in BLUEPRINT["phases"]
    )
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">What We Forge Web will create</span>
      <h2 class="display opener-title" style="font-size:26px;">Foundation build blueprint</h2>
      <div class="callout teal" style="margin:4mm 0 6mm;"><h4>The goal</h4><p>{BLUEPRINT['goal']}</p></div>
      {phases}
      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:24px; margin:0;"><span class="accent">{total_items} concrete deliverables</span> sa build blueprint na ito.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act3", page_no=page_no, section_label="The Blueprint")


def build_glossary(page_no: int) -> str:
    rows = "".join(f"<tr><td>{term}</td><td>{explanation}</td></tr>" for term, explanation in TECH_GLOSSARY)
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Sa simpleng salita</span>
      <h2 class="display opener-title" style="font-size:26px;">Ano ba talaga ang mga technical na term na ito?</h2>
      <p class="body-text" style="margin-top:3mm;">Hindi namin gustong maligaw kayo sa jargon. Ito ang mga term na mababasa niyo sa proposal na ito, in plain language.</p>
      <table class="term-table">{rows}</table>
      <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
        <p class="pull-quote" style="font-size:24px; margin:0;"><span class="accent">{len(TECH_GLOSSARY)} terms,</span> ini-explain sa simpleng salita, para walang malilito.</p>
      </div>
    </div>
    """
    return shell(content, klass="page-act3", page_no=page_no, section_label="Plain English")


def build_investment_value(page_no: int) -> str:
    items = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{i}</span></li>' for i in INVESTMENT_VALUE_ITEMS)
    content = f"""
    <div class="pad">
      <span class="tag tag-orange">Ano talaga ang binabayaran niyo dito</span>
      <h2 class="display opener-title">{INVESTMENT_VALUE_INTRO}</h2>
      <p class="body-text" style="margin-top:3mm;">{INVESTMENT_VALUE_LEAD}</p>
      <ul class="checklist good">{items}</ul>
      <p class="pull-quote" style="font-size:26px; margin-top:6mm;"><span class="pull-quote-mark">&ldquo;</span>{INVESTMENT_VALUE_CLOSER}</p>
    </div>
    """
    return shell(content, klass="page-act3", page_no=page_no, section_label="The Value")


def build_pricing(page_no: int) -> str:
    tiers = ""
    for t in PRICING_TIERS:
        classes = "tier"
        badge_html = ""
        # Any truthy badge renders as a pill. "RECOMMENDED" gets the orange highlight
        # treatment, anything else (e.g. "SKIP", "LATER", "OPTIONAL") gets the neutral
        # grey treatment with whatever label the client file provides.
        if t.get("badge") == "RECOMMENDED":
            classes += " recommended"
            badge_html = '<span class="tier-badge">RECOMMENDED</span>'
        elif t.get("badge"):
            classes += " skip"
            badge_html = f'<span class="tier-badge skip">{t["badge"]}</span>'
        items = "".join(f"<li>{i}</li>" for i in t["items"])
        price_note_html = f'<div class="tier-price-note">{t["price_note"]}</div>' if t.get("price_note") else ""
        tiers += f"""
        <div class="{classes}">
          {badge_html}
          <div class="tier-name">{t['name']}</div>
          <div class="tier-price">{t['price']}</div>
          {price_note_html}
          <div class="tier-timeline mono">Timeline: {t['timeline']}</div>
          <ul>{items}</ul>
        </div>
        """
    content = f"""
    <div class="pad">
      <span class="tag tag-teal">Proposal</span>
      <h2 class="display opener-title">Investment options</h2>
      <p class="body-text" style="margin-top:3mm;">{PRICING_INTRO}</p>
      {tiers}
    </div>
    """
    return shell(content, klass="page-act3", page_no=page_no, section_label="The Investment")


def build_payment(page_no: int) -> str:
    addon_rows = "".join(
        f"""
        <div class="addon-row">
          <span class="name">{name}{f'<span class="note">{note}</span>' if note else ''}</span>
          <span class="price mono">{price}</span>
        </div>
        """
        for name, price, note in ADDONS
    )
    included = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{i}</span></li>' for i in PAYMENT["included"])
    not_included = "".join(f'<li><span class="dot">!</span><span>{i}</span></li>' for i in PAYMENT["not_included"])
    accounts = "".join(f"<tr><td>{name}</td><td>{num}</td></tr>" for name, num in PAYMENT["accounts"])
    steps = "".join(f"<li>{s}</li>" for s in PAYMENT["next_steps"])
    what_we_need_html = ""
    closer_html = ""
    if PAYMENT.get("what_we_need"):
        items = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{i}</span></li>' for i in PAYMENT["what_we_need"])
        what_we_need_html = f"""
        <div class="callout teal" style="margin-top:6mm;">
          <h4>Ano ang kailangan namin mula sa inyo</h4>
          <ul class="checklist good" style="margin-top:2mm;">{items}</ul>
        </div>
        """
    elif not ADDONS:
        # Only room for this closing pull-quote when neither the what-we-need box nor
        # the add-ons box is also present, any two together overflow the page (see
        # generate_audit_report_rf_munoz.py).
        closer_html = """
        <div style="margin:auto 0; padding-top:6mm; border-top:1px solid rgba(24,53,43,0.08);">
          <p class="pull-quote" style="font-size:24px; margin:0;">Ligtas at malinaw ang bawat hakbang, mula downpayment hanggang launch.</p>
        </div>
        """
    content = f"""
    <div class="pad">
      <span class="tag tag-orange">Start clearly</span>
      <h2 class="display opener-title">Payment terms and next step</h2>
      <div class="payment-box">
        <div class="mono" style="font-size:9px; text-transform:uppercase; letter-spacing:.08em; color:{BRAND['teal']}; margin-bottom:2mm;">Foundation payment structure</div>
        <div class="amounts">
          <span>Kabuuan: {PAYMENT['total']}</span>
          <span>Downpayment: {PAYMENT['downpayment']} bago magsimula</span>
          <span>Balance: {PAYMENT['balance']} bago mag launch</span>
        </div>
      </div>
      <div class="two-col">
        <div><h4>Included</h4><ul class="checklist good">{included}</ul></div>
        <div><h4>Not included</h4><ul class="checklist warn">{not_included}</ul></div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-top:6mm;">
        <div>
          <h3 style="font-size:13px;">Official payment accounts</h3>
          <table class="accounts-table">{accounts}</table>
        </div>
        <div>
          <h3 style="font-size:13px;">Susunod na hakbang</h3>
          <ol class="num-list">{steps}</ol>
        </div>
      </div>
      <div class="addon-box" style="margin-top:5mm;">
        <div class="addon-label">Add-ons (on top of any package)</div>
        {addon_rows}
      </div>
      {what_we_need_html}
      <p class="mock-label">Makikita ang QR codes at full terms sa official Terms page: {PAYMENT['terms_url']}. Pagkatapos magbayad, paki send lang ang screenshot ng resibo sa official We Forge Web Viber, WhatsApp, o Facebook page para sa verification.</p>
      {closer_html}
    </div>
    """
    return shell(content, klass="page-act3", page_no=page_no, section_label="Start Here")


def build_close() -> str:
    """Inviting magazine endpaper -- content-strategy soft close, no photo, no black.
    Shared treatment across every generator (see brand_kit.py .close-invite-* CSS)."""
    qr_url = CLIENT.get("cover_qr_url") or f"https://{CONTACT['site']}"
    qr_src = qr_data_uri(qr_url)
    return f"""
    <section class="page close-invite">
      <div class="close-invite-ghost">Next.</div>
      <div class="close-invite-inner">
        <div class="close-invite-mast">
          <div class="brand-lock">{LOGO_SVG}<span class="brand">We Forge Web</span></div>
          <span>End matter &middot; Discovery</span>
          <span>{CONTACT['site']}</span>
        </div>
        <div class="close-invite-kicker">Ready when you are</div>
        <div class="close-invite-mega rud-close-headline">
          <span class="ln">Gawin nating</span>
          <span class="ln teal">mas madaling makita</span>
          <span class="ln soft">at pagkatiwalaan</span>
          <span class="ln">ang business ninyo.</span>
        </div>
        <p class="close-invite-body">{SOFT_CLOSE}</p>
        <p class="close-invite-body">{SOFT_CLOSE_2}</p>
        <p class="close-invite-body emphasis">{SOFT_CLOSE_3}</p>
        <div class="close-invite-grid">
          <div>
            <div class="k">Email</div>
            <div class="v">{CONTACT['email']}</div>
            <div class="k" style="margin-top:3.5mm;">WhatsApp / Viber / SMS</div>
            <div class="v">{CONTACT['phone_display']}</div>
            <div class="k" style="margin-top:3.5mm;">Hours</div>
            <div class="v">{CONTACT['hours']}</div>
            <div class="platform-row">
              <span class="platform-label">Online din kami sa</span>
              <span class="platform-badge"><span class="ic" style="background:#7360F2;">{ICON_PHONE}</span><span class="name">Viber</span></span>
              <span class="platform-badge"><span class="ic" style="background:#25D366;">{ICON_PHONE}</span><span class="name">WhatsApp</span></span>
            </div>
          </div>
          <div>
            <div class="k">Location</div>
            <div class="v">{CONTACT['location']}</div>
          </div>
          <div class="qr">
            <img src="{qr_src}" alt="QR" />
            <div class="url">{CONTACT['site']}</div>
          </div>
        </div>
        <div class="close-invite-foot">Built for <span class="accent">today</span>. Ready for <span class="accent">tomorrow</span>.</div>
      </div>
    </section>
    """


def build_html() -> str:
    n = 1
    pages = [build_cover_v2(business_name=CLIENT["business_name"], business_domain=CLIENT["domain"], date=CLIENT["date"])]
    n += 1
    pages.append(build_exec_verdict(n)); n += 1
    pages.append(build_opportunity(n)); n += 1
    pages.append(build_findings(n)); n += 1
    # Evidence page(s): only rendered when a client file populates EVIDENCE_LARGE /
    # EVIDENCE_PAIRED. For clients with several screenshots worth grouping into more
    # than one page, call build_evidence_page() directly with your own item subsets
    # and an explicit page_no here instead (see generate_audit_report_rf_munoz.py for
    # an example with two evidence pages).
    if EVIDENCE_LARGE or EVIDENCE_PAIRED:
        pages.append(
            build_evidence_page(
                eyebrow="Live audit evidence",
                title="May proof na, pero kailangan ng sariling hub.",
                lede="Hindi ito mockup. Ito ang aktwal na screenshot evidence mula sa live research. May social proof na, pero may friction pa sa customer journey.",
                large=EVIDENCE_LARGE,
                paired=EVIDENCE_PAIRED,
                page_no=n,
            )
        )
        n += 1
    if OPPORTUNITY_EVIDENCE_LARGE or OPPORTUNITY_EVIDENCE_PAIRED:
        pages.append(
            build_evidence_page(
                eyebrow="Opportunity evidence",
                title="May demand at may kalaban na naka-position.",
                lede="Ipinapakita ng competitor screenshots na may active service-area positioning sa septic at declogging space. Dito papasok ang mas malinaw na NCR website foundation.",
                large=OPPORTUNITY_EVIDENCE_LARGE,
                paired=OPPORTUNITY_EVIDENCE_PAIRED,
                page_no=n,
            )
        )
        n += 1
    pages.append(build_root_cause(n)); n += 1
    pages.append(build_scenario(n)); n += 1
    pages.append(build_dream_serp(n)); n += 1
    pages.append(build_dream_keywords(n)); n += 1
    pages.append(build_website_dream(n)); n += 1
    if CLIENT["business_type"] != "online_only" and not CLIENT.get("skip_gbp"):
        pages.append(build_dream_gbp(n)); n += 1
    pages.append(build_proof(n)); n += 1
    pages.append(build_blueprint(n)); n += 1
    pages.append(build_glossary(n)); n += 1
    pages.append(build_investment_value(n)); n += 1
    pages.append(build_pricing(n)); n += 1
    pages.append(build_payment(n)); n += 1
    pages.append(build_close())

    body = "\n".join(pages)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>We Forge Web | {CLIENT['business_name']} Audit + Proposal</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>{body}</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the client Brand Presence Audit + Proposal PDF.")
    parser.add_argument(
        "--out",
        type=Path,
        default=OUTPUT_DIR / f"{CLIENT['business_name'].replace(' ', '_')}_Brand_Presence_Audit.pdf",
        help="Output PDF path.",
    )
    args = parser.parse_args()
    render_pdf(build_html(), OUTPUT_DIR / "_audit_report_source.html", args.out)
    print(f"Audit report generated: {args.out}")


if __name__ == "__main__":
    main()
