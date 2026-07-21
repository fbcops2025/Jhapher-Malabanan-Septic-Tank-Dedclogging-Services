from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://example.com"
PHONE_1 = "0999 744 2521"
PHONE_2 = "0977 206 8785"
VIBER = "0927 437 4428"

NAV = [
    ("Services", "services.html"),
    ("Service Areas", "service-areas.html"),
    ("Helpful Guides", "guides.html"),
    ("About", "about.html"),
    ("Contact", "contact.html"),
]

PAGES = {}


def icon(name):
    paths = {
        "tank": '<path d="M4 8h16v10H4z"/><path d="M8 8V5h8v3M8 12h8M12 12v6"/>',
        "drain": '<path d="M4 6h16M6 10h12M8 14h8M10 18h4"/>',
        "check": '<path d="m5 12 4 4L19 6"/>',
        "pin": '<path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.63a2 2 0 0 1-.45 2.11L8 9.73a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.85.29 1.73.5 2.63.62A2 2 0 0 1 22 16.92Z"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "home": '<path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10M9 20v-6h6v6"/>',
    }
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'


def cards(items, cls="three-col"):
    output = []
    for item in items:
        label, title, text, href = item
        link = f'<a class="text-link" href="{href}">Learn more <span>→</span></a>' if href else ""
        output.append(f'''<article class="card">
          <span class="card-label">{label}</span>
          <h3>{title}</h3>
          <p>{text}</p>{link}
        </article>''')
    return f'<div class="{cls}">' + "".join(output) + '</div>'


def process_steps(steps):
    return '<ol class="process">' + ''.join(
        f'<li><span>{i:02}</span><div><h3>{title}</h3><p>{text}</p></div></li>'
        for i, (title, text) in enumerate(steps, 1)
    ) + '</ol>'


def faq(items):
    return '<div class="faq">' + ''.join(
        f'<details><summary>{question}</summary><p>{answer}</p></details>'
        for question, answer in items
    ) + '</div>'


def area_links():
    return '''<div class="area-grid">
      <a href="metro-manila.html"><span>01</span><strong>Metro Manila</strong><small>Pasig, Makati, Taguig, Quezon City and more</small></a>
      <a href="rizal.html"><span>02</span><strong>Rizal</strong><small>Antipolo, Cainta, Taytay and nearby towns</small></a>
      <a href="cavite-laguna.html"><span>03</span><strong>Cavite and Laguna</strong><small>Selected cities and municipalities by confirmation</small></a>
    </div>'''


def page(slug, title, description, eyebrow, h1, intro, body, hero_image=None, schema_type="LocalBusiness"):
    path = "/" if slug == "index" else f"/{slug}"
    image = hero_image or "assets/images/hero-service.webp"
    nav = ''.join(f'<a href="{href}" data-page="{href[:-5]}">{label}</a>' for label, href in NAV)
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title if schema_type == "Article" else "Jhapher Malabanan Septic Tank & Declogging Services",
        "url": f"{DOMAIN}{path}",
        "image": f"{DOMAIN}/assets/images/hero-service.webp",
    }
    if schema_type == "LocalBusiness":
        schema.update({
            "telephone": ["+639997442521", "+639772068785", "+639274374428"],
            "areaServed": ["Metro Manila", "Rizal", "Cavite", "Laguna", "Bulacan"],
            "makesOffer": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Septic tank siphoning"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Pozo negro cleaning"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Declogging"}},
            ],
        })
    else:
        schema.update({"description": description, "author": {"@type": "Organization", "name": "Jhapher Malabanan"}})
    html = f'''<!doctype html>
<html lang="tl-PH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{DOMAIN}{path}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{DOMAIN}/assets/images/hero-service.webp">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#071a2c">
  <link rel="icon" type="image/png" href="favicon.png">
  <link rel="apple-touch-icon" href="favicon.png">
  <link rel="preload" href="styles.css" as="style">
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  <script src="site.js" defer></script>
</head>
<body data-page="{slug}">
  <a class="skip-link" href="#content">Skip to content</a>
  <div class="utility"><div class="shell"><span>Pasig City-based service coordination</span><span>Call {PHONE_1} · {PHONE_2} · Viber {VIBER}</span></div></div>
  <header class="site-header">
    <div class="shell nav-wrap">
      <a class="brand" href="index.html" aria-label="Jhapher Malabanan home"><span><strong>Jhapher Malabanan</strong><small>Septic Tank and Declogging Services</small></span></a>
      <button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav"><span></span><span></span><span></span><b>Menu</b></button>
      <nav id="primary-nav" class="primary-nav" aria-label="Primary navigation">{nav}<a class="nav-cta" href="contact.html">Request assessment</a></nav>
    </div>
  </header>
  <main id="content">
    <section class="page-hero {'home-hero' if slug == 'index' else ''}">
      <img class="hero-image" src="{image}" alt="Professional septic and declogging service concept" width="1600" height="900" fetchpriority="high">
      <div class="hero-shade"></div>
      <div class="shell hero-content">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p>{intro}</p>
        <div class="hero-actions"><a class="button button-primary" href="tel:09997442521">{icon('phone')} Call {PHONE_1}</a><a class="button button-light" href="viber://chat?number=%2B639274374428">Request an assessment</a></div>
        <div class="hero-proof"><span>{icon('pin')} Pasig-centered</span><span>{icon('home')} Residential & commercial</span><span>{icon('clock')} Schedule by confirmation</span></div>
      </div>
    </section>
{body}
  </main>
  <section class="closing-cta">
    <div class="shell closing-grid"><div><span class="eyebrow dark">Clear next step</span><h2>Tell us what is happening. We will help identify the right service.</h2><p>Send your city or barangay, a short description, and clear photos when safe. For urgent overflow or backup, call first.</p></div><div class="closing-actions"><a class="button button-primary" href="tel:09997442521">Call {PHONE_1}</a><a class="button button-outline" href="tel:09772068785">Call {PHONE_2}</a><a class="button button-outline" href="viber://chat?number=%2B639274374428">Viber {VIBER}</a></div></div>
  </section>
  <footer class="site-footer">
    <div class="shell footer-grid"><div class="footer-brand"><strong>JHAPHER</strong><p>Septic tank siphoning, pozo negro cleaning, and declogging services centered in Pasig and coordinated across listed service areas.</p></div><div><h2>Services</h2><a href="septic-tank-siphoning.html">Septic tank siphoning</a><a href="pozo-negro-cleaning.html">Pozo negro cleaning</a><a href="declogging-services.html">Declogging services</a></div><div><h2>Coverage</h2><a href="metro-manila.html">Metro Manila</a><a href="rizal.html">Rizal</a><a href="cavite-laguna.html">Cavite and Laguna</a></div><div><h2>Contact</h2><a href="tel:09997442521">{PHONE_1}</a><a href="tel:09772068785">{PHONE_2}</a><a href="viber://chat?number=%2B639274374428">Viber {VIBER}</a></div></div>
    <div class="shell legal"><span>© Jhapher Malabanan Services</span><span>Availability, access, scope, and estimate are confirmed before service.</span></div>
  </footer>
  <div class="mobile-actions"><a href="tel:09997442521">Call now</a><a href="viber://chat?number=%2B639274374428">Viber</a></div>
</body>
</html>'''
    PAGES[f"{slug}.html"] = html


home_body = f'''
<section class="trust-strip"><div class="shell"><span>SEPTIC SIPHONING</span><span>POZO NEGRO CLEANING</span><span>DRAIN DECLOGGING</span><span>AREA ASSESSMENT</span></div></section>
<section class="section section-light"><div class="shell"><div class="section-heading"><span class="kicker">The right response starts with the right diagnosis</span><h2>Practical help for the problems property owners cannot ignore.</h2><p>Slow drains, foul odors, wastewater backup, and full tanks can look similar. A clear assessment helps prevent the wrong service, wasted time, and repeat disruption.</p></div>{cards([
('FULL OR OVERDUE TANK', 'Septic tank siphoning', 'Removal of accumulated septic waste for homes, apartments, offices, and commercial properties, with access and scope checked before scheduling.', 'septic-tank-siphoning.html'),
('ODOR OR WASTE BUILDUP', 'Pozo negro cleaning', 'Assessment and cleaning support for pozo negro systems showing odor, overflow, or maintenance concerns.', 'pozo-negro-cleaning.html'),
('SLOW OR BLOCKED FLOW', 'Professional declogging', 'Targeted help for blocked toilets, floor drains, sinks, and drainage lines, including guidance when the issue may be deeper.', 'declogging-services.html'),
])}</div></section>
<section class="section section-dark"><div class="shell media-grid"><div class="media-copy"><span class="kicker">Know what is below the property</span><h2>A septic system works quietly until warning signs appear.</h2><p>Wastewater enters the tank, solids settle, and liquid continues to the next stage of the system. When buildup becomes excessive, normal flow can slow down and the property may experience odor, backup, or overflow.</p><ul class="check-list"><li>{icon('check')} Slow flushing across more than one fixture</li><li>{icon('check')} Persistent odor near drains or access points</li><li>{icon('check')} Gurgling, wastewater return, or wet areas</li></ul><a class="button button-light" href="septic-tank-warning-signs.html">Read the warning-sign guide</a></div><figure class="feature-image"><img src="assets/images/septic-system.webp" alt="Illustrated cutaway of a residential septic system" width="1600" height="900" loading="lazy"><figcaption>Concept illustration for customer education. Actual systems and access points vary by property.</figcaption></figure></div></section>
<section class="section"><div class="shell"><div class="section-heading compact"><span class="kicker">A simple, professional process</span><h2>How the service works</h2></div>{process_steps([
('Share the location and symptoms', 'Tell us the city or barangay, property type, and what you notice. Photos or a short video can help when safe.'),
('Confirm the likely service', 'The initial details help distinguish tank maintenance, pozo negro cleaning, and a drainage blockage.'),
('Check access and schedule', 'Access point, equipment approach, area availability, and preferred timing are confirmed before dispatch.'),
('Complete the agreed scope', 'The team attends to the confirmed work and explains any next step if another issue is discovered.'),
])}</div></section>
<section class="section section-sand"><div class="shell"><div class="section-heading"><span class="kicker">Coverage with local relevance</span><h2>Service coordination across key Luzon markets.</h2><p>Pasig is the center area. Metro Manila, Rizal, Cavite, Laguna, Bulacan, and selected extended locations are handled based on schedule and practical travel access.</p></div>{area_links()}<a class="text-link prominent" href="service-areas.html">View the complete service-area guide <span>→</span></a></div></section>
<section class="section"><div class="shell"><div class="section-heading"><span class="kicker">Useful before you book</span><h2>Helpful guides for cleaner decisions.</h2><p>Clear, plain-language answers for Filipino homeowners, property managers, and businesses dealing with septic and drainage concerns.</p></div>{cards([
('HOMEOWNER GUIDE', 'Warning signs your septic tank may need attention', 'Learn which symptoms point to a full tank, a blocked line, or a problem that needs closer assessment.', 'septic-tank-warning-signs.html'),
('SERVICE GUIDE', 'Siphoning, cleaning, or declogging?', 'Understand the difference so you can describe the problem clearly and request the right help.', 'services.html'),
('BOOKING GUIDE', 'What to prepare before requesting an estimate', 'A short checklist can make the first call faster and the assessment more useful.', 'contact.html'),
])}</div></section>
'''
page("index", "Septic Tank Siphoning & Declogging in Metro Manila | Jhapher", "Professional septic tank siphoning, pozo negro cleaning, and declogging centered in Pasig and serving Metro Manila, Rizal, Cavite, Laguna, and nearby areas.", "Pasig City-based · Serving key Philippine areas", "Septic and drainage problems, handled with a clearer next step.", "Baradong CR, slow drains, odor, or a full-tank concern? For homes, apartments, offices, and commercial properties, tell us the symptoms and location so the right service can be assessed before scheduling.", home_body)

services_body = f'''
<section class="section"><div class="shell"><div class="section-heading"><span class="kicker">Choose by symptom, not guesswork</span><h2>Three core services. One clear assessment path.</h2><p>The visible symptom does not always reveal the source. A blocked toilet may come from a local drain obstruction, while several slow fixtures can point to a fuller system issue.</p></div>{cards([
('SERVICE 01', 'Septic tank siphoning', 'For tank maintenance, reduced capacity, overflow warning signs, and properties where the septic system has not been serviced for a long period.', 'septic-tank-siphoning.html'),
('SERVICE 02', 'Pozo negro cleaning', 'For odor, waste buildup, and pozo negro maintenance concerns where the access and condition must be checked first.', 'pozo-negro-cleaning.html'),
('SERVICE 03', 'Declogging services', 'For toilets, sinks, floor drains, and drainage lines that are slow, blocked, gurgling, or backing up.', 'declogging-services.html'),
])}</div></section>
<section class="section section-dark"><div class="shell media-grid"><figure class="feature-image"><img src="assets/images/declogging-equipment.webp" alt="Professional drain inspection and declogging equipment" width="1600" height="900" loading="lazy"><figcaption>Concept service image. Equipment used depends on the actual blockage and site access.</figcaption></figure><div class="media-copy"><span class="kicker">Describe what you observe</span><h2>Not sure which service you need?</h2><p>Start with the symptoms. Tell us whether one fixture or several are affected, whether water returns, whether there is odor, and when the issue began.</p><ul class="check-list"><li>{icon('check')} One blocked fixture may be a local clog</li><li>{icon('check')} Several slow drains may indicate a deeper issue</li><li>{icon('check')} Overflow or strong odor needs prompt assessment</li></ul></div></div></section>
<section class="section"><div class="shell"><div class="section-heading compact"><span class="kicker">From first message to site visit</span><h2>How the service works</h2></div>{process_steps([('Send basic details', 'Location, property type, affected fixtures, symptoms, and photos if available.'),('Receive initial guidance', 'The team reviews whether siphoning, cleaning, or declogging is the likely next step.'),('Confirm practical details', 'Schedule, access point, service area, and job scope are discussed before attendance.'),('Proceed with the agreed service', 'Work is completed based on the confirmed issue and actual site conditions.')])}</div></section>
'''
page("services", "Septic, Pozo Negro & Declogging Services | Jhapher Malabanan", "Compare septic tank siphoning, pozo negro cleaning, and professional declogging services for homes and businesses across Metro Manila and nearby areas.", "Services explained clearly", "The right service starts with understanding the real problem.", "Explore the core services, common warning signs, and information that helps the team assess your property more accurately.", services_body, "assets/images/septic-system.webp")

service_specs = {
"septic-tank-siphoning": ("Septic Tank Siphoning in Metro Manila | Jhapher Malabanan", "Septic tank siphoning for homes, apartments, and commercial properties in Metro Manila, Rizal, Cavite, Laguna, and selected nearby areas.", "Septic tank siphoning", "Restore working capacity before a full tank becomes a property emergency.", "Siphoning removes accumulated liquid and solid waste from accessible septic tanks. The right timing depends on usage, tank size, maintenance history, and warning signs.", "assets/images/septic-system.webp", [
('When it may be needed', 'Multiple slow drains, persistent odor, wastewater backup, wet areas near the tank, or a long gap since the last service.'),
('What affects the scope', 'Tank accessibility, hose distance, property type, estimated volume, and whether another drainage issue is present.'),
('What to prepare', 'Exact location, access-point photo, property type, known tank details, and a description of recent symptoms.'),
]),
"pozo-negro-cleaning": ("Pozo Negro Cleaning Services | Metro Manila & Nearby Areas", "Pozo negro cleaning and waste-removal assessment for residential and commercial properties across Metro Manila, Rizal, and nearby service areas.", "Pozo negro cleaning", "A cleaner response to odor, buildup, and overflow concerns.", "Pozo negro systems can develop odor, reduced capacity, and overflow risk as waste accumulates. An initial assessment helps determine access, likely volume, and whether cleaning or another service is appropriate.", "assets/images/hero-service.webp", [
('Common concerns', 'Strong odor, visible overflow, slow wastewater movement, or maintenance that has been delayed.'),
('Assessment first', 'The team checks location, access, property use, and available details before recommending the next step.'),
('For different properties', 'Homes, rental properties, food businesses, offices, and other sites may have different usage and access needs.'),
]),
"declogging-services": ("Declogging Services in Metro Manila | Toilet, Drain & Sewer Help", "Professional declogging assessment for blocked toilets, floor drains, sinks, and drainage lines in Metro Manila, Rizal, and nearby areas.", "Drain and toilet declogging", "Clear the blockage. Understand what caused it. Reduce repeat disruption.", "Professional declogging begins by identifying whether the obstruction is limited to one fixture, affects a branch line, or may connect to a larger septic or sewer concern.", "assets/images/declogging-equipment.webp", [
('Typical symptoms', 'Slow drainage, standing water, gurgling sounds, repeated toilet blockage, foul odor, or water returning through another drain.'),
('Useful details', 'Which fixtures are affected, when the problem started, what has already been tried, and whether several areas are backing up.'),
('When siphoning may be involved', 'If multiple fixtures are affected or the septic system is full, clearing one drain may not solve the root problem.'),
]),
}
for slug, (title, desc, eyebrow, h1, intro, image, items) in service_specs.items():
    body = f'''<section class="section"><div class="shell"><div class="section-heading"><span class="kicker">Understand the service</span><h2>What property owners should know</h2></div>{cards([(f'0{i}', a, b, None) for i,(a,b) in enumerate(items,1)])}</div></section>
<section class="section section-sand"><div class="shell split-content"><div><span class="kicker">A better first call</span><h2>Information that helps us assess the job</h2><p>Share your city or barangay, property type, problem symptoms, safe photos of the affected area or access point, and preferred schedule. Clear details support a more useful conversation before dispatch.</p><a class="button button-dark" href="contact.html">Prepare your request</a></div><div>{process_steps([('Describe the issue', 'Explain what you see, smell, or hear and how many fixtures are affected.'),('Show the access', 'Send a photo of the manhole, drain, or work area when safe.'),('Confirm the scope', 'Location, practical access, and likely service are discussed before scheduling.')])}</div></div></section>
<section class="section"><div class="shell"><div class="section-heading compact"><span class="kicker">Service coverage</span><h2>Available across listed areas by confirmation</h2></div>{area_links()}</div></section>'''
    page(slug, title, desc, eyebrow, h1, intro, body, image)

areas_body = f'''
<section class="section"><div class="shell"><div class="section-heading"><span class="kicker">Pasig-centered operations</span><h2>Check the service guide for your area.</h2><p>Availability depends on the job, team schedule, access, and travel practicality. Send your exact city or barangay so the team can confirm coverage before you make plans.</p></div>{area_links()}</div></section>
<section class="section section-sand"><div class="shell area-detail"><div><h2>Metro Manila / NCR</h2><p>Pasig City, Makati, Taguig, Mandaluyong, Quezon City, Caloocan, Marikina City, Las Piñas, Greenhills, and other NCR locations by confirmation.</p></div><div><h2>Rizal Area</h2><p>Antipolo City, Cainta, Taytay, Angono, Binangonan, Cardona, Morong, Baras, Teresa, Tanay, Pililla, San Mateo, and Montalban.</p></div><div><h2>Nearby areas</h2><p>Selected locations in Bulacan, Cavite, and Laguna. Cagayan de Oro and Misamis Occidental remain extended areas that require advance confirmation.</p></div></div></section>
<section class="section"><div class="shell"><div class="section-heading compact"><span class="kicker">Before requesting a schedule</span><h2>Send these three details</h2></div>{cards([('01', 'Exact location', 'City, barangay, subdivision or building, and a useful nearby landmark.', None),('02', 'Service concern', 'Septic maintenance, odor, overflow, blocked toilet, slow drain, or another visible symptom.', None),('03', 'Access information', 'Photo of the manhole or affected drain and any parking or equipment-access concern.', None)])}</div></section>
'''
page("service-areas", "Septic & Declogging Service Areas | Metro Manila, Rizal & Nearby", "Check septic siphoning, pozo negro cleaning, and declogging coverage across Metro Manila, Rizal, Cavite, Laguna, Bulacan, and extended areas.", "Service areas", "Local coordination across Metro Manila and nearby growth areas.", "Pasig City is the center area, with service availability across listed NCR cities, Rizal municipalities, and selected nearby provinces by confirmation.", areas_body)

area_specs = {
"metro-manila": ("Septic Siphoning & Declogging in Metro Manila | Jhapher", "Septic tank siphoning, pozo negro cleaning, and declogging in Pasig, Makati, Taguig, Quezon City, Mandaluyong, Marikina, and NCR.", "Metro Manila service guide", "Septic and declogging support for busy NCR properties.", "From family homes and apartment buildings to offices and commercial spaces, Metro Manila properties need clear coordination around access, traffic, timing, and the actual source of the problem.", "Pasig, Makati, Taguig, Mandaluyong, Quezon City, Caloocan, Marikina City, Las Piñas, and other NCR locations by confirmation."),
"rizal": ("Septic Siphoning & Declogging in Rizal | Jhapher Malabanan", "Septic siphoning, pozo negro cleaning, and declogging across Antipolo, Cainta, Taytay, Angono, Binangonan, and other Rizal areas.", "Rizal service guide", "Practical septic and drainage help across Rizal communities.", "Fast-growing subdivisions, older homes, rental properties, and commercial sites can have very different septic access and drainage layouts. Photos and exact location help the assessment.", "Antipolo City, Cainta, Taytay, Angono, Binangonan, Cardona, Morong, Baras, Teresa, Tanay, Pililla, San Mateo, and Montalban."),
"cavite-laguna": ("Septic & Declogging Services in Cavite and Laguna | Jhapher", "Request septic tank siphoning, pozo negro cleaning, and declogging assessment in selected Cavite and Laguna locations by schedule confirmation.", "Cavite and Laguna service guide", "Septic and drainage service for selected Cavite and Laguna areas.", "Coverage is coordinated based on the exact location, job type, schedule, and practical travel access. Send details first so availability can be checked before an appointment is discussed.", "Selected Cavite and Laguna cities and municipalities are served by confirmation. Exact barangay and a nearby landmark help the team assess travel and timing."),
}
for slug, (title, desc, eyebrow, h1, intro, locations) in area_specs.items():
    body = f'''<section class="section"><div class="shell split-content"><div><span class="kicker">Coverage overview</span><h2>Areas commonly discussed</h2><p>{locations}</p><p class="note-block">Coverage is not implied automatically. Team schedule, service type, equipment access, and travel conditions are confirmed for every request.</p></div><div><span class="kicker">Services available</span>{cards([('01','Septic tank siphoning','For maintenance, buildup, reduced capacity, and full-tank warning signs.','septic-tank-siphoning.html'),('02','Pozo negro cleaning','For odor, overflow, and waste-accumulation concerns.','pozo-negro-cleaning.html'),('03','Declogging','For blocked toilets, drains, and wastewater lines.','declogging-services.html')], 'stacked-cards')}</div></div></section>
<section class="section section-sand"><div class="shell"><div class="section-heading compact"><span class="kicker">How the service works</span><h2>Plan the visit with fewer surprises</h2></div>{process_steps([('Send your exact location', 'Include city, barangay, property or subdivision name, and a useful landmark.'),('Explain the problem', 'Describe symptoms, affected fixtures, and how long the issue has been present.'),('Show practical access', 'Share safe photos of the manhole, drain, driveway, parking, or narrow access.'),('Confirm availability', 'The team discusses the likely service and schedule based on the details provided.')])}</div></section>'''
    page(slug, title, desc, eyebrow, h1, intro, body)

guides_body = f'''
<section class="section"><div class="shell"><div class="section-heading"><span class="kicker">Straight answers for property owners</span><h2>Helpful guides, written around real customer questions.</h2><p>These resources are designed to help you recognize warning signs, prepare useful information, and avoid choosing a service based on guesswork.</p></div>{cards([('FEATURED GUIDE','Warning signs your septic tank may need attention','A plain-language guide to slow drains, odors, gurgling, wet ground, overflow, and when a local clog may be the real issue.','septic-tank-warning-signs.html'),('SERVICE EXPLAINER','Siphoning versus declogging','Learn why a blocked toilet is not always a full septic tank and why several affected fixtures can signal a deeper concern.','services.html'),('BOOKING CHECKLIST','Prepare for a faster assessment','Know which location, access, symptom, and property details help the team give a clearer next step.','contact.html')])}</div></section>
<section class="section section-dark"><div class="shell editorial-quote"><span>GOOD PROPERTY CARE</span><blockquote>Acting early is often less disruptive than waiting for wastewater to return, odor to worsen, or access to become an emergency.</blockquote><a class="button button-light" href="contact.html">Request an assessment</a></div></section>
'''
page("guides", "Septic Tank & Declogging Guides for Filipino Property Owners", "Helpful septic tank and declogging guides covering warning signs, service choices, booking preparation, and property care in the Philippines.", "Helpful guides", "Better decisions begin with understanding the warning signs.", "Practical, easy-to-read guidance for homeowners, landlords, building managers, and business owners dealing with septic and drainage concerns.", guides_body, "assets/images/septic-system.webp")

article_body = f'''
<section class="article-layout section"><article class="article shell"><p class="article-lead">A septic system usually gives clues before a serious backup. The challenge is that some signs can also come from a local drain blockage. Looking at the pattern across the property helps you describe the problem more accurately.</p>
<h2>1. More than one drain is moving slowly</h2><p>One slow sink can be a local obstruction. When toilets, floor drains, and sinks begin slowing at the same time, the issue may involve a larger wastewater line or reduced septic capacity.</p>
<h2>2. Toilets gurgle or water returns elsewhere</h2><p>Gurgling can happen when air is displaced inside a restricted line. Water that rises in a floor drain while another fixture is used is an important detail to report during assessment.</p>
<figure><img src="assets/images/septic-system.webp" alt="Concept illustration of a home septic system and service access" width="1600" height="900" loading="lazy"><figcaption>A concept diagram of a residential system. Actual tank design, pipe layout, and access vary.</figcaption></figure>
<h2>3. Persistent wastewater odor develops</h2><p>A recurring smell near drains, the yard, or an access point deserves attention. It can be connected to drainage traps, venting, waste buildup, or a septic concern. Location and timing help narrow the possibilities.</p>
<h2>4. Wet ground appears near the system</h2><p>Unexpected wet or unusually green areas can indicate excess moisture. Avoid opening or entering any tank. Keep people away from unsafe areas and request professional assessment.</p>
<h2>5. Wastewater begins to back up</h2><p>Backup is the clearest reason to stop using affected fixtures where practical and call. Tell the team which fixtures are involved and whether the return is clear water or wastewater.</p>
<div class="article-callout"><h2>Siphoning or declogging?</h2><p>If only one fixture is blocked, declogging may be the likely starting point. If several fixtures are affected, the tank is overdue for maintenance, or there are odor and overflow signs, septic assessment may also be needed.</p><a class="button button-dark" href="services.html">Compare the services</a></div>
<h2>What to send when requesting help</h2><ul><li>Exact city, barangay, and property type</li><li>Which fixtures are affected</li><li>When symptoms began and whether they are getting worse</li><li>Safe photos of the access point or affected drain</li><li>Any known maintenance history</li></ul>
</article></section>
<section class="section section-sand"><div class="shell"><div class="section-heading compact"><span class="kicker">How the service works</span><h2>From warning sign to clear next step</h2></div>{process_steps([('Observe the pattern','Note whether one or several fixtures are affected.'),('Share useful evidence','Send the location, symptoms, and safe photos.'),('Confirm the likely service','Discuss whether siphoning, cleaning, or declogging is the practical next step.')])}</div></section>
'''
page("septic-tank-warning-signs", "5 Septic Tank Warning Signs Filipino Property Owners Should Know", "Learn five septic tank warning signs, how they differ from a local drain clog, and what details to prepare before requesting service.", "Homeowner education", "Five warning signs your septic system may need attention.", "Slow drains and odors are easy to ignore until they become disruptive. Here is how to read the pattern and know what information to prepare.", article_body, "assets/images/septic-system.webp", "Article")

about_body = f'''
<section class="section"><div class="shell split-content"><div><span class="kicker">A more professional service experience</span><h2>Clear communication before equipment arrives.</h2><p>Jhapher Malabanan is presented as a Pasig-centered septic and declogging service for households, property managers, and businesses across listed areas. The website is built around practical customer questions: What is wrong? Which service fits? Is the area covered? What should be prepared?</p><p>That approach helps customers move from worry to a useful next step without unsupported promises or confusing technical language.</p></div><div class="principles"><div><strong>01</strong><h3>Problem-first guidance</h3><p>Start with symptoms and property details before naming the service.</p></div><div><strong>02</strong><h3>Honest service scope</h3><p>Access, location, timing, and work requirements are confirmed for each request.</p></div><div><strong>03</strong><h3>Useful preparation</h3><p>Customers know what information and safe photos can improve the assessment.</p></div></div></div></section>
<section class="section section-dark"><div class="shell editorial-quote"><span>OUR SERVICE STANDARD</span><blockquote>Professional does not need to mean complicated. It means a clear response, a clear scope, and a clear next step.</blockquote><a class="button button-light" href="contact.html">Request an assessment</a></div></section>
'''
page("about", "About Jhapher Malabanan | Septic & Declogging Service", "Learn about Jhapher Malabanan, a Pasig-centered septic tank, pozo negro, and declogging service coordinating work across listed Philippine areas.", "About the service", "Built around clarity, practical assessment, and direct communication.", "For property owners dealing with an unpleasant and urgent problem, a professional experience starts before the site visit.", about_body)

contact_body = f'''
<section class="section"><div class="shell contact-grid"><div><span class="kicker">Direct contact</span><h2>Choose the fastest contact path for your situation.</h2><div class="contact-cards"><a href="tel:09997442521"><small>Primary call</small><strong>{PHONE_1}</strong><span>Tap to call →</span></a><a href="tel:09772068785"><small>Second call line</small><strong>{PHONE_2}</strong><span>Tap to call →</span></a><a href="viber://chat?number=%2B639274374428"><small>Send details on Viber</small><strong>{VIBER}</strong><span>Open Viber →</span></a></div></div><div class="request-card"><span class="kicker">Prepare your request</span><h2>Four details make the assessment more useful.</h2>{process_steps([('Location','City, barangay, subdivision or building, and landmark.'),('Symptoms','Slow drain, odor, gurgling, blockage, overflow, or full-tank concern.'),('Property','Home, apartment, office, restaurant, shop, or another site type.'),('Access','Safe photo of the manhole, drain, driveway, or work area.')])}</div></div></section>
<section class="section section-sand"><div class="shell"><div class="section-heading compact"><span class="kicker">Before you call</span><h2>Frequently asked questions</h2></div>{faq([('How is an estimate determined?','Location, likely service, tank or blockage conditions, access, property type, and actual work scope can affect the estimate. Share details first for a more useful assessment.'),('Can service be scheduled on the same day?','Availability depends on team schedule, location, job type, and access. Call first when the problem is urgent.'),('What if I do not know whether I need siphoning or declogging?','Describe which fixtures are affected and whether there is odor, gurgling, overflow, or wastewater return. The team can suggest the practical next step.'),('Is my area covered?','Pasig is the center area. Metro Manila, Rizal, Cavite, Laguna, Bulacan, and selected extended locations are handled by confirmation.')])}</div></section>
'''
page("contact", "Contact Jhapher Malabanan | Request Septic or Declogging Help", "Call or Viber Jhapher Malabanan to request septic siphoning, pozo negro cleaning, or declogging assessment and confirm service-area availability.", "Contact and assessment", "Send the right details. Get a clearer next step.", "For urgent overflow or wastewater backup, call first. For an assessment, send the exact location, symptoms, property type, and safe photos through Viber.", contact_body)

for filename, content in PAGES.items():
    (ROOT / filename).write_text(content, encoding="utf-8")

urls = ["/" if name == "index.html" else "/" + name[:-5] for name in PAGES]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url in urls:
    priority = "1.0" if url == "/" else "0.8"
    sitemap.append(f"  <url><loc>{DOMAIN}{url}</loc><priority>{priority}</priority></url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
print(f"Built {len(PAGES)} pages and sitemap.xml")
