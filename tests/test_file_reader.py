import unittest

from src.file_reader import html_to_text


class FileReaderTest(unittest.TestCase):
    def test_html_to_text_preserves_links_as_markdown(self):
        text = html_to_text(
            '<main><p>Read <a href="https://example.com/post">this article</a>.</p></main>'
        )

        self.assertIn("[this article](https://example.com/post)", text)

    def test_html_to_text_omits_non_content_regions(self):
        text = html_to_text(
            """
            <html>
              <nav>Menu item</nav>
              <main><h1>Today Plus</h1><p>Useful insight</p></main>
              <footer>Copyright</footer>
              <script>alert("tracking")</script>
            </html>
            """
        )

        self.assertIn("Today Plus", text)
        self.assertIn("Useful insight", text)
        self.assertNotIn("Menu item", text)
        self.assertNotIn("Copyright", text)
        self.assertNotIn("tracking", text)


if __name__ == "__main__":
    unittest.main()
