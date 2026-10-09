from textnode import TextNode, TextType
from copystatic import copystatic
from gencontent import generate_pages_recursive


def main():
    a = TextNode('This is some achor text', TextType.link, 'https://www.boot.dev')
    print(a)

    copystatic("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()