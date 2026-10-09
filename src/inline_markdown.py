import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.plain:
            new_nodes.append(node)
        else:
            nt = node.text.split(delimiter)
            if len(nt) % 2 == 0:
                raise Exception("even")
            for i in range(len(nt)):
                if i % 2 == 0 and len(nt[i]) != 0:
                    new_nodes.append(TextNode(nt[i], TextType.plain))
                else:
                    if len(nt[i]) != 0:
                        new_nodes.append(TextNode(nt[i], text_type))
    return new_nodes
def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.plain:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for alt, url in images:
                    before, remaining_text = remaining_text.split(f"![{alt}]({url})", 1)
                    if len(before) != 0:
                        new_nodes.append(TextNode(before, TextType.plain))
                    new_nodes.append(TextNode(alt, TextType.image, url))
                if len(remaining_text) != 0:
                    new_nodes.append(TextNode(remaining_text, TextType.plain))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.plain:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for alt, url in links:
                    before, remaining_text = remaining_text.split(f"[{alt}]({url})", 1)
                    if len(before) != 0:
                        new_nodes.append(TextNode(before, TextType.plain))
                    new_nodes.append(TextNode(alt, TextType.link, url))
                if len(remaining_text) != 0:
                    new_nodes.append(TextNode(remaining_text, TextType.plain))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.plain)]
    result = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(nodes, "**", TextType.bold), "_", TextType.italic), "`", TextType.code)))
    return result

def markdown_to_blocks(markdown):
    markdown += '\n'
    new_s = ''
    l = []
    for i in markdown.split('\n'):
        if len(i) == 0 and len(new_s) != 0:
            l.append(new_s)
            new_s = ''
        else:
            if len(new_s) > 0:
                new_s += '\n'
            new_s += i
    return l

def block_to_block_type(block) -> BlockType:
    c = 0
    for ch in block:
        if ch == '#':
            c += 1
        else:
            break
    if 1 <= c <= 6 and block[c] == " ":
        return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    if block.startswith('>'):
        f = True
        for i in block.split('\n'):
            if i.startswith('>'):
                continue
            else:
                f = False
        if f:
            return BlockType.QUOTE
    if block.startswith('- '):
        f = True
        for i in block.split('\n'):
            if i.startswith('- '):
                continue
            else:
                f = False
        if f:
            return BlockType.UNORDERED_LIST
    if block.startswith('1. '):
        f = True
        expected = 1
        for i in block.split('\n'):
            if i.startswith(f'{str(expected)}. '):
                expected += 1
                continue
            else:
                f = False
        if f:

            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.PARAGRAPH:
            HTMLnode = ParentNode("p", text_to_children(block.replace("\n", " ")))
            children.append(HTMLnode)
        elif blocktype == BlockType.HEADING:
            c = 0
            for ch in block:
                if ch == '#':
                    c += 1
                else:
                    break
            if 1 <= c <= 6 and block[c] == " ":
                HTMLnode = ParentNode(f"h{c}", text_to_children(block[c+1:]))
                children.append(HTMLnode)
        elif blocktype == BlockType.CODE:
            code_text = block[4:-3]
            text_node = TextNode(code_text, TextType.plain)
            code_html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [code_html_node])
            HTMLnode = ParentNode("pre", [code_node])
            children.append(HTMLnode)
        elif blocktype == BlockType.QUOTE:
            lines = block.split('\n')
            clean_lines = []
            for line in lines:
                text = line[2:]
                clean_lines.append(text)
            full_text = "\n".join(clean_lines)
            HTMLnode = ParentNode("blockquote", text_to_children(full_text))
            children.append(HTMLnode)
        elif blocktype == BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            li = []
            for line in lines:
                text = line[2:]
                item_children = text_to_children(text)
                li_node = ParentNode("li", item_children)
                li.append(li_node)
            HTMLnode = ParentNode("ul", li)
            children.append(HTMLnode)
        elif blocktype == BlockType.ORDERED_LIST:
            lines = block.split('\n')
            li = []
            for line in lines:
                space_index = line.find(" ")
                text = line[space_index + 1:]
                item_children = text_to_children(text)
                li_node = ParentNode("li", item_children)
                li.append(li_node)
            HTMLnode = ParentNode("ol", li)
            children.append(HTMLnode)
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)  # шаг 1, уже готов
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)  # шаг 2, уже готов
        children.append(html_node)
    return children