from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from content.blog_posts import BLOG_POSTS, get_post_slugs

CORE_PAGES = [
    "index.html",
    "services.html",
    "septic-tank-siphoning.html",
    "pozo-negro-cleaning.html",
    "declogging-services.html",
    "service-areas.html",
    "metro-manila.html",
    "rizal.html",
    "cavite-laguna.html",
    "guides.html",
    "blog.html",
    "about.html",
    "contact.html",
    *[f"{slug}.html" for slug in get_post_slugs()],
]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class SiteContentTest(unittest.TestCase):
    def test_core_static_files_exist(self):
        for rel in [
            *CORE_PAGES,
            "styles.css",
            "site.js",
            "robots.txt",
            "sitemap.xml",
            "vercel.json",
            "content/blog_posts.py",
        ]:
            self.assertTrue((ROOT / rel).exists(), f"Missing {rel}")

    def test_blog_library_has_expected_coverage(self):
        self.assertGreaterEqual(len(BLOG_POSTS), 20)
        html = read("blog.html")
        self.assertIn("Blog library", html)
        self.assertIn("practical guides", html)
        for post in BLOG_POSTS[:5]:
            self.assertIn(f'{post["slug"]}.html', html)

    def test_homepage_has_core_offer_and_contacts(self):
        html = read("index.html")
        required = [
            "Jhapher Malabanan",
            "Pasig City",
            "Septic tank siphoning",
            "Pozo negro cleaning",
            "Declogging",
            "0999 744 2521",
            "0977 206 8785",
            "0927 437 4428",
            "Baradong CR",
            "blog.html",
        ]
        for item in required:
            self.assertIn(item, html)

    def test_service_areas_are_grouped_and_include_confirmed_locations(self):
        html = read("service-areas.html")
        for item in [
            "Metro Manila / NCR",
            "Rizal Area",
            "Nearby areas",
            "Makati",
            "Taguig",
            "Quezon City",
            "Antipolo City",
            "Taytay",
            "Cagayan de Oro",
            "Misamis Occidental",
        ]:
            self.assertIn(item, html)

    def test_no_forbidden_overclaims_or_removed_words(self):
        combined = "\n".join(
            p.read_text(encoding="utf-8")
            for p in ROOT.glob("*.html")
        ).lower()
        forbidden = [
            "#1",
            "guaranteed",
            "licensed",
            "certified",
            "habwa",
            "suyop",
            "replace with approved",
            "proof section",
            "real proof wins",
            "problems customers usually search for",
            "simple lang dapat ang website",
        ]
        for word in forbidden:
            self.assertNotIn(word, combined)

    def test_seo_and_viber_basics_present(self):
        for rel in ["index.html", "services.html", "service-areas.html", "contact.html", "about.html", "blog.html"]:
            html = read(rel)
            self.assertIn('lang="tl-PH"', html)
            self.assertIn('rel="canonical"', html)
            self.assertIn('application/ld+json', html)
            self.assertIn('%2B639274374428', html)

    def test_contact_numbers_are_consistent_on_all_pages(self):
        for rel in CORE_PAGES:
            html = read(rel)
            self.assertIn("0999 744 2521", html)
            self.assertIn("0977 206 8785", html)
            self.assertIn("0927 437 4428", html)

    def test_every_page_has_unique_search_metadata_and_one_h1(self):
        titles = set()
        descriptions = set()
        for rel in CORE_PAGES:
            html = read(rel)
            self.assertEqual(html.count("<h1"), 1, f"{rel} must have one H1")
            self.assertIn('name="description"', html)
            self.assertIn('rel="canonical"', html)
            title = html.split("<title>", 1)[1].split("</title>", 1)[0]
            description = html.split('name="description" content="', 1)[1].split('"', 1)[0]
            self.assertNotIn(title, titles, f"Duplicate title: {title}")
            self.assertNotIn(description, descriptions, f"Duplicate description: {description}")
            titles.add(title)
            descriptions.add(description)

    def test_blog_articles_use_article_schema_and_checklists(self):
        for slug in get_post_slugs():
            html = read(f"{slug}.html")
            self.assertIn('"@type": "Article"', html)
            self.assertIn("Related reads", html)
            self.assertIn("How the service works", html)

    def test_premium_site_assets_and_conversion_paths_exist(self):
        combined = "\n".join(read(rel) for rel in CORE_PAGES)
        for rel in [
            "assets/images/hero-service.webp",
            "assets/images/septic-system.webp",
            "assets/images/declogging-equipment.webp",
        ]:
            self.assertTrue((ROOT / rel).exists(), f"Missing premium artwork {rel}")
            self.assertIn(rel, combined)
        for phrase in [
            "Request an assessment",
            "How the service works",
            "Helpful guides",
            "Metro Manila",
            "Rizal",
            "Cavite and Laguna",
            "Blog",
        ]:
            self.assertIn(phrase, combined)

    def test_header_and_footer_use_the_same_brand_format(self):
        for rel in CORE_PAGES:
            html = read(rel)
            self.assertEqual(html.count("<strong>Jhapher Malabanan</strong>"), 2, rel)
            self.assertEqual(
                html.count("<small>Septic Tank and Declogging Services</small>"),
                2,
                rel,
            )


if __name__ == "__main__":
    unittest.main()
