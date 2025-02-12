import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_eq_false_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.BOLD, "http://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_eq_false_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == None
        assert html_node.value == "Hello, world!"
    
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == 'b'
        assert html_node.value == "Bold text"
    
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == 'i'
        assert html_node.value == "Italic text"
    
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == 'code'
        assert html_node.value == "Code text"
    
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click me", TextType.LINK, "http://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == 'a'
        assert html_node.value == "Click me"
        assert html_node.props == {"href": "http://www.boot.dev"}

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Alt image text", TextType.IMAGE, "http://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == 'img'
        assert html_node.value == ""
        assert html_node.props == {"src": "http://www.boot.dev", "alt": "Alt image text"}

    def test_text_node_to_html_node_invalid(self):
        # Create a text node with an invalid type
        text_node = TextNode("Some text", "invalid_type")
        
        # Use assertRaises instead of pytest.raises
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()