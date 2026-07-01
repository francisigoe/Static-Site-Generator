from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
from enum import Enum
import re 

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        seperate = node.text
        while True:
            seperate = seperate.split(delimiter,maxsplit=2)
            if len(seperate) == 2:
                raise ValueError(f"node value:`",{node.text},"` is missing a closing delimiter.")
            if len(seperate) == 1:
                node1 = TextNode(seperate[0], TextType.TEXT)
                return_nodes.append(node1)
                break
            node1 = TextNode(seperate[0], TextType.TEXT)
            return_nodes.append(node1)
            node2 = TextNode(seperate[1], text_type)
            return_nodes.append(node2)
            seperate = seperate[2]

    return return_nodes

def extract_markdown_images(node_text: str) -> (tuple):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node_text)
    return result

def extract_markdown_links(text: str) -> (tuple):
    result = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images == []:
            return_nodes.append(node)
            continue
        seperate = node.text
        for image in images:
            seperate = seperate.split(f"![{image[0]}]({image[1]})",maxsplit=1)
            if len(seperate) == 1:
                node1 = TextNode(seperate[0], TextType.TEXT)
                return_nodes.append(node1)
                break
            node1 = TextNode(seperate[0], TextType.TEXT)
            return_nodes.append(node1)
            node2 = TextNode(image[0],TextType.IMAGE,image[1])
            return_nodes.append(node2)
            seperate = seperate[1]
        if len(seperate) > 0:
            return_nodes.append(TextNode(seperate, TextType.TEXT))
    
    return return_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links == []:
            return_nodes.append(node)
            continue
        seperate = node.text
        for link in links:
            seperate = seperate.split(f"[{link[0]}]({link[1]})",maxsplit=1)
            if len(seperate) == 1:
                node1 = TextNode(seperate[0], TextType.TEXT)
                return_nodes.append(node1)
                break
            node1 = TextNode(seperate[0], TextType.TEXT)
            return_nodes.append(node1)
            node2 = TextNode(link[0],TextType.LINK,link[1])
            return_nodes.append(node2)
            seperate = seperate[1]
        if len(seperate) > 0:
            return_nodes.append(TextNode(seperate, TextType.TEXT))
    return return_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown: str) -> list:
    result = []
    splited = markdown.split("\n\n")
    for item in range(0,len(splited)):
        splited[item] = splited[item].strip()
        if splited[item]:
            result.append(splited[item])
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block:str) -> BlockType:
    splited = markdown_block.split("\n")
    starts_with = True 
    if markdown_block.startswith("#"):
        return BlockType.HEADING
    if (markdown_block.startswith("```\n") and markdown_block.endswith("\n```")):
        return BlockType.CODE
    starts_with = True
    for line in splited:
        if not line.startswith(">"):
            starts_with = False
            break
    if starts_with == True:
        return BlockType.QUOTE
    starts_with = True
    for line in splited:
        if not line.startswith("- "):
            starts_with = False
            break
    if starts_with == True:
        return BlockType.UNORDERED_LIST
    starts_with = True
    count = 1
    for line in splited:
        if not line.startswith(f"{count}. "):
            starts_with = False
            break
        count += 1
    if starts_with == True:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH  

def markdown_to_html_node(markdown: str):
    #print(markdown)
    result = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        #print(block,block_type)
        if block_type == BlockType.PARAGRAPH:
            block_html_nodes = paragraph_block_to_html_node(block)
            result.append(block_html_nodes)
        if block_type == BlockType.HEADING:
            block_html_nodes = heading_block_to_html_node(block)
            result.append(block_html_nodes)
        if block_type == BlockType.CODE:
            block_html_nodes = code_block_to_html_node(block)
            result.append(block_html_nodes)
        if block_type == BlockType.UNORDERED_LIST:
            block_html_nodes = unordered_list_block_to_html_node(block)
            result.append(block_html_nodes)
        if block_type == BlockType.ORDERED_LIST:
            block_html_nodes = ordered_list_block_to_html_node(block)
            result.append(block_html_nodes)
        if block_type == BlockType.QUOTE:
            block_html_nodes = quote_block_to_html_node(block)
            result.append(block_html_nodes)
    return ParentNode("div",result)


def paragraph_block_to_html_node(text):
    splited = text.split("\n") 
    for item in range(0,len(splited)):
        splited[item] = splited[item].strip()
        if splited[item]:
                one_line_text = " ".join(splited)
    children = text_to_children(one_line_text)
    parent_node = ParentNode("p",children)
    return parent_node

def heading_block_to_html_node(text):
    if text.startswith("######"):
        head = "h6"
        text = text[6:]
    elif text.startswith("#####"):
        head = "h5"
        text = text[5:]
    elif text.startswith("####"):
        head = "h4"
        text = text[4:]
    elif text.startswith("###"):
        head = "h3"
        text = text[3:]
    elif text.startswith("##"):
        head = "h2"
        text = text[2:]
    else:
        head = "h1"
        text = text[1:]
    children = text_to_children(text)
    parent_node = ParentNode(head,children)
    return parent_node

def code_block_to_html_node(text):
    text = text[4:]
    text = text[:-3]
    node = TextNode(text=text, text_type=TextType.TEXT)
    grandchild_node = text_node_to_html_node(node)
    child_node = ParentNode("code",[grandchild_node])
    parent_node = ParentNode("pre",[child_node])
    return parent_node


def quote_block_to_html_node(text):
    text = text[1:]
    children = text_to_children(text)
    parent_node = ParentNode("blockquote",children)
    return parent_node

def ordered_list_block_to_html_node(text):
    children = []
    lis = text.split("\n")
    for l in lis:
        grandchildren = text_to_children(l[3:])
        children.append(ParentNode("li",grandchildren))
    #print("here",lis)
    parent_node = ParentNode("ol",children)
    return parent_node

def unordered_list_block_to_html_node(text):
    children = []
    lis = text.split("\n")
    for l in lis:
        grandchildren = text_to_children(l[2:])
        children.append(ParentNode("li",grandchildren))
    #print("here",lis)
    parent_node = ParentNode("ul",children)
    return parent_node

def text_to_children(text):
    children = []
    nodes = text_to_textnodes(text) 
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children
