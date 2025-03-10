from enum import Enum
import re
from textnode import TextNode, TextType, text_node_to_html_node#, #text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    # heading block
    if re.match(r'^#{1,6} ', markdown_block):
        return BlockType.HEADING
    
    # code block
    if markdown_block.startswith('```') and markdown_block.endswith('```'):
        return BlockType.CODE

    # quote block
    lines = markdown_block.splitlines()
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # unordered list block
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # ordered list
    is_ordered_list = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False
            break

    if is_ordered_list and lines:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    markdown = markdown.strip()  # Trim entire markdown string
    raw_blocks = markdown.split("\n\n")  # Split into blocks by double newline

    cleaned_blocks = []
    
    for block in raw_blocks:
        lines = block.splitlines()  # Handle block line by line
        valid_lines = [line for line in lines if line.strip()]  # Only non-empty lines
        
        if valid_lines:  # Ensure there are valid lines to process
            # Calculate minimum indentation of non-empty lines
            min_indent = min(len(line) - len(line.lstrip()) for line in valid_lines)
            normalized_lines = [line[min_indent:] for line in lines]
            cleaned_blocks.append("\n".join(normalized_lines).strip())
    
    return [block for block in cleaned_blocks if block.strip()]  # Omit empty blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    html_root = ParentNode('div', [])

    for block in blocks:
        
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            paragraph_node = ParentNode('p', [])
            text_nodes = text_to_textnodes(block)

            for text_node in text_nodes:
                html_child = text_node_to_html_node(text_node)
                paragraph_node.children.append(html_child)
            
            html_root.children.append(paragraph_node)


        elif block_type == BlockType.HEADING:
            heading_lines = block.strip().split('\n')
            
            for line in heading_lines:
                line = line.strip()
            
                if not line.startswith('#'):
                    continue
            
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
            
                content = line[level:].strip()

                header_node = ParentNode(f"h{level}", [])

                text_node = text_to_textnodes(content)

                for text_node in text_node:
                    html_child = text_node_to_html_node(text_node)
                    header_node.children.append(html_child)
                
                html_root.children.append(header_node)

        elif block_type == BlockType.CODE:

            lines = block.strip().split('\n')
            
            if lines and lines[0].strip() == '```' and lines[-1].strip() == '```':

                code_lines = lines[1:-1]

                processed_lines = []
                for line in code_lines:
                    line_content = line.strip()

                    if line_content.startswith("print("):
                        processed_lines.append("    " + line_content)
                    else:
                        processed_lines.append(line_content)
                        
                code_content = '\n'.join(processed_lines)
                raw_text_node = TextNode(code_content, TextType.TEXT)
                child = text_node_to_html_node(raw_text_node)
                code = ParentNode("code", [child])
                pre = ParentNode("pre", [code])
                html_root.children.append(pre)
                
        elif block_type == BlockType.QUOTE:
            lines = block.strip().split('\n')
            quote_lines = []

            for line in lines:
                if line.startswith(">"):

                    if len(line) > 1 and line[1] == ' ':
                        quote_lines.append(line[2:])
                    else:
                        quote_lines.append(line[1:])
            
            quote_content = " ".join(quote_lines)
            
            blockquote_node = ParentNode('blockquote', [])
            text_nodes = text_to_textnodes(quote_content)
            
            for text_node in text_nodes:
                html_child = text_node_to_html_node(text_node)
                blockquote_node.children.append(html_child)
            
            html_root.children.append(blockquote_node)
        
        elif block_type == BlockType.UNORDERED_LIST:
            list_node = ParentNode("ul", [])

            lines = block.strip().split('\n')
            
            for line in lines:

                line = line.strip()
                if line.startswith("- ") or line.startswith("* ") or line.startswith("+ "):

                    item_content = line[2:]
                    
                    li_node = ParentNode("li", [])
                    
                    text_nodes = text_to_textnodes(item_content)
                    for text_node in text_nodes:
                        html_child = text_node_to_html_node(text_node)
                        li_node.children.append(html_child)
                    
                    list_node.children.append(li_node)
            
            html_root.children.append(list_node)
    
        elif block_type == BlockType.ORDERED_LIST:
            list_node = ParentNode("ol", [])
            
            lines = block.strip().split('\n')
            
            for line in lines:
                line = line.strip()

                if re.match(r'^\d+[.)] ', line):

                    match = re.match(r'^\d+[.)] ', line)
                    item_content = line[match.end():]
                    
                    li_node = ParentNode("li", [])
                    
                    text_nodes = text_to_textnodes(item_content)
                    for text_node in text_nodes:
                        html_child = text_node_to_html_node(text_node)
                        li_node.children.append(html_child)
                    
                    list_node.children.append(li_node)
            
            html_root.children.append(list_node)

    return html_root