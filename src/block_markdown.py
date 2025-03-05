from enum import Enum
import re
from textnode import TextNode, TextType

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
