"""
We Forge Web -- Portfolio Case Study generator (audit-to-proposal Output 2).

Renders a single-client case study PDF for internal/portfolio use: project
overview, the main problem, strategy, what was or will be improved, the
customer journey, SEO/Google readiness, a visual-assets checklist for
whoever assembles screenshots later, a safe strategic outcome statement, a
100-150 word portfolio summary, and a social media caption.

Pulls client facts (name, domain, business_type) from generate_audit_report
so the two documents never disagree about the same client. If the project
has not launched yet, CASE_STUDY["status"] should say so and every section
should stay in future/plan tense, matching the spec's "use safe wording if
the work is not completed yet" rule.

Usage:
    python generate_case_study.py [--out PATH]

Requires: pip install -r requirements.txt && playwright install chromium
"""

from __future__ import annotations

import argparse
from pathlib import Path

from brand_kit import BASE_CSS, BRAND, CONTACT, LOGO_SVG, TOOL_DIR, page_shell, qr_data_uri, render_pdf
from generate_audit_report_jhapher_ncr import CLIENT

OUTPUT_DIR = TOOL_DIR / "output"


def shell(content: str, **kwargs) -> str:
    kwargs.setdefault("footer_left", "We Forge Web | Portfolio Case Study")
    kwargs.setdefault("footer_right", CONTACT["site"])
    return page_shell(content, **kwargs)


# ---------------------------------------------------------------------------
# CASE STUDY BLOCK -- specific to Jhapher NCR website proposal.
# ---------------------------------------------------------------------------

CASE_STUDY = {
    "status": "Project preview draft, pre launch",
    "subtitle": "Building a dedicated NCR service-area website for urgent septic and declogging customers.",
    "industry": "Local service, septic tank siphoning, pozo negro, and declogging",
    "project_type": "Website Foundation + Service Area Pages (proposal stage)",
    "overview": (
        "Jhapher Malabanan Septic Tank & Declogging Services is preparing a separate NCR-focused "
        "website for Metro Manila, Rizal, Cavite, Laguna, Bulacan, and nearby service areas. Public "
        "Facebook proof exists, but customers still need one clean website hub for services, coverage, "
        "proof, and booking."
    ),
    "main_problem": (
        "The brand has proof, but the NCR customer journey is not yet organized into a dedicated "
        "website with clear services, served areas, and a fast contact path."
    ),
    "strategy": (
        "We Forge Web planned a Website Foundation build centered on a mobile-first NCR homepage, "
        "service pages for septic siphoning, pozo negro cleaning, and declogging, a grouped service "
        "area structure, approved proof screenshots, and direct call or booking CTAs."
    ),
    "improvements": [
        ("Brand clarity", "Separate NCR positioning for Jhapher Malabanan Septic Tank & Declogging Services."),
        ("Website structure", "Homepage plus service and service-area sections built around urgent local intent."),
        ("Service pages", "Septic tank siphoning, pozo negro cleaning, habwa/suyop, and declogging."),
        ("Service areas", "Metro Manila, Rizal, Cavite, Laguna, Bulacan, and listed cities grouped cleanly."),
        ("Content strategy", "FAQs for urgent calls, access, scheduling, and what customers should prepare."),
        ("Trust proof", "Facebook screenshots/video stills used only with honest source labels."),
        ("Contact flow", "Phone and booking CTAs centered around 0999 744 2521, 0977 206 8785, and Viber 0927 437 4428."),
        ("Google ready foundation", "Sitemap, robots file, metadata, and Search Console prep."),
    ],
    "customer_journey": (
        "An urgent customer in Pasig, Makati, Quezon City, Antipolo, or another served area lands on "
        "a Jhapher NCR service page, sees the service type and area coverage, checks proof, then calls "
        "or books through the visible phone path."
    ),
    "seo_readiness": (
        "The site will launch with clean page titles and descriptions, a sitemap and robots file so "
        "Google knows what to check, and a Search Console submission path. None of this guarantees "
        "ranking. It gives Google a complete, accurate picture of the site from day one."
    ),
    "visual_assets": [
        "Homepage screenshot",
        "Mobile homepage screenshot",
        "Septic siphoning service page screenshot",
        "Declogging service page screenshot",
        "Contact page screenshot",
        "Proof section screenshot",
        "Before and after visual, Facebook-only proof versus owned NCR website",
        "Google search preview mockup",
        "Portfolio thumbnail",
        "Strategy summary graphic",
    ],
    "safe_outcome": (
        "This project is focused on creating a clearer, more professional, and more Google ready "
        "website foundation for Jhapher Malabanan NCR. Rankings, calls, leads, and Google placement "
        "are not guaranteed and depend on many factors beyond the website itself."
    ),
    "portfolio_summary": (
        "Jhapher Malabanan needed a separate NCR website foundation for septic tank siphoning, pozo "
        "negro cleaning, and declogging services across Metro Manila, Rizal, Cavite, Laguna, and "
        "Bulacan. The proposal turns scattered Facebook proof and broad service-area demand into a "
        "clear website structure: homepage, service sections, served-area grouping, proof blocks, and "
        "a direct phone path. Instead of promising rankings or leads, the plan focuses on urgent local "
        "customer behavior: people need to know if the service covers their area, what problem it "
        "solves, and how to call quickly."
    ),
    "social_caption": (
        "A separate NCR website foundation for Jhapher Malabanan Septic Tank & Declogging Services, "
        "built around urgent local search, clear service areas, proof, and a direct call path. "
        "#WeForgeWeb #BuiltToBeFound"
    ),
}

# Items that only make sense for local/physical businesses get filtered out
# automatically for online_only clients, keeping this template reusable.
_LOCAL_ONLY_ASSETS = {"Google Business Profile screenshot", "Google Maps screenshot"}
if CLIENT["business_type"] == "online_only" or CLIENT.get("skip_gbp"):
    CASE_STUDY["visual_assets"] = [a for a in CASE_STUDY["visual_assets"] if a not in _LOCAL_ONLY_ASSETS]
else:
    CASE_STUDY["visual_assets"] = CASE_STUDY["visual_assets"] + ["Google Business Profile screenshot", "Google Maps screenshot"]

ICON_CHECK = '<svg viewBox="0 0 24 24" class="ic"><polyline points="4 13 9 18 20 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

EXTRA_CSS = f"""
.status-ribbon {{
  display: inline-flex; align-items: center; gap: 6px;
  font-family: 'JetBrains Mono', monospace; font-size: 9.5px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase;
  padding: 4px 11px; border-radius: 999px;
  background: rgba(242,106,61,0.14); color: {BRAND['orange_dark']}; border: 1px solid rgba(242,106,61,0.3);
}}
.meta-strip {{ display: flex; flex-wrap: wrap; gap: 10mm; margin-top: 6mm; }}
.meta-strip .item {{ font-size: 9.5px; }}
.meta-strip .k {{ text-transform: uppercase; letter-spacing: 0.08em; color: rgba(244,241,234,0.6); font-weight: 600; font-size: 8.5px; }}
.meta-strip .v {{ margin-top: 1.5mm; font-weight: 700; color: #fff; }}

.body-text {{ font-size: 11px; line-height: 1.7; color: {BRAND['muted']}; max-width: 165mm; }}
.body-text + .body-text {{ margin-top: 3mm; }}

.callout {{ border-radius: 12px; padding: 6mm 7mm; border-left: 3px solid {BRAND['orange']}; background: {BRAND['card_peach']}; margin: 4mm 0; }}
.callout h4 {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 12.5px; margin-bottom: 2mm; color: {BRAND['ink']}; }}
.callout p {{ font-size: 10.5px; line-height: 1.6; color: {BRAND['ink']}; }}
.callout.teal {{ border-left-color: {BRAND['teal']}; background: {BRAND['card_mint']}; }}

.stack {{ display: flex; flex-direction: column; gap: 4mm; margin-top: 4mm; }}
.improve-card {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 12px; padding: 5mm 6mm; box-shadow: 0 8px 22px rgba(24,53,43,0.05); }}
.improve-card .label {{ font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 11.5px; color: {BRAND['teal']}; }}
.improve-card p {{ font-size: 10px; line-height: 1.55; color: {BRAND['muted']}; margin-top: 1.5mm; }}

.checklist {{ display: flex; flex-direction: column; gap: 2.5mm; margin-top: 3mm; }}
.checklist li {{ list-style: none; display: flex; gap: 3mm; font-size: 10.5px; line-height: 1.55; color: {BRAND['ink']}; }}
.checklist .dot {{ flex-shrink: 0; width: 5mm; height: 5mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 0.5mm; background: {BRAND['card_mint']}; color: {BRAND['teal']}; }}

.summary-box {{ background: #fff; border: 1px solid rgba(24,53,43,0.08); border-radius: 14px; padding: 7mm 8mm; margin-top: 4mm; box-shadow: 0 10px 26px rgba(24,53,43,0.05); }}
.summary-box p {{ font-size: 10.5px; line-height: 1.75; color: {BRAND['ink']}; }}

.caption-card {{ background: {BRAND['dark']}; border-radius: 14px; padding: 7mm 8mm; margin-top: 4mm; }}
.caption-card .handle {{ font-family: 'JetBrains Mono', monospace; font-size: 9px; color: {BRAND['orange']}; text-transform: uppercase; letter-spacing: 0.08em; }}
.caption-card p {{ font-size: 11px; line-height: 1.7; color: #f4f1ea; margin-top: 3mm; }}
"""


def build_header() -> str:
    return f"""
    <div class="report-head" style="display:flex; align-items:center; justify-content:space-between; margin-bottom:9mm;">
      <div class="logo-row">{LOGO_SVG}<span class="logo-wordmark" style="color:{BRAND['teal']};">We Forge Web</span></div>
      <span class="who mono" style="font-size:10px; color:{BRAND['muted']};">{CLIENT['business_name']} | Case Study</span>
    </div>
    """


def build_cover() -> str:
    """Condensed newsstand masthead (see brand_kit.py .mag-masthead CSS), sized to
    leave room for the overview/problem/strategy content below it on the same
    page, unlike the audit report's full mag-cover which is its own page."""
    content = f"""
    <div class="mag-masthead" style="min-height:92mm;">
      <div class="mag-masthead-top">
        <div class="brand-lock">{LOGO_SVG}<span class="word">We Forge Web</span></div>
        <div class="issue"><strong>Case Study</strong> &middot; {CASE_STUDY['status']}</div>
        <div class="site">{CONTACT['site']}</div>
      </div>
      <div class="mag-masthead-body" style="grid-template-columns:1fr;">
        <div class="mag-masthead-copy">
          <div class="kicker">{CASE_STUDY['industry']}</div>
          <div class="xl" style="font-size:64px;">{CLIENT['business_name']}</div>
          <p class="hook" style="max-width:150mm;">{CASE_STUDY['subtitle']}</p>
        </div>
      </div>
      <div class="mag-masthead-glow"></div>
    </div>
    <div class="mag-cover-meta" style="margin-top:0;">
      <div><div class="k">Industry</div><div class="v-sub">{CASE_STUDY['industry']}</div></div>
      <div><div class="k">Project type</div><div class="v-sub">{CASE_STUDY['project_type']}</div></div>
      <div><div class="k">Website</div><div class="v-sub">{CLIENT['domain']}</div></div>
      <div><div class="k">Status</div><div class="v-sub">{CASE_STUDY['status']}</div></div>
    </div>
    <div class="pad" style="padding-top:10mm;">
      <span class="tag tag-teal">Project overview</span>
      <p class="body-text" style="margin-top:3mm;">{CASE_STUDY['overview']}</p>
      <div class="callout" style="margin-top:6mm;">
        <h4>The main problem</h4>
        <p>{CASE_STUDY['main_problem']}</p>
      </div>
      <span class="tag tag-orange" style="margin-top:6mm;">Strategy</span>
      <p class="body-text" style="margin-top:3mm;">{CASE_STUDY['strategy']}</p>
    </div>
    """
    return shell(content, footer_left="We Forge Web | Built to Be Found. Built to Last.")


def build_close() -> str:
    """Inviting magazine endpaper, matching the audit report's back-page treatment
    (see brand_kit.py .close-invite-* CSS)."""
    qr_src = qr_data_uri(f"https://{CONTACT['site']}")
    return f"""
    <section class="page close-invite">
      <div class="close-invite-ghost">Next.</div>
      <div class="close-invite-inner">
        <div class="close-invite-mast">
          <span class="brand">We Forge Web</span>
          <span>End matter</span>
          <span>{CONTACT['site']}</span>
        </div>
        <div class="close-invite-kicker">Ready when you are</div>
        <div class="close-invite-mega">Want results<br/><span class="accent">like this?</span></div>
        <p class="close-invite-body">Kung gusto niyo ng ganitong klaseng foundation para sa brand ninyo, kausapin lang kami. Simula sa isang honest audit, walang fake promises.</p>
        <div class="close-invite-grid">
          <div>
            <div class="k">Write / Call</div>
            <div class="v">{CONTACT['email']}<br/>{CONTACT['phone_display']}</div>
            <div class="k" style="margin-top:3.5mm;">Location</div>
            <div class="v">{CONTACT['location']}</div>
          </div>
          <div>
            <div class="quote">We don't just build websites. We build digital foundations that help local businesses be found, trusted, and chosen.</div>
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


def build_improvements() -> str:
    cards = "".join(
        f'<div class="improve-card"><div class="label">{label}</div><p>{detail}</p></div>'
        for label, detail in CASE_STUDY["improvements"]
    )
    content = f"""
    <div class="pad">
      {build_header()}
      <span class="tag tag-teal">What we improved or will improve</span>
      <h2 class="display" style="font-size:22px; margin-top:3mm;">The build, piece by piece.</h2>
      <div class="stack">{cards}</div>
    </div>
    """
    return shell(content)


def build_journey_and_seo() -> str:
    content = f"""
    <div class="pad">
      {build_header()}
      <span class="tag tag-orange">Customer journey</span>
      <h2 class="display" style="font-size:22px; margin-top:3mm;">From search to decision.</h2>
      <p class="body-text" style="margin-top:3mm;">{CASE_STUDY['customer_journey']}</p>

      <span class="tag tag-teal" style="margin-top:8mm;">SEO and Google readiness</span>
      <h3 style="font-size:14px; margin-top:3mm;">What "Google ready" actually means here.</h3>
      <p class="body-text" style="margin-top:3mm;">{CASE_STUDY['seo_readiness']}</p>

      <div class="callout teal" style="margin-top:8mm;">
        <h4>Safe strategic outcome</h4>
        <p>{CASE_STUDY['safe_outcome']}</p>
      </div>
    </div>
    """
    return shell(content)


def build_assets_and_summary() -> str:
    assets = "".join(f'<li><span class="dot">{ICON_CHECK}</span><span>{a}</span></li>' for a in CASE_STUDY["visual_assets"])
    content = f"""
    <div class="pad">
      {build_header()}
      <span class="tag tag-orange">Visual assets to use</span>
      <h2 class="display" style="font-size:22px; margin-top:3mm;">What to gather once assets are ready.</h2>
      <ul class="checklist">{assets}</ul>

      <span class="tag tag-teal" style="margin-top:8mm;">Portfolio summary</span>
      <h3 style="font-size:14px; margin-top:3mm;">Ready to drop into the We Forge Web portfolio.</h3>
      <div class="summary-box"><p>{CASE_STUDY['portfolio_summary']}</p></div>

      <span class="tag tag-orange" style="margin-top:8mm;">Social media caption</span>
      <div class="caption-card">
        <div class="handle">We Forge Web</div>
        <p>{CASE_STUDY['social_caption']}</p>
      </div>
    </div>
    """
    return shell(content)


def build_html() -> str:
    pages = [
        build_cover(),
        build_improvements(),
        build_journey_and_seo(),
        build_assets_and_summary(),
        build_close(),
    ]
    body = "\n".join(pages)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>We Forge Web | {CLIENT['business_name']} Case Study</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>{body}</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the client portfolio case study PDF.")
    parser.add_argument(
        "--out",
        type=Path,
        default=OUTPUT_DIR / f"{CLIENT['business_name'].replace(' ', '_')}_Case_Study.pdf",
        help="Output PDF path.",
    )
    args = parser.parse_args()
    render_pdf(build_html(), OUTPUT_DIR / "_case_study_source.html", args.out)
    print(f"Case study generated: {args.out}")


if __name__ == "__main__":
    main()
