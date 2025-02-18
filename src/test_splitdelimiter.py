import unittest
from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_with_code(self):
        node = TextNode("text with `code` in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "text with ")
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_with_unclosed_delimiter(self):
        node = TextNode("text with `unclosed code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_with_bold(self):
        node = TextNode("text with **bold** in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "text with ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_with_italic(self):
        node = TextNode("text with *italic* in it", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "text with ")
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[2].text, " in it")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
    
    def test_multiple_text_nodes(self):
        # Test with a list containing multiple nodes
        node1 = TextNode("text with `code`", TextType.TEXT)
        node2 = TextNode("and *italic*", TextType.TEXT)
        nodes = [node1, node2]
        # First split for code
        result1 = split_nodes_delimiter(nodes, "`", TextType.CODE)
        # Then split result for italic
        result2 = split_nodes_delimiter(result1, "*", TextType.ITALIC)
        self.assertEqual(len(result2), 6)  # Should have 5 nodes total

    def test_non_text_node_preserved(self):
        # Test that already-formatted nodes aren't changed
        node1 = TextNode("text with ", TextType.TEXT)
        node2 = TextNode("code", TextType.CODE)
        node3 = TextNode(" and *italic*", TextType.TEXT)
        nodes = [node1, node2, node3]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[1].text_type, TextType.CODE)  # Middle node preserved

    def test_extract_markdown_images(self):
        # Test case 1: Single image
        text1 = "![alt text](image.jpg)"
        assert extract_markdown_images(text1) == [("alt text", "image.jpg")]

        # Test case 2: Multiple images
        text2 = "![img1](url1.jpg) ![img2](url2.jpg)"
        assert extract_markdown_images(text2) == [("img1", "url1.jpg"), ("img2", "url2.jpg")]

        # Empty text
        text1 = "This is text with no images"
        assert extract_markdown_images(text1) == []
        
        # Mix of links and images
        text2 = "Here's a [link](url) and ![image](img.jpg)"
        assert extract_markdown_images(text2) == [("image", "img.jpg")]
        
        # Images with spaces
        text3 = "![my cool image](my photo.jpg)"
        assert extract_markdown_images(text3) == [("my cool image", "my photo.jpg")]

    def test_extract_markdown_links(self):
        # Empty text
        text1 = "This is text with no links"
        assert extract_markdown_links(text1) == []
        
        # Single link
        text2 = "Here's a [Boot.dev](https://boot.dev) link"
        assert extract_markdown_links(text2) == [("Boot.dev", "https://boot.dev")]
        
        # Multiple links
        text3 = "[Link1](url1) and [Link2](url2)"
        assert extract_markdown_links(text3) == [("Link1", "url1"), ("Link2", "url2")]
        
        # Mix of links and images
        text4 = "![image](img.jpg) and [link](url.com)"
        assert extract_markdown_links(text4) == [("link", "url.com")]
        
        # Links with spaces in text
        text5 = "[My cool website](https://example.com)"
        assert extract_markdown_links(text5) == [("My cool website", "https://example.com")]

if __name__ == "__main__":
    unittest.main()