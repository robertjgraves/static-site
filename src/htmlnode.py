
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("child class will override")

    def props_to_html(self):
        if self.props is None:
            return ""
        
        html_props = ""
        
        for k,v in self.props.items():
            html_props += f' {k}="{v}"'

        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.children = None
    
    @property
    def children(self):
        return None

    @children.setter
    def children(self, value):
        raise AttributeError("LeafNode cannot have children.")
    
    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        
        if not self.tag:
            return self.value

        props_string = self.props_to_html() if self.props else ""

        html_results = f'<{self.tag}{props_string}>{self.value}</{self.tag}>'.strip()

        return html_results

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
