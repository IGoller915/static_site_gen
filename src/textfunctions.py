from textnode import *
from blocktype import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches  

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", node.text)
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 1:
                match = re.search(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", split_text[i])
                new_nodes.append(TextNode(match.group(1), TextType.IMAGE, match.group(2)))
            else:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = re.split(r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", node.text)
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 1:
                match = re.search(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", split_text[i])
                new_nodes.append(TextNode(match.group(1), TextType.LINK, match.group(2)))
            else:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_image(code)
    parsed_text_nodes = split_nodes_link(image)
    return parsed_text_nodes

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = [block.strip() for block in split_markdown]
    final_blocks = [block for block in blocks if re.search(r"\w", block)]
    return final_blocks

def block_to_blocktype(block):
    if bool(re.search(r"^#{1,6}", block)):
        return BlockType.HEADING
    if bool(re.search(r"^```[\s\S]+?```$", block)):
        return BlockType.CODE
    if bool(re.search(r"^>.*(\n>.*)*$", block)):
        return BlockType.QUOTE
    if bool(re.search(r"^-\s.*(\n-\s.*)*$", block)):
        return BlockType.UNORDERED_LIST
    if bool(re.search(r"^1\.\s.*(\n2\.\s.*)*(\n3\.\s.*)*(\n\d\.\s.*)*$", block)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH