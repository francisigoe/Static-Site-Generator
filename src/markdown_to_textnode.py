from textnode import TextNode, TextType


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

