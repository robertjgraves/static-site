import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Hello")
            ]
        )
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")
    
    def test_parent_node_missing_tag(self):
        node = ParentNode(
            None,
            [LeafNode("p", "Hello")]
        )
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_node_missing_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_node_multiple_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "First"),
                LeafNode("p", "Second"),
                LeafNode("p", "Third")
            ]
        )
        self.assertEqual(node.to_html(), "<div><p>First</p><p>Second</p><p>Third</p></div>")

    def test_parent_node_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [LeafNode("p", "Nested")]
                )
            ]
        )
        self.assertEqual(node.to_html(), "<div><section><p>Nested</p></section></div>")

    def test_parent_node_mixed_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "Just text"),
                LeafNode("p", "Paragraph"),
                LeafNode(None, "More text")
            ]
        )
        self.assertEqual(node.to_html(), "<div>Just text<p>Paragraph</p>More text</div>")

    def test_parent_node_with_props(self):
    # Arrange: create a node with some props
        node = ParentNode(
            "a",
            [LeafNode("span", "Click me!")],
            {"href": "https://boot.dev"}
        )
        
        # Act: convert to HTML
        result = node.to_html()
        
        # Assert: check if the HTML is correct
        self.assertEqual(result, '<a href="https://boot.dev"><span>Click me!</span></a>')

    def test_parent_node_nested_with_props(self):
    # Arrange: create a complex nested structure with props
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "nav",
                    [
                        LeafNode("a", "Home", {"href": "/home", "class": "active"}),
                        LeafNode("a", "About", {"href": "/about"})
                    ],
                    {"class": "navbar"}
                )
            ],
            {"id": "main"}
        )
        
        # Act
        result = node.to_html()
        
        # Assert
        expected = '<div id="main"><nav class="navbar"><a href="/home" class="active">Home</a><a href="/about">About</a></nav></div>'
        self.assertEqual(result, expected)

    def test_parent_node_form_structure(self):
        # Arrange: Let's build a form
        node = ParentNode(
            "form",
            [
                # A label and input group
                ParentNode(
                    "div",
                    [
                        LeafNode("label", "Username:", {"for": "username"}),
                        # Remove the empty value for input
                        LeafNode("input", None, {"type": "text", "id": "username"})
                    ],
                    {"class": "form-group"}
                ),
                # A submit button
                LeafNode("button", "Submit", {"type": "submit"})
            ],
            {"action": "/submit", "method": "POST"}
        )
        
        # Act
        result = node.to_html()
        
        # Assert
        expected = '<form action="/submit" method="POST"><div class="form-group"><label for="username">Username:</label><input type="text" id="username"></div><button type="submit">Submit</button></form>'
        self.assertEqual(result, expected)
    
    def test_parent_node_article_structure(self):
        # Arrange: Create an article with header and paragraphs
        node = ParentNode(
            "article",
            [
                LeafNode("h1", "My First Blog Post", {"class": "title"}),
                LeafNode("p", "This is the first paragraph."),
                LeafNode("p", "This is the second paragraph.", {"class": "highlight"})
            ],
            {"id": "post-1"}
        )
        
        # Act
        result = node.to_html()
        
        # Assert
        expected = '<article id="post-1"><h1 class="title">My First Blog Post</h1><p>This is the first paragraph.</p><p class="highlight">This is the second paragraph.</p></article>'
        self.assertEqual(result, expected)

    def test_parent_node_nav_with_dropdown(self):
        # Arrange: Create a nav with nested dropdown menu
        node = ParentNode(
            "nav",
            [
                LeafNode("a", "Home", {"href": "/"}),
                ParentNode(
                    "div",
                    [
                        LeafNode("button", "Products", {"class": "dropdown-trigger"}),
                        ParentNode(
                            "ul",
                            [
                                LeafNode("li", "Software", {"class": "item"}),
                                LeafNode("li", "Hardware", {"class": "item"}),
                                LeafNode("li", "Services", {"class": "item"})
                            ],
                            {"class": "dropdown-menu"}
                        )
                    ],
                    {"class": "dropdown"}
                )
            ],
            {"class": "navbar"}
        )
        
        # Act
        result = node.to_html()
        
        # Assert
        expected = '<nav class="navbar"><a href="/">Home</a><div class="dropdown"><button class="dropdown-trigger">Products</button><ul class="dropdown-menu"><li class="item">Software</li><li class="item">Hardware</li><li class="item">Services</li></ul></div></nav>'
        self.assertEqual(result, expected)
    
    def test_parent_node_error_cases(self):
        # Test missing tag
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode("p", "text")])
            node.to_html()
        self.assertTrue("ParentNode must have a tag" in str(context.exception))

        # Test missing children
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", None)
            node.to_html()
        self.assertTrue("ParentNode must have children" in str(context.exception))

        # Test empty children list
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div", [])
            node.to_html()
        self.assertTrue("ParentNode must have children" in str(context.exception))

        # Test invalid child type
        with self.assertRaises(TypeError) as context:
            node = ParentNode("div", ["Not a node"])
            node.to_html()

    def test_complete_blog_layout(self):
        # Create a complex blog post structure
        node = ParentNode(
            "main",
            [
                ParentNode(
                    "article",
                    [
                        LeafNode("h1", "My Programming Journey"),
                        ParentNode(
                            "section",
                            [
                                LeafNode("p", "Yesterday I learned about HTML nodes."),
                                LeafNode("img", None, {"src": "code.jpg", "alt": "Code screenshot"}),
                                ParentNode(
                                    "div",
                                    [
                                        LeafNode("strong", "Key takeaway:"),
                                        LeafNode(None, " Always test your code!")
                                    ],
                                    {"class": "highlight"}
                                )
                            ]
                        )
                    ],
                    {"class": "blog-post"}
                )
            ]
        )
        
        # Act
        result = node.to_html()
        
        # Assert
        expected = '<main><article class="blog-post"><h1>My Programming Journey</h1><section><p>Yesterday I learned about HTML nodes.</p><img src="code.jpg" alt="Code screenshot"><div class="highlight"><strong>Key takeaway:</strong> Always test your code!</div></section></article></main>'
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main()