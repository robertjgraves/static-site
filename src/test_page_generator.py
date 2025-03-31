import unittest
from page_generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    
    def test_no_h1(self):
        with self.assertRaises(ValueError):
            extract_title("No header here")
    
    def test_only_h1(self):
        self.assertEqual(extract_title("#Header"), "Header")
    
    def test_other_headers(self):
        # Example with no h1, only h2 or higher
        with self.assertRaises(ValueError):
            extract_title("## Not an h1")