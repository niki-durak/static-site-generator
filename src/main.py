from textnode import TextNode, TextType
from copystatic import copystatic
from gencontent import generate_pages_recursive
import sys


def main():
    
    a = TextNode('This is some achor text', TextType.link, 'https://www.boot.dev')
    print(a)

    basepath = "/"
    copystatic("static", "docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    generate_pages_recursive("content", "template.html", "docs", basepath)
   
main()