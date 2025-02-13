import unittest
from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter

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

if __name__ == "__main__":
    unittest.main()