import unittest

import src.python.add_news_update as mod


class TestAddNewsUpdate(unittest.TestCase):
    def test_build_content_keeps_english_summary_in_body(self):
        parsed = {
            "title": "Example title",
            "date": "2026-06-12",
            "summary": "English summary only.",
            "summary_fr": "Resume francais.",
        }

        content = mod._build_content(parsed)

        self.assertTrue(content.startswith("---\ntitle:"))
        self.assertIn('excerpt: "English summary only."', content)
        self.assertIn('excerpt_en: "English summary only."', content)
        self.assertIn("\nEnglish summary only.\n", content)
        self.assertNotIn("excerpt_fr:", content.split("---", 2)[-1])

    def test_build_content_treats_x_summary_as_title_only(self):
        parsed = {
            "title": "Example title",
            "date": "2026-06-12",
            "summary": "X",
            "summary_fr": "",
            "external_link": "https://example.com/update",
        }

        content = mod._build_content(parsed)

        self.assertTrue(content.startswith("---\ntitle:"))
        self.assertIn('excerpt: ""', content)
        self.assertIn('excerpt_en: ""', content)
        self.assertIn("[Read more](https://example.com/update)", content)
        self.assertNotIn("\nX\n", content)

    def test_build_fr_content_falls_back_to_english_summary_when_missing(self):
        parsed = {
            "title": "Example title",
            "title_fr": "Titre exemple",
            "date": "2026-06-12",
            "summary": "English summary only.",
            "summary_fr": "",
        }

        content = mod._build_fr_content(parsed)

        self.assertTrue(content.startswith("---\ntitle:"))
        self.assertIn('excerpt: "English summary only."', content)
        self.assertIn('excerpt_fr: "English summary only."', content)
        self.assertIn("\nEnglish summary only.\n", content)
