import os
from block_markdown import markdown_to_html_node

def extract_title(markdown_string):
    markdown_lines = markdown_string.splitlines()

    for line in markdown_lines:
        if line.startswith('#') and not line.startswith('##'):
            title = line[1:].strip()
            return title
    
    raise ValueError("No h1 header (line starting with '#') found in the markdown.")

def generate_page(from_path, template_path, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(from_path, 'r', encoding='utf-8') as markdown_file:
        markdown_content = markdown_file.read()

    title = extract_title(markdown_content)

    markdown_node = markdown_to_html_node(markdown_content)
    html_content = markdown_node.to_html()

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
        rendered_html = template_content.replace("{{ Title }}", title)
        rendered_html = rendered_html.replace("{{ Content }}", html_content)
    
    with open(dest_path, 'w', encoding='utf-8') as output_file:
        output_file.write(rendered_html)
    
    print(f"Generated page from {from_path} to {dest_path} using {template_path}")


if __name__ == "__main__":
    generate_page('content/index.md', 'template.html', 'public/index.html')