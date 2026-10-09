from inline_markdown import markdown_to_html_node, markdown_to_blocks
import os

def extract_title(markdown):
    md = markdown.split("\n")
    for line in md:
        if line.startswith("# "):
            return line[2:].strip()
        
    raise Exception("no heading")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()
    
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    head = extract_title(markdown)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    html = template.replace("{{ Title }}", head).replace("{{ Content }}", html)

    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    l = os.listdir(dir_path_content)
    for el in l:
        from_path = os.path.join(dir_path_content,el)
        dest_path = os.path.join(dest_dir_path,el)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)