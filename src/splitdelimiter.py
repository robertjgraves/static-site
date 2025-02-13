from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    
    for node in old_nodes:

        if node.text_type == TextType.TEXT:
            first_delimiter = node.text.find(delimiter)
            
            #print(f"first_delimiter:\t{first_delimiter}")
            
            
            if first_delimiter == -1:
                result_nodes.append(node)

            else:
                second_delimiter = node.text.find(delimiter, first_delimiter + 1)
                #print(f"second_delimiter:\t{second_delimiter}")

                if second_delimiter == -1:
                    raise Exception("second delimiter not found")
            
                else:
                    before_text = node.text[:first_delimiter]
                    middle_text = node.text[first_delimiter + len(delimiter):second_delimiter]
                    after_text = node.text[second_delimiter + len(delimiter):]
                    result_nodes.append(TextNode(before_text, TextType.TEXT))
                    result_nodes.append(TextNode(middle_text, text_type))
                    result_nodes.append(TextNode(after_text, TextType.TEXT))
                    #print(f"before_text:\t{before_text}")
                    #print(f"middle_text:\t{middle_text}")
                    #print(f"after_text:\t{after_text}")
        else:
            result_nodes.append(node)# add node directly to results
    
    return result_nodes


#node = TextNode("This is text with a `code block` word", TextType.TEXT)
#new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

#print(f"new nodes: \t{new_nodes}")