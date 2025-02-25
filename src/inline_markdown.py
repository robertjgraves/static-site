from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result_nodes.append(node)
            continue
            
        first_delimiter = node.text.find(delimiter)
        if first_delimiter == -1:
            result_nodes.append(node)
            continue
            
        remaining_text = node.text[first_delimiter + len(delimiter):]
        
        # Look for exact matching delimiter
        second_delimiter_in_remaining = -1
        current_pos = 0
        while current_pos <= len(remaining_text) - len(delimiter):
            if remaining_text[current_pos:current_pos + len(delimiter)] == delimiter:
                second_delimiter_in_remaining = current_pos
                break
            current_pos += 1
            
        if second_delimiter_in_remaining == -1:
            raise Exception("second delimiter not found")
            
        second_delimiter = first_delimiter + len(delimiter) + second_delimiter_in_remaining
        
        before_text = node.text[:first_delimiter]
        middle_text = node.text[first_delimiter + len(delimiter):second_delimiter]
        after_text = node.text[second_delimiter + len(delimiter):]
        
        result_nodes.append(TextNode(before_text, TextType.TEXT))
        result_nodes.append(TextNode(middle_text, text_type))
        result_nodes.append(TextNode(after_text, TextType.TEXT))
            
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

def text_to_textnodes(text):
    # First split into bold nodes
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Only process non-bold nodes for other delimiters
    result = []
    for node in nodes:
        if node.text_type == TextType.BOLD:
            # Don't process bold nodes any further
            result.append(node)
        else:
            # Process other delimiters only for text nodes
            current = [node]
            current = split_nodes_delimiter(current, "*", TextType.ITALIC)
            current = split_nodes_delimiter(current, "`", TextType.CODE)
            
            # Handle images and links
            for n in current:
                if n.text_type != TextType.TEXT:
                    result.append(n)
                    continue
                    
                image_nodes = split_nodes_image(n)
                for img_node in image_nodes:
                    if img_node.text_type == TextType.TEXT:
                        result.extend(split_nodes_link(img_node))
                    else:
                        result.append(img_node)
                        
    return result