import os
import re
from pathlib import Path
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, tt_text, tt_bold, tt_italic, tt_code, tt_link, tt_image, text_nodes_to_html_nodes

bt_heading = "heading"                      # <h1>-<h6>
bt_code = "code"                            # <pre><code>
bt_quote = "quote"                          # <blockquote>
bt_unordered_list = "unordered_list"        # <ul>
bt_ordered_list = "ordered_list"            # <ol>
bt_paragraph = "paragraph"                  # <p>

html_bt = {bt_heading: "h",             # tag += level
           bt_code: "pre><code",        # ParentNode("pre", [LeafNode("code", "code text")]
           bt_quote: "blockquote",
           bt_unordered_list: "ul",
           bt_ordered_list: "ol",
           bt_paragraph: "p"}

mdChars = {"**": tt_bold,
            "*": tt_italic,
            "`": tt_code,}

# INLINE MARKDOWN
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
# def split_nodes_delimiter(old, delimiter, tt=None):
#     out = []
#     for n in old:
#         if not (delimiter in mdChars):      # ` or * or **
#             out.append(n)
#         else:
#             parsed = n.text.split(delimiter)
#             if len(parsed)%2 == 0:
#                 raise ValueError("Invalid markdown syntax")
#             for i in range(len(parsed)):
#                 if len(parsed[i]) == 0:
#                     continue
#                 if i%2 == 0:
#                     out.append(TextNode(parsed[i], tt_text))
#                 else:
#                     out.append(TextNode(parsed[i], mdChars[delimiter]))
#     return out
# takes tt_text TextNodes with bold, italic, or code markdown and a delimiter and returns a list of TNs with appropriate text types
def split_nodes_delimiter(old_nodes, delimiter, text_type=None):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != tt_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:                                                  # misses even amounts of list items as italics...
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], tt_text))
            else:
                split_nodes.append(TextNode(sections[i], mdChars[delimiter]))
        new_nodes.extend(split_nodes)
    return new_nodes
#parses tt_text TNs into tt_text and tt_image TNs
def split_nodes_image(old):
    out = []
    for n in old:
        images = extract_markdown_images(n.text)
        if not images:
            out.append(n)
        else:
            remaining = n.text
            for i in images:                                            # for each image 
                nonimage = remaining.split(f"![{i[0]}]({i[1]})", 1)     #split string with it
                if nonimage[0]:                                         #if any preceding text
                    out.append(TextNode(nonimage[0], tt_text))          #add TN 
                remaining = nonimage[1]
                out.append(TextNode(i[0], tt_image, i[1]))              #add image node
            if remaining:                                               
                out.append(TextNode(remaining, tt_text))                #add any trailing TN text
    return out
#parses tt_text TNs into tt_text and tt_link TNs
def split_nodes_link(old):
    out = []
    for n in old:
        links = extract_markdown_links(n.text)
        if not links:
            out.append(n)
        else:
            remaining = n.text
            for i in links:                                            
                nonlink = remaining.split(f"[{i[0]}]({i[1]})", 1)     
                if nonlink[0]:                                         
                    out.append(TextNode(nonlink[0], tt_text))          
                remaining = nonlink[1]
                out.append(TextNode(i[0], tt_link, i[1]))             
            if remaining:                                               
                out.append(TextNode(remaining, tt_text))                
    return out
# keeps correct order because all functions build a new list and maintain order
# takes raw inline markdown text and returns a list of TextNodes of appropriate text types
def text_to_textnodes(text):
    textnodes = [TextNode(text, tt_text)]
    for d in mdChars:
        textnodes = split_nodes_delimiter(textnodes, d)
    imgnodes = split_nodes_image(textnodes)
    linknodes = split_nodes_link(imgnodes)
    return linknodes


# BLOCK MARKDOWN
def markdown_to_blocks(text):
    out = []
    for s in re.split(r"\n{2,}", text):
        if s:
            out.append(s.strip())
    return out

def get_blocktype(text):
    lines = text.split("\n")
    if text.startswith("# ") or text.startswith("## ") or text.startswith("### ") or text.startswith("#### ") or text.startswith("##### ") or text.startswith("###### "):
        return bt_heading
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return bt_code
    elif text.startswith(">"):
        for l in lines:
            if not l.startswith(">"):
                return bt_paragraph
        return bt_quote
    elif text.startswith("* ") or text.startswith("- "):
        for l in lines:
            if not (l.startswith("* ") or l.startswith("- ")):
                return bt_paragraph
        return bt_unordered_list
    elif text.startswith("1. "):
        for i, l in enumerate(lines):
            if not l.startswith(f"{i+1}. "):
                return bt_paragraph
        return bt_ordered_list
    else:
        return bt_paragraph
def block_to_blocktype(text):
    return get_blocktype(text)

def heading_to_htmlnode(text):
    level = 1
    while text[level] == "#":
        level += 1
    return ParentNode(f"h{level}", text_nodes_to_html_nodes(text_to_textnodes(text[level+1:].strip())))
def code_to_htmlnode(text):
    return ParentNode("pre", [ParentNode("code", text_nodes_to_html_nodes(text_to_textnodes(text[3:-3].strip())))])
def quote_to_htmlnode(text):
    lines = text.split("\n")
    stripped = ""
    for l in lines:
        stripped += l[2:] + "\n"
    return ParentNode("blockquote", text_nodes_to_html_nodes(text_to_textnodes(stripped.strip())))
def unordered_to_htmlnode(text):
    lines = text.split("\n")
    items = []
    for l in lines:
        items.append(ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(l[2:]))))
    return ParentNode("ul", items)
def ordered_to_htmlnode(text):
    lines = text.split("\n")
    items = []
    for l in lines:
        items.append(ParentNode("li", text_nodes_to_html_nodes(text_to_textnodes(l[3:]))))
    return ParentNode("ol", items)
def paragraph_to_htmlnode(text):
    return ParentNode("p", text_nodes_to_html_nodes(text_to_textnodes(text)))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)       # convert to blocks (list of strings)
    children = []
    for b in blocks:
        type = get_blocktype(b)                 # get type
        if type == bt_heading:                  
            children.append(heading_to_htmlnode(b)) 
        elif type == bt_code:
            children.append(code_to_htmlnode(b))
        elif type == bt_quote:
            children.append(quote_to_htmlnode(b))
        elif type == bt_unordered_list:
            children.append(unordered_to_htmlnode(b))
        elif type == bt_ordered_list:
            children.append(ordered_to_htmlnode(b))
        else:   # type == bt_paragraph:
            children.append(paragraph_to_htmlnode(b))
    return ParentNode("div", children)                  # create a div htmlnode tree root
    # convert blocks to html - 
        # root div parent node
            # children blocks are parent nodes 
                # with leaf nodes for block content and inline markdown children
            
                
def extract_title(markdown):
    lines = markdown.split("\n")
    if lines[0].startswith("# "):
        return lines[0][2:]
    raise SyntaxError("Invalid syntax: markdown must start with a '# ' heading")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using {template_path}. Writing to {dest_path}...")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        temp = f.read()
    html = temp.replace("{{ Content }}", markdown_to_html_node(md).to_html()).replace("{{ Title }}", extract_title(md))
    dir = os.path.dirname(dest_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(content, template, dest):
    p = Path(content).glob('**/*')
    files = [x for x in p if x.is_file() and x.suffix == ".md"]
    for f in files:
        # print(str(f))                                           # content/index.md, content/majesty/index.md
        # print(str(f.name))                                      # index.md, index.md
        # print(f.relative_to(content))                           # index.md, majesty/index.md
        # print(f.relative_to(content).with_suffix(".html"))      # index.html, majesty/index.html
        generate_page(str(f), template, str(Path(dest) / f.relative_to(content).with_suffix(".html")))
