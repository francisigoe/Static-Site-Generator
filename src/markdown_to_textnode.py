from textnode import TextNode, TextType
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
