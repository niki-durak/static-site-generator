import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)
    def test_2(self):

        node = TextNode("FDASFASDF", TextType.italic)
        node2 = TextNode("fqwefwq", TextType.bold)
        self.assertNotEqual(node,node2)
    def test_3(self):
        node = TextNode("Hello", TextType.plain, 'www.com')
        node2 = TextNode("Hello", TextType.plain)
        self.assertNotEqual(node,node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.plain)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
            


if __name__ == "__main__":
    unittest.main()