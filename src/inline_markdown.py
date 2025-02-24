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

def split_nodes_image(old_nodes):
    images = extract_markdown_images(old_nodes.text)

    if not images:
        return [old_nodes]
    
    results = []
    remaining_text = old_nodes.text

    for image_alt, image_link in images:
        sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)

        if sections[0]:
            text_node = TextNode(sections[0], TextType.TEXT)
            results.append(text_node)
        
        image_node = TextNode(image_alt, TextType.IMAGE, image_link)
        results.append(image_node)

        remaining_text = sections[1]

    if len(images) == 1:
        text_node = TextNode(remaining_text, TextType.TEXT)
        results.append(text_node)
    elif remaining_text:
        text_node = TextNode(remaining_text, TextType.TEXT)
        results.append(text_node)
    
    return results

def split_nodes_link(old_nodes):
    links = extract_markdown_links(old_nodes.text)
    
    if not links:
        return [old_nodes]
    
    results = []
    remaining_text = old_nodes.text

    for link_text, link_url in links:
        sections = remaining_text.split(f"[{link_text}]({link_url})", 1)

        if sections[0]:
            text_node = TextNode(sections[0], TextType.TEXT)
            results.append(text_node)

        link_node = TextNode(link_text, TextType.LINK, link_url)
        results.append(link_node)
        
        remaining_text = sections[1]

    if len(links) == 1:
        text_node = TextNode(remaining_text, TextType.TEXT)
        results.append(text_node)
    elif remaining_text:
        text_node = TextNode(remaining_text, TextType.TEXT)
        results.append(text_node)    
        
    return results