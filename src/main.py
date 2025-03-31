from copystatic import delete_directory_contents, copy_folder_recursive
from textnode import TextNode, TextType
from page_generator import generate_page

def main():
    source_folder = "./static"
    destination_folder = "./public"
    
    delete_directory_contents(destination_folder)
    copy_folder_recursive(source_folder, destination_folder)
    
    markdown_file = "content/index.md"
    template_file = "template.html"
    destination_file = "public/index.html"
    
    #generate_page('content/index.md', 'template.html', 'public/index.html')
    generate_page(markdown_file, template_file, destination_file)


main()