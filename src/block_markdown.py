from textnode import TextNode, TextType

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
