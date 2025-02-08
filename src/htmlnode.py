
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

