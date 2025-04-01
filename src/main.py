from copystatic import delete_directory_contents, copy_folder_recursive
from textnode import TextNode, TextType
from page_generator import generate_page, generate_pages_recursive
import os

def main():
    source_folder = "./static"
    destination_folder = "./public"
    
    delete_directory_contents(destination_folder)
    copy_folder_recursive(source_folder, destination_folder)
    
    #markdown_file = "content/index.md"
    #template_file = "template.html"
    #destination_file = "public/index.html"
    
    #generate_page('content/index.md', 'template.html', 'public/index.html')
    #generate_page(markdown_file, template_file, destination_file)

    # Print current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # Use absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.abspath(os.path.join(script_dir, '..', 'content'))
    template_path = os.path.abspath(os.path.join(script_dir, '..', 'template.html'))
    public_dir = os.path.abspath(os.path.join(script_dir, '..', 'public'))
    
    print(f"Content directory: {content_dir}")
    print(f"Template path: {template_path}")
    print(f"Public directory: {public_dir}")
    
    # Check if content directory exists
    if not os.path.exists(content_dir):
        print(f"ERROR: Content directory does not exist: {content_dir}")
        return
        
    # Generate pages
    generate_pages_recursive(content_dir, template_path, public_dir)

main()