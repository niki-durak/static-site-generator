import unittest
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, split_nodes_image, text_to_textnodes, markdown_to_blocks


class TestHTMLNode(unittest.TestCase):
    def test_3(self):
        node = HTMLNode("p", "текст", None, {"href": "google.com"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="google.com"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain),
                TextNode("second image", TextType.image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **bold** and _italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.plain),
            TextNode("bold", TextType.bold),
            TextNode(" and ", TextType.plain),
            TextNode("italic", TextType.italic),
        ]
        self.assertEqual(nodes, expected)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks(self):
            md = "Заголовок\n\nПервый абзац текста\n\n\nВторой абзац"
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                ['Заголовок', 'Первый абзац текста', 'Второй абзац'],
            )    

    
if __name__ == "__main__":
    unittest.main()