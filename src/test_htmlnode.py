import unittest
#from <file> import <class>
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq1(self):
        n1 = HTMLNode("a", "some text", [HTMLNode("p", "text", None, None), HTMLNode("p", "text", None, None)], {"href": "https://www.google.com", "target": "_blank"})
        n2 = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(n1.props_to_html(), n2)
    def test_eq2(self):
        n1 = HTMLNode("a", "some text", [HTMLNode("p", "text", None, None), HTMLNode("p", "text", None, None)], {"href": "https://www.google.com", "target": "_blank"})
        n2 = HTMLNode("a", "some text", [HTMLNode("p", "text", None, None), HTMLNode("p", "text", None, None)], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(n1, n2)
    def test_eq3(self):
        n1 = ParentNode("a", [LeafNode("p", "text"), LeafNode("p", "things")], {"href": "https://www.google.com", "target": "_blank"})
        n2 = ParentNode("a", [LeafNode("p", "text"), LeafNode("p", "things")], {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(n1, n2)
    def test_eq3(self):
        n1 = LeafNode("p", "text", {"href": "https://www.google.com", "target": "_blank"})
        n2 = LeafNode("p", "text", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(n1, n2)

class TestParentNode(unittest.TestCase):
    def test1(self):
        p = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            p.to_html()
    def test2(self):
        p = ParentNode("p", [])
        with self.assertRaises(ValueError):
            p.to_html()
    def test3(self):
        p = ParentNode("p", None)
        with self.assertRaises(ValueError):
            p.to_html()
    def test4(self):
        p = ParentNode("p", [LeafNode("b", "Bold text"), 
                            ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),],), 
                            LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),],)
        self.assertEqual(p.to_html(), "<p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text<i>italic text</i>Normal text</p>")
    def test5(self):
        parent_node = ParentNode("div", [LeafNode("span", "text"), LeafNode("main", "blah blah")])
        self.assertEqual(parent_node.to_html(), "<div><span>text</span><main>blah blah</main></div>")

class TestLeafNode(unittest.TestCase):
    def test1(self):
        l = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(l.to_html(), "<p>This is a paragraph of text.</p>")
    def test2(self):
        l = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(l.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    def test3(self):
        l = LeafNode(None, "plain text", {"href": "https://www.google.com"})
        self.assertEqual(l.to_html(), "plain text")
    def test4(self):                                          #IDK WTF
        l = LeafNode("p", None)
        with self.assertRaises(ValueError):
            l.to_html()

if __name__ == "__main__":
    unittest.main()
