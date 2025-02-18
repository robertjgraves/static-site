from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    
    for node in old_nodes:

        if node.text_type == TextType.TEXT:
            first_delimiter = node.text.find(delimiter)
                        
            if first_delimiter == -1:
                result_nodes.append(node)

            else:
                second_delimiter = node.text.find(delimiter, first_delimiter + 1)

                if second_delimiter == -1:
                    raise Exception("second delimiter not found")
            
                else:
                    before_text = node.text[:first_delimiter]
                    middle_text = node.text[first_delimiter + len(delimiter):second_delimiter]
                    after_text = node.text[second_delimiter + len(delimiter):]
                    result_nodes.append(TextNode(before_text, TextType.TEXT))
                    result_nodes.append(TextNode(middle_text, text_type))
                    result_nodes.append(TextNode(after_text, TextType.TEXT))
 
        else:
            result_nodes.append(node)# add node directly to results
    
    return result_nodes

def extract_markdown_images(text):
    
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches