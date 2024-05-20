from htmlnode import LeafNode
# TextTypes
tt_text = "text"
tt_bold = "bold"
tt_italic = "italic"
tt_code = "code"
tt_link = "link"
tt_image = "image"        

class TextNode:
    def __init__(self, t,tt,url=None):
        self.text = t
        self.text_type = tt
        self.url = url

    def __eq__(self, node: object) -> bool:
        if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
            return True
        return False
    
    def __repr__(self) -> str:
        return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"

def text_node_to_html_node(textnode):
    if type(textnode) != TextNode:
        raise TypeError("Not a TextNode")
    if textnode.text_type == tt_text:
        return LeafNode(None, textnode.text)
    elif textnode.text_type == tt_bold:
        return LeafNode("b", textnode.text)
    elif textnode.text_type == tt_italic:
        return LeafNode("i", textnode.text)
    elif textnode.text_type == tt_code:
        return LeafNode("code", textnode.text)
    elif textnode.text_type == tt_link:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    elif textnode.text_type == tt_image:
        return LeafNode("img", "", {"alt": textnode.text, "src": textnode.url})
    else:
        raise ValueError(f"{textnode.text_type} is not a valid text type. The valid types are 'text', 'bold', 'italic', 'code', 'link', or 'image'.")

def text_nodes_to_html_nodes(nodes):
    return [text_node_to_html_node(n) for n in nodes]



