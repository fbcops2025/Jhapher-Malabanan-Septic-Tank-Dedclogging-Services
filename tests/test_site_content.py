from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class SiteContentTest(unittest.TestCase):
    def test_core_static_files_exist(self):
        for rel in [
            "index.html",
            "services.html",
            "service-areas.html",
            "contact.html",
            "about.html",
            "styles.css",
            "robots.txt",
            "sitemap.xml",
            "vercel.json",
        ]:
            self.assertTrue((ROOT / rel).exists(), f"Missing {rel}")

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
        for rel in ["index.html", "services.html", "service-areas.html", "contact.html", "about.html"]:
            html = read(rel)
            self.assertIn('lang="tl-PH"', html)
            self.assertIn('rel="canonical"', html)
            self.assertIn('application/ld+json', html)
            self.assertIn('%2B639274374428', html)

    def test_contact_numbers_are_consistent_on_all_pages(self):
        for rel in ["index.html", "services.html", "service-areas.html", "contact.html", "about.html"]:
            html = read(rel)
            self.assertIn("0999 744 2521", html)
            self.assertIn("0977 206 8785", html)
            self.assertIn("0927 437 4428", html)


if __name__ == "__main__":
    unittest.main()
