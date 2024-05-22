class HTMLNode:
    #                   
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        # props - A dictionary of key-value pairs representing the attributes of the HTML tag. 
        # For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props                  
        self.summary = self.get_summary()

    def get_summary(self):
        s = ""
        if self.tag:
            s += "T"
        if self.value:
            s += "V"
        if self.children:
            s += "C"
        if self.props:
            s += "P"
        return s
    
    def to_html(self):
        raise Exception("NotImplementedError")
    
    def props_to_html(self):
        html = ""
        if self.props:
            for k, v in self.props.items():
                html += " "+k+"=\""+v+"\""      
        return html
    
    def __eq__(self, node: object) -> bool:
        return (self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props)

    def __repr__(self) -> str:
        l = len(self.children)
        return f"HTMLNode({self.tag}, {self.value}, {[self.children[i].summary for i in range(l)]}, {self.props_to_html()}"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("No tag in ParentNode")
        if not self.children:
            raise ValueError("No children in ParentNode")
        s = f"<{self.tag}>"
        for c in self.children:
            s += c.to_html()
        return s+f"</{self.tag}>"
    
    def __repr__(self) -> str:
        l = 0
        if self.children:               
            l = len(self.children)
        if self.props:
            return f"ParentNode({self.tag}, {[self.children[i] for i in range(l)]}, {self.props_to_html()})"
        else:
            return f"ParentNode({self.tag}, {[self.children[i] for i in range(l)]})"
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNodes must have a value")
        return f"{self.get_open_tag()}{self.value}{self.get_close_tag()}"

    def get_open_tag(self):
        t = ""
        if self.tag:
            t = f"<{self.tag}{self.props_to_html()}>"
        return t
    def get_close_tag(self):
        t = ""
        if self.tag:
            t = f"</{self.tag}>"
        return t

    def __repr__(self) -> str:
        if self.props:
            return f"LeafNode({self.tag}, {self.value}, {self.props_to_html()})"
        else:
            return f"LeafNode({self.tag}, {self.value})"

