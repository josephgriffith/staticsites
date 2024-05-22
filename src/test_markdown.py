import unittest
__import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

from markdown import (extract_markdown_images, extract_markdown_links, markdown_to_blocks, get_blocktype,  # type: ignore - removes warning on markdown import
                        bt_paragraph, bt_heading, bt_code, bt_quote, bt_unordered_list, bt_ordered_list, mdChars, 
                        split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes,
                        heading_to_htmlnode, code_to_htmlnode, quote_to_htmlnode, unordered_to_htmlnode, ordered_to_htmlnode, paragraph_to_htmlnode, markdown_to_html_node)
from textnode import TextNode, tt_text, tt_bold, tt_italic, tt_code, tt_link, tt_image
from htmlnode import ParentNode, LeafNode

class TestMarkdown(unittest.TestCase):
    # images
    def test_images1(self):
        input = "blah ![image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), furthermore ![mem](https://i.imgur.com/yFhRM6h.jpeg)"
        expected = [("image!", "https://i.imgur.com/GWbjXVV.jpeg"), ("meme", "https://i.imgur.com/B0hYfji.jpeg"), ("mem", "https://i.imgur.com/yFhRM6h.jpeg")]
        self.assertEqual(extract_markdown_images(input), expected)
    def test_images2(self):
        input = "no markdown images here... (https://i.imgur.com/yFhRM6h.jpeg), maybe ![red herring]https://i.imgur.com/BGus7Go.jpg"
        expected = []
        self.assertEqual(extract_markdown_images(input), expected)
    # links
    def test_links1(self):
        input = "no markdown images here... (https://i.imgur.com/yFhRM6h.jpeg), maybe [red herring]https://i.imgur.com/BGus7Go.jpg"
        expected = []
        self.assertEqual(extract_markdown_links(input), expected)
    def test_links2(self):
        input = "blah ![image!](https://i.imgur.com/GWbjXVV.jpeg), also [meme](https://i.imgur.com/B0hYfji.jpeg), furthermore [mem](https://i.imgur.com/yFhRM6h.jpeg)"
        expected = [("image!", "https://i.imgur.com/GWbjXVV.jpeg"), ("meme", "https://i.imgur.com/B0hYfji.jpeg"), ("mem", "https://i.imgur.com/yFhRM6h.jpeg")]
        self.assertEqual(extract_markdown_links(input), expected)

    # split_nodes_delimiter 
    def test_split_nodes_delimiter_1(self):
        nodes = [TextNode("sup?", "link", "abc.com")]
        expected = [TextNode("sup?", "link", "abc.com")]
        self.assertEqual(split_nodes_delimiter(nodes,""), expected)
    def test_split_nodes_delimiter_2(self):
        nodes = [TextNode("sup **dawg**", tt_text)]
        expected = [TextNode("sup ", "text"), TextNode("dawg", "bold")]
        self.assertEqual(split_nodes_delimiter(nodes,"**"), expected)
    def test_split_nodes_delimiter_3(self):
        nodes = [TextNode("sup *dawg*", tt_text)]
        expected = [TextNode("sup ", "text"), TextNode("dawg", "italic")]
        self.assertEqual(split_nodes_delimiter(nodes,"*"), expected)
    def test_split_nodes_delimiter_4(self):
        nodes = [TextNode("sup `dawg` ...", tt_text)]
        expected = [TextNode("sup ", "text"), TextNode("dawg", "code"), TextNode(" ...", "text")]
        self.assertEqual(split_nodes_delimiter(nodes,"`"), expected)
    def test_split_nodes_delimiter_5(self):
        nodes = [TextNode("inputs are `x` and `y`", tt_text)]
        expected = [TextNode("inputs are ", "text"), TextNode("x", "code"), TextNode(" and ", "text"), TextNode("y", "code")]
        self.assertEqual(split_nodes_delimiter(nodes,"`"), expected)
    def test_split_nodes_delimiter_6(self):
        text = "Here's **bold**, *italic* and `code block` and ![image](domain.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        end = ", *italic* and `code block` and ![image](domain.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = [TextNode(text, tt_text)]
        expected = [TextNode("Here's ", "text"), TextNode("bold", "bold"), TextNode(end, "text")]
        self.assertEqual(split_nodes_delimiter(nodes,"**"), expected)
    def test_split_nodes_delimiter_8(self):
        text = "Here's **bold**, *italic* and `code block` and ![image](domain.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        end = " and ![image](domain.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = [TextNode(text, tt_text)]
        expected = [TextNode("Here's **bold**, *italic* and ", "text"), TextNode("code block", "code"), TextNode(end, "text")]
        self.assertEqual(split_nodes_delimiter(nodes,"`"), expected)
    def test_split_nodes_delimiter_9(self):
        nodes = [TextNode("hanging *chad", tt_text)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes,"*")
        
    # split_nodes_image
    def test_split_image1(self):
        input = "![image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), furthermore ![mem](https://i.imgur.com/yFhRM6h.jpeg)"
        expected = [TextNode("image!", tt_image, "https://i.imgur.com/GWbjXVV.jpeg"), 
                    TextNode(", also ", tt_text),
                    TextNode("meme", tt_image, "https://i.imgur.com/B0hYfji.jpeg"),
                    TextNode(", furthermore ", tt_text),
                    TextNode("mem", tt_image, "https://i.imgur.com/yFhRM6h.jpeg")]
        self.assertEqual(split_nodes_image([TextNode(input, tt_text)]), expected)
    def test_split_image2(self):
        input = "blah ![image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), furthermore ![mem](https://i.imgur.com/yFhRM6h.jpeg)"
        expected = [TextNode("blah ", tt_text),
                    TextNode("image!", tt_image, "https://i.imgur.com/GWbjXVV.jpeg"), 
                    TextNode(", also ", tt_text),
                    TextNode("meme", tt_image, "https://i.imgur.com/B0hYfji.jpeg"),
                    TextNode(", furthermore ", tt_text),
                    TextNode("mem", tt_image, "https://i.imgur.com/yFhRM6h.jpeg")]
        self.assertEqual(split_nodes_image([TextNode(input, tt_text)]), expected)
    def test_split_image3(self):
        input = "blah ![image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), ![mem](https://i.imgur.com/yFhRM6h.jpeg), etc..."
        expected = [TextNode("blah ", tt_text),
                    TextNode("image!", tt_image, "https://i.imgur.com/GWbjXVV.jpeg"), 
                    TextNode(", also ", tt_text),
                    TextNode("meme", tt_image, "https://i.imgur.com/B0hYfji.jpeg"),
                    TextNode(", ", tt_text),
                    TextNode("mem", tt_image, "https://i.imgur.com/yFhRM6h.jpeg"),
                    TextNode(", etc...", tt_text)]
        self.assertEqual(split_nodes_image([TextNode(input, tt_text)]), expected)
    def test_split_image4(self):
        input = "no markdown images here... (https://i.imgur.com/yFhRM6h.jpeg), maybe ![red herring]https://i.imgur.com/BGus7Go.jpg"
        expected = [TextNode(input, tt_text)]
        self.assertEqual(split_nodes_image([TextNode(input, tt_text)]), expected)

    # split_nodes_link
    def test_split_link1(self):
        input = "[image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), furthermore ![mem](https://i.imgur.com/yFhRM6h.jpeg)"
        expected = [TextNode("image!", tt_link, "https://i.imgur.com/GWbjXVV.jpeg"), 
                    TextNode(", also !", tt_text),
                    TextNode("meme", tt_link, "https://i.imgur.com/B0hYfji.jpeg"),
                    TextNode(", furthermore !", tt_text),
                    TextNode("mem", tt_link, "https://i.imgur.com/yFhRM6h.jpeg")]
        self.assertEqual(split_nodes_link([TextNode(input, tt_text)]), expected)
    def test_split_link2(self):
        input = "blah ![image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), furthermore [mem](https://i.imgur.com/yFhRM6h.jpeg)"
        expected = [TextNode("blah !", tt_text),
                    TextNode("image!", tt_link, "https://i.imgur.com/GWbjXVV.jpeg"), 
                    TextNode(", also !", tt_text),
                    TextNode("meme", tt_link, "https://i.imgur.com/B0hYfji.jpeg"),
                    TextNode(", furthermore ", tt_text),
                    TextNode("mem", tt_link, "https://i.imgur.com/yFhRM6h.jpeg")]
        self.assertEqual(split_nodes_link([TextNode(input, tt_text)]), expected)
    def test_split_link3(self):
        input = "blah ![image!](https://i.imgur.com/GWbjXVV.jpeg), also ![meme](https://i.imgur.com/B0hYfji.jpeg), ![mem](https://i.imgur.com/yFhRM6h.jpeg), etc..."
        expected = [TextNode("blah !", tt_text),
                    TextNode("image!", tt_link, "https://i.imgur.com/GWbjXVV.jpeg"), 
                    TextNode(", also !", tt_text),
                    TextNode("meme", tt_link, "https://i.imgur.com/B0hYfji.jpeg"),
                    TextNode(", !", tt_text),
                    TextNode("mem", tt_link, "https://i.imgur.com/yFhRM6h.jpeg"),
                    TextNode(", etc...", tt_text)]
        self.assertEqual(split_nodes_link([TextNode(input, tt_text)]), expected)
    def test_split_link4(self):
        input = "no markdown links here... (https://i.imgur.com/yFhRM6h.jpeg), maybe ![red herring]https://i.imgur.com/BGus7Go.jpg"
        expected = [TextNode(input, tt_text)]
        self.assertEqual(split_nodes_link([TextNode(input, tt_text)]), expected)

    # text_to_textnodes
    def test_to_textnodes1(self):
        input = "Here's **bold**, *italic* and `code block` and ![image](domain.com/JKZ.png) and a [link](boot.dev)"
        expected = [TextNode("Here's ", tt_text),
                    TextNode("bold", tt_bold),
                    TextNode(", ", tt_text),
                    TextNode("italic", tt_italic),
                    TextNode(" and ", tt_text),
                    TextNode("code block", tt_code),
                    TextNode(" and ", tt_text),
                    TextNode("image", tt_image, "domain.com/JKZ.png"),
                    TextNode(" and a ", tt_text),
                    TextNode("link", tt_link, "boot.dev")]
        self.assertEqual(text_to_textnodes(input), expected)
    def test_to_textnodes2(self):
        input = "Here's *italic* and **bold**`code block` and ![image](domain.com/JKZ.png) and a [link](boot.dev)"
        expected = [TextNode("Here's ", tt_text),
                    TextNode("italic", tt_italic),
                    TextNode(" and ", tt_text),
                    TextNode("bold", tt_bold),
                    TextNode("code block", tt_code),
                    TextNode(" and ", tt_text),
                    TextNode("image", tt_image, "domain.com/JKZ.png"),
                    TextNode(" and a ", tt_text),
                    TextNode("link", tt_link, "boot.dev")]
        self.assertEqual(text_to_textnodes(input), expected)
    def test_to_textnodes3(self):
        input = "Here's *italic* and **bold** and a [link](boot.dev)"
        expected = [TextNode("Here's ", tt_text),
                    TextNode("italic", tt_italic),
                    TextNode(" and ", tt_text),
                    TextNode("bold", tt_bold),
                    TextNode(" and a ", tt_text),
                    TextNode("link", tt_link, "boot.dev")]
        self.assertEqual(text_to_textnodes(input), expected)
    def test_to_textnodes4(self):
        input = "Here's text"
        expected = [TextNode("Here's text", tt_text)]
        self.assertEqual(text_to_textnodes(input), expected)
    def test_to_textnodes5(self):
        input = "*italic* and **bold** and a [link](boot.dev)"
        expected = [TextNode("italic", tt_italic),
                    TextNode(" and ", tt_text),
                    TextNode("bold", tt_bold),
                    TextNode(" and a ", tt_text),
                    TextNode("link", tt_link, "boot.dev")]
        self.assertEqual(text_to_textnodes(input), expected)


    
    # blocks
    def test_blocks1(self):
        input = "one\n\ntwo\n\n\nthree\n\n\n\nfour\n\n\n\n\nfive"
        expected = ["one", "two", "three", "four", "five"]
        self.assertEqual(markdown_to_blocks(input), expected)
    def test_blocks2(self):
        input = "# heading\n\nparagraph of text. some **bold** and *italic*.\n\n* This is a list item\n* This is another list item"
        expected = ["# heading","paragraph of text. some **bold** and *italic*.","* This is a list item\n* This is another list item"]
        self.assertEqual(markdown_to_blocks(input), expected)
    def test_blocks3(self):
        input = "**bolded** paragraph\n\nparagraph with *italic* text and `code` here\nsame paragraph on a new line\n\n* This is a list\n* with items"
        expected = ["**bolded** paragraph","paragraph with *italic* text and `code` here\nsame paragraph on a new line","* This is a list\n* with items"]
        self.assertEqual(markdown_to_blocks(input), expected)
    def test_blocks4(self):
        input = " one\n\ntwo \n\n\n three\n\n\n\n four\n\n\n\n\n five"
        expected = ["one", "two", "three", "four", "five"]
        self.assertEqual(markdown_to_blocks(input), expected)

    # blocktype
    def test_blocktype1(self):
        input = "# heading"
        expected = bt_heading
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype7(self):
        input = "## heading"
        expected = bt_heading
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype8(self):
        input = "### heading"
        expected = bt_heading
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype9(self):
        input = "#### heading"
        expected = bt_heading
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype10(self):
        input = "##### heading"
        expected = bt_heading
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype11(self):
        input = "###### heading"
        expected = bt_heading
        self.assertEqual(get_blocktype(input), expected)

    def test_blocktype2(self):
        input = "```\n```"
        expected = bt_code
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype12(self):
        input = "```\njvdskvd\n```"
        expected = bt_code
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype14(self):
        input = "```stuff\nthings\nand junk```"
        expected = bt_code
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype3(self):
        input = "> quote"
        expected = bt_quote
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype13(self):        
        input = "> quote\n> jvdsklv\n> things"
        expected = bt_quote
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype4(self):
        input = "* unordered list\n* nested list\n* another item"
        expected = bt_unordered_list
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype5(self):
        input = "1. ordered list\n2. nested list\n3. another item"
        expected = bt_ordered_list
        self.assertEqual(get_blocktype(input), expected)
    def test_blocktype6(self):
        input = "paragraph\n1. oops!"
        expected = bt_paragraph
        self.assertEqual(get_blocktype(input), expected)

    # to html
    def test_heading1(self):
        input = "# heading"
        expected = ParentNode("h2", [LeafNode(None, "heading")])
        self.assertNotEqual(heading_to_htmlnode(input), expected)
    def test_heading2(self):
        input = "# heading"
        expected = ParentNode("h1", [LeafNode(None, "headings")])
        self.assertNotEqual(heading_to_htmlnode(input), expected)
    def test_heading3(self):
        input = "### heading 3"
        expected = ParentNode("h3", [LeafNode(None, "heading 3")])
        self.assertEqual(heading_to_htmlnode(input), expected)
    def test_heading4(self):
        input = "###### heading six"
        expected = ParentNode("h6", [LeafNode(None, "heading six")])
        self.assertEqual(heading_to_htmlnode(input), expected)
    def test_heading5(self):
        input = "###### heading **six**"
        expected = ParentNode("h6", [LeafNode(None, "heading "), LeafNode("b", "six")])
        self.assertEqual(heading_to_htmlnode(input), expected)
    def test_heading6(self):
        input = "###### ."
        expected = ParentNode("h6", [LeafNode(None, ".")])
        self.assertEqual(heading_to_htmlnode(input), expected)

    def test_code1(self):
        input = "```stuff```"
        expected = ParentNode("pre", [ParentNode("code", [LeafNode(None, "stuff")])])
        self.assertEqual(code_to_htmlnode(input), expected)    
    def test_code2(self):
        input = "```stuff\nthings\nand junk```"
        expected = ParentNode("pre", [ParentNode("code", [LeafNode(None, "stuff\nthings\nand junk")])])
        self.assertEqual(code_to_htmlnode(input), expected)    
    def test_code3(self):
        input = "```\n```"
        expected = ParentNode("pre", [ParentNode("code", [])])
        self.assertEqual(code_to_htmlnode(input), expected)    
    def test_code4(self):
        input = "```stuff\n**things**`and` junk```"
        expected = ParentNode("pre", [ParentNode("code", [LeafNode(None, "stuff\n"), LeafNode("b", "things"), LeafNode("code", "and"), LeafNode(None, " junk")])])
        self.assertEqual(code_to_htmlnode(input), expected)    

    def test_quote1(self):
        input = "> quote"
        expected = ParentNode("blockquote", [LeafNode(None, "quote")])
        self.assertEqual(quote_to_htmlnode(input), expected)
    def test_quote2(self):
        input = "> quote\n> more text"
        expected = ParentNode("blockquote", [LeafNode(None, "quote\nmore text")])
        self.assertEqual(quote_to_htmlnode(input), expected)
    def test_quote2(self):
        input = "> quote\n> more *text*"
        expected = ParentNode("blockquote", [LeafNode(None, "quote\nmore "), LeafNode("i", "text")])
        self.assertEqual(quote_to_htmlnode(input), expected)

    def test_unordered1(self):
        input = "* item\n* another item"
        expected = ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode(None, "another item")])])
        self.assertEqual(unordered_to_htmlnode(input), expected)
    def test_unordered2(self):
        input = "* item"
        expected = ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")])])
        self.assertEqual(unordered_to_htmlnode(input), expected)
    def test_unordered3(self):
        input = "* item\n* *another* item"
        expected = ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode("i", "another"), LeafNode(None, " item")])])
        self.assertEqual(unordered_to_htmlnode(input), expected)
    def test_unordered4(self):
        input = "- item\n- *another* item"
        expected = ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode("i", "another"), LeafNode(None, " item")])])
        self.assertEqual(unordered_to_htmlnode(input), expected)
    def test_unordered5(self):
        input = "- item\n* *another* item"
        expected = ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode("i", "another"), LeafNode(None, " item")])])
        self.assertEqual(unordered_to_htmlnode(input), expected)

    def test_ordered1(self):
        input = "1. item"
        expected = ParentNode("ol", [ParentNode("li", [LeafNode(None, "item")])])
        self.assertEqual(ordered_to_htmlnode(input), expected)
    def test_ordered2(self):
        input = "1. item\n2. another item"
        expected = ParentNode("ol", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode(None, "another item")])])
        self.assertEqual(ordered_to_htmlnode(input), expected)
    def test_ordered3(self):
        input = "1. item\n2. another `item`"
        expected = ParentNode("ol", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode(None, "another "), LeafNode("code", "item")])])
        self.assertEqual(ordered_to_htmlnode(input), expected)

    def test_paragraph1(self):
        input = "paragraph of text. some **bold** and *italic*."
        expected = ParentNode("p", [LeafNode(None, "paragraph of text. some "), LeafNode("b", "bold"), LeafNode(None, " and "), LeafNode("i", "italic"), LeafNode(None, ".")])
        self.assertEqual(paragraph_to_htmlnode(input), expected)
    def test_paragraph2(self):
        input = "paragraph of text.\n> not a quote\n# another not heading"
        expected = ParentNode("p", [LeafNode(None, "paragraph of text.\n> not a quote\n# another not heading")])
        self.assertEqual(paragraph_to_htmlnode(input), expected)

    def test_markdown_to_html_node1(self):
        input = "# heading"
        expected = ParentNode("div", [ParentNode("h1", [LeafNode(None, "heading")])])
        self.assertEqual(markdown_to_html_node(input), expected)
    def test_markdown_to_html_node2(self):
        input = "```stuff\nthings\nand junk```"
        expected = ParentNode("div", [ParentNode("pre", [ParentNode("code", [LeafNode(None, "stuff\nthings\nand junk")])])])
        self.assertEqual(markdown_to_html_node(input), expected)
    def test_markdown_to_html_node3(self):
        input = "> quote\n> more *text*"
        expected = ParentNode("div", [ParentNode("blockquote", [LeafNode(None, "quote\nmore "), LeafNode("i", "text")])])
        self.assertEqual(markdown_to_html_node(input), expected)
    def test_markdown_to_html_node4(self):
        input = "* item\n* another"
        expected = ParentNode("div", [ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode(None, "another")])])])
        self.assertEqual(markdown_to_html_node(input), expected)
    def test_markdown_to_html_node5(self):
        input = "1. item\n2. another"
        expected = ParentNode("div", [ParentNode("ol", [ParentNode("li", [LeafNode(None, "item")]), ParentNode("li", [LeafNode(None, "another")])])])
        self.assertEqual(markdown_to_html_node(input), expected)
    def test_markdown_to_html_node6(self):
        input = "paragraph of text.\n> not a quote\n# another not heading"
        expected = ParentNode("div", [ParentNode("p", [LeafNode(None, "paragraph of text.\n> not a quote\n# another not heading")])])
        self.assertEqual(markdown_to_html_node(input), expected)

    def test_markdown_to_html1(self):
        input = "# heading"
        expected = "<div><h1>heading</h1></div>"
        self.assertEqual(markdown_to_html_node(input).to_html(), expected)
    def test_markdown_to_html2(self):
        input = "```stuff\nthings\nand junk```"
        expected = "<div><pre><code>stuff\nthings\nand junk</code></pre></div>"
        self.assertEqual(markdown_to_html_node(input).to_html(), expected)
    def test_markdown_to_html3(self):
        input = "> quote\n> more *text*"
        expected = "<div><blockquote>quote\nmore <i>text</i></blockquote></div>"
        self.assertEqual(markdown_to_html_node(input).to_html(), expected)
    def test_markdown_to_html4(self):
        input = "* item\n* another"
        expected = "<div><ul><li>item</li><li>another</li></ul></div>"
        self.assertEqual(markdown_to_html_node(input).to_html(), expected)
    def test_markdown_to_html5(self):
        input = "1. item\n2. another"
        expected = "<div><ol><li>item</li><li>another</li></ol></div>"
        self.assertEqual(markdown_to_html_node(input).to_html(), expected)
    def test_markdown_to_html6(self):
        input = "paragraph of text.\n> not a quote\n# another not heading"
        expected = "<div><p>paragraph of text.\n> not a quote\n# another not heading</p></div>"
        self.assertEqual(markdown_to_html_node(input).to_html(), expected)





















