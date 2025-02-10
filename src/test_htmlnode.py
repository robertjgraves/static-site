import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props=None)
        self.assertEqual(
            "", node.props_to_html()
        )
    
    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(
            ' href="https://boot.dev"', node.props_to_html()
        )
    
    def test_props_to_html_multiple(self):
        node = HTMLNode(props={
            "href": "https://boot.dev",
            "target": "_blank"
            })
        self.assertEqual(
            ' href="https://boot.dev" target="_blank"', node.props_to_html()
        )
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

class TestPropsToHTML(unittest.TestCase):
    def test_multiple_props(self):
        node = HTMLNode(tag="img", value=None, props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="An image"')

    def test_empty_props(self):
        node = HTMLNode(tag="img", value=None, props={})
        self.assertEqual(node.props_to_html(), '')

    def test_none_props(self):
        node = HTMLNode(tag="img", value=None, props=None)
        self.assertEqual(node.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()