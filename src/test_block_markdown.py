import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


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

class TestMarkdownToHTML(unittest.TestCase):
    def test_single_paragraph(self):
        md = "This is **bold** and *italic* in a paragraph."
        
        node = markdown_to_html_node(md)
        #print(repr(node))
        #print(type(node))
        html = node.to_html()

        self.assertEqual(
            html, 
            "<div><p>This is <b>bold</b> and <i>italic</i> in a paragraph.</p></div>"
        )
    def test_headers(self):
        md = """
        # Heading 1
        ## Heading 2
        ### Heading 3
            """

        node = markdown_to_html_node(md)
        html = node.to_html()

        #print(repr(node))  # To examine the internal structure during debugging
        #print(html)        # To check the final HTML string

        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_code_blocks(self):
        # Test 1: Basic code block with backticks on separate lines
        md1 = """
        ```
        def hello_world():
        print("Hello, world!")
        ```
        """
        
        node1 = markdown_to_html_node(md1)
        html1 = node1.to_html()
        self.assertEqual(
            html1,
            "<div><pre><code>def hello_world():\n    print(\"Hello, world!\")</code></pre></div>"
        )

        # Test 2: Code block with markdown that should not be processed
        md2 = """
        ```
        This is text that *should* remain
        the **same** even with inline stuff
        ```
        """
        node2 = markdown_to_html_node(md2)
        html2 = node2.to_html()
        self.assertEqual(
            html2,
            "<div><pre><code>This is text that *should* remain\nthe **same** even with inline stuff</code></pre></div>"
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
        
    def test_unorderedlists(self):
        md = """
- This is a list
- with items
- and *more* items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul></div>",
        )
    
    def test_orderedlists(self):
        md = """
1. This is a list
2. with items
3. and *more* items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()