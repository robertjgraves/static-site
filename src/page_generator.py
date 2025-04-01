import os
from block_markdown import markdown_to_html_node

def extract_title(markdown_string):
    markdown_lines = markdown_string.splitlines()

    for line in markdown_lines:
        if line.startswith('#') and not line.startswith('##'):
            title = line[1:].strip()
            return title
    
    raise ValueError("No h1 header (line starting with '#') found in the markdown.")

def generate_page(from_path, template_path, dest_path, basepath):
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
        rendered_html = rendered_html.replace('href="/', f'href="{basepath}')
        rendered_html = rendered_html.replace('src="/', f'src="{basepath}')
    
    with open(dest_path, 'w', encoding='utf-8') as output_file:
        output_file.write(rendered_html)
    
    print(f"Generated page from {from_path} to {dest_path} using {template_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Processing directory: {dir_path_content}")
    
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Get all items in the current directory
    try:
        items = os.listdir(dir_path_content)
    except Exception as e:
        print(f"Error listing directory {dir_path_content}: {e}")
        return
    
    for item in items:
        # Skip hidden files and directories
        if item.startswith('.'):
            continue
        
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path):
            # Only process markdown files
            if item.endswith('.md'):
                # Convert filename.md to filename.html
                html_filename = os.path.splitext(item)[0] + '.html'
                html_path = os.path.join(dest_dir_path, html_filename)
                
                print(f"Generating: {item_path} -> {html_path}")
                generate_page(item_path, template_path, html_path, basepath)
        
        elif os.path.isdir(item_path):
            # Create equivalent directory in destination
            new_dest_dir = os.path.join(dest_dir_path, item)
            
            # Recursively process the subdirectory
            generate_pages_recursive(item_path, template_path, new_dest_dir, basepath) 

if __name__ == "__main__":
    #generate_page('content/index.md', 'template.html', 'public/index.html')
    dir_path_content = "content/"
    template_path = ""
    dest_dir_path = "public/"
    basepath = ""
    
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)