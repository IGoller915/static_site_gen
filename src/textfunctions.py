from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.extend(node)
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid markdown syntax - unmatched delimiters")
        
        split_text = node.text.split(f"{delimiter}")

        #Case where text node starts with delimiter - odd indexes should get new text type, but index 0 needs skipping
        if split_text[0] == "":
            i = 1
        else:
            i = 0
        while i < len(split_text):
            if split_text[i] != "":
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
            i += 1
        #When text node does not start with delimiter, odd indexes still get new text type, but start at index 0
        
    return new_nodes