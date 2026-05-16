import unittest

from src.summarizer import RuleBasedSummarizer


class RuleBasedSummarizerTest(unittest.TestCase):
    def test_extracts_limited_summary_from_headings_and_sentences(self):
        text = """
        # AI automation trend

        - Make.com workflows can connect lead capture and reporting.
        - Obsidian notes can become a reusable knowledge base.

        This content explains how local archiving helps operators reuse insights.
        Short.
        """

        summary = RuleBasedSummarizer(max_items=3).summarize(text)

        self.assertLessEqual(len(summary), 3)
        self.assertIn("Make.com workflows can connect lead capture and reporting.", summary)
        self.assertIn("Obsidian notes can become a reusable knowledge base.", summary)

    def test_extracts_keywords_by_frequency_without_stopwords(self):
        text = "AI automation automation Obsidian knowledge knowledge knowledge Make.com"

        keywords = RuleBasedSummarizer(max_keywords=4).extract_keywords(text)

        self.assertEqual(keywords[0], "knowledge")
        self.assertIn("automation", keywords)


if __name__ == "__main__":
    unittest.main()
