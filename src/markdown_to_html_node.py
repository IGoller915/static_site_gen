from textfunctions import *
from textnode import *
from htmlnode import *
from blocktype import *
import re

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    node_list = []
    for block in md_blocks:
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.PARAGRAPH:
                clean_block = (block.replace("\n", " "))
                children = text_to_children(clean_block)
                block_node = ParentNode("p", children)
                node_list.append(block_node)
            case BlockType.HEADING:
                heading_number = len(re.search(r"(^#+)", block).group(0))
                clean_block = block.strip("# ")
                children = text_to_children(clean_block)
                block_node = ParentNode(f"h{heading_number}", children)
                node_list.append(block_node)
            case BlockType.CODE:
                clean_block = block.lstrip("`\n").rstrip("`")
                inner_block_node = LeafNode("code", clean_block)
                outer_block_node = ParentNode("pre", [inner_block_node])
                node_list.append(outer_block_node)
            case BlockType.QUOTE:
                clean_block = block.replace("> ", "")
                children = text_to_children(clean_block)
                block_node = ParentNode("blockquote", children)
                node_list.append(block_node)
            case BlockType.ORDERED_LIST:
                split_block = re.split("\d\. ", block)
                clean_split_block = [item.strip("\n") for item in split_block if item.strip()]
                children = [ParentNode("li", text_to_children(block)) for block in clean_split_block]
                block_node = ParentNode("ol", children)
                node_list.append(block_node)
            case BlockType.UNORDERED_LIST:
                clean_split_block = block.strip("- ").split("\n- ")
                children = [ParentNode("li", text_to_children(block)) for block in clean_split_block]
                block_node = ParentNode("ul", children)
                node_list.append(block_node)

    return ParentNode("div", node_list)

def text_to_children(text):
    text_nodes_list = text_to_textnodes(text)
    html_nodes_list = [text_node_to_html_node(text_node) for text_node in text_nodes_list]
    return html_nodes_list  


# md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

# print(markdown_to_html_node(md).to_html())