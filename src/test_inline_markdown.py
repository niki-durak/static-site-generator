import unittest
from inline_markdown import block_to_block_type, BlockType, markdown_to_blocks, markdown_to_html_node

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(
            block_to_block_type("## Заголовок"),
            BlockType.HEADING,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Просто текст"),
            BlockType.PARAGRAPH,
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )