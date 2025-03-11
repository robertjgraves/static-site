from copystatic import delete_directory_contents, copy_folder_recursive
from textnode import TextNode, TextType


def main():
    source_folder = "./static"
    destination_folder = "./public"
    delete_directory_contents(destination_folder)
    copy_folder_recursive(source_folder, destination_folder)

main()