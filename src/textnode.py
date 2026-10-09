from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    plain = 'plain'
    bold = 'bold'
    italic = 'italic'
    code = 'code'
    link = 'link'
    image = 'image'


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
            
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.plain:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.bold:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.italic:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.code:
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("invalid text type")