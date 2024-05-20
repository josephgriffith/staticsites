import unittest

from textnode import (TextNode, 
                      tt_text, tt_bold, tt_italic, tt_code, tt_link, tt_image,  
                      text_node_to_html_node)
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is a text node", "bold", "123.com")
        node2 = TextNode("This is a text node", "bold", "123.com")
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", "bold", "123.com")
        node2 = TextNode("This is a text node!", "bold", "123.com")
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", "bold", "123.com")
        node2 = TextNode("This is a text node", "Bold", "123.com")
        self.assertNotEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is a text node", "bold", "123.com")
        node2 = TextNode("This is a text node", "bold", "124.com")
        self.assertNotEqual(node, node2)
    def test_eq5(self):
        node = TextNode(None, "bold", "123.com")
        node2 = TextNode(None, "bold", "123.com")
        self.assertEqual(node, node2)
    def test_eq6(self):
        node = TextNode("string", None, "123.com")
        node2 = TextNode("string", None, "123.com")
        self.assertEqual(node, node2)
    def test_eq7(self):
        node = TextNode("string", "bold", None)
        node2 = TextNode("string", "bold", None)
        self.assertEqual(node, node2)

    #text_node_to_html_node 
    def test_text_node_to_html_node_1(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("this is not a textnode")
    def test_text_node_to_html_node_2(self):
        self.assertEqual(text_node_to_html_node(TextNode("hello", "text")), LeafNode(None, "hello"))
    def test_text_node_to_html_node_3(self):
        self.assertEqual(text_node_to_html_node(TextNode("hello", "bold")), LeafNode("b", "hello"))
    def test_text_node_to_html_node_8(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("hello there", "underlined"))
    
if __name__ == "__main__":
    unittest.main()
