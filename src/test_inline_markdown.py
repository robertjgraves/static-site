import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image

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


class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        # Case with no links
        node = TextNode("No links here", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No links here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_one_link(self):
        # Case with one link
        node = TextNode("Check this [example](http://example.com)", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 3)
        
        self.assertEqual(result[0].text, "Check this ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "example")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://example.com")
        
        self.assertEqual(result[2].text, "")  # No trailing text after the link
        self.assertEqual(result[2].text_type, TextType.TEXT)

class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        # Case with no links
        node = TextNode("No links here", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No links here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_one_link(self):
        # Case with one link
        node = TextNode("Check this [example](http://example.com)", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 3)
        
        self.assertEqual(result[0].text, "Check this ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "example")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://example.com")
        
        self.assertEqual(result[2].text, "")  # No trailing text after the link
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_links(self):
        # Case with multiple links
        node = TextNode(
            "Look at [site1](http://site1.com) and [site2](http://site2.com).",
            TextType.TEXT,
        )
        result = split_nodes_link(node)
        self.assertEqual(len(result), 5)

        # First text part
        self.assertEqual(result[0].text, "Look at ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # First link part
        self.assertEqual(result[1].text, "site1")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://site1.com")

        # Middle text part
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)

        # Second link part
        self.assertEqual(result[3].text, "site2")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].url, "http://site2.com")

        # Final text part
        self.assertEqual(result[4].text, ".")
        self.assertEqual(result[4].text_type, TextType.TEXT)
    
    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_malformed_links(self):
        node = TextNode("This is broken [link](url", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is broken [link](url")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_back_to_back_links(self):
        node = TextNode(
            "[Link1](http://link1.com)[Link2](http://link2.com)",
            TextType.TEXT,
        )
        result = split_nodes_link(node)
        self.assertEqual(len(result), 2)

        # First Link
        self.assertEqual(result[0].text, "Link1")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "http://link1.com")

        # Second Link
        self.assertEqual(result[1].text, "Link2")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://link2.com")    

class TestSplitNodesImages(unittest.TestCase):
    # Case with no images
    def test_no_images(self):
        node = TextNode("No images here", TextType.TEXT)
        result = split_nodes_link(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No images here")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_one_image(self):
        # Case with one image
        node = TextNode("Check this ![example](http://example.com)", TextType.TEXT)
        result = split_nodes_image(node)
        self.assertEqual(len(result), 3)
        
        self.assertEqual(result[0].text, "Check this ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "example")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "http://example.com")
        
        self.assertEqual(result[2].text, "")  # No trailing text after the image
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_multiple_images(self):
        # Case with multiple images
        node = TextNode(
            "Look at ![site1](http://site1.com) and ![site2](http://site2.com).",
            TextType.TEXT,
        )
        result = split_nodes_image(node)
        self.assertEqual(len(result), 5)

        # First text part
        self.assertEqual(result[0].text, "Look at ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # First link part
        self.assertEqual(result[1].text, "site1")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "http://site1.com")

        # Middle text part
        self.assertEqual(result[2].text, " and ")
        self.assertEqual(result[2].text_type, TextType.TEXT)

        # Second link part
        self.assertEqual(result[3].text, "site2")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "http://site2.com")

        # Final text part
        self.assertEqual(result[4].text, ".")
        self.assertEqual(result[4].text_type, TextType.TEXT)
    
    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_malformed_image(self):
        node = TextNode("This is broken ![link](url", TextType.TEXT)
        result = split_nodes_image(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is broken ![link](url")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_back_to_back_images(self):
        node = TextNode(
            "![Link1](http://link1.com)![Link2](http://link2.com)",
            TextType.TEXT,
        )
        result = split_nodes_image(node)
        self.assertEqual(len(result), 2)

        # First Link
        self.assertEqual(result[0].text, "Link1")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "http://link1.com")

        # Second Link
        self.assertEqual(result[1].text, "Link2")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "http://link2.com")

if __name__ == "__main__":
    unittest.main()