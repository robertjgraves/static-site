import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
            md = """
        This is **bolded** paragraph




        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

class TestBlockTypeDetection(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Test invalid headings
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode goes here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        # Test invalid code block
        self.assertEqual(block_to_block_type("```not closed properly"), BlockType.PARAGRAPH)
    
    def test_quote(self):
        self.assertEqual(block_to_block_type(">Quote line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2"), BlockType.QUOTE)
    
    def test_quote_block(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2"), BlockType.QUOTE)
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item\n3. Wrong"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()