import unittest
from textnode import TextNode, TextType, text_node_to_html_node 


class TestTextNode(unittest.TestCase):
    def test_eq_or_not(self):
        node = TextNode("This is the same text", TextType.BOLD)
        node2 = TextNode("This is the same text", TextType.BOLD)
        node3 = TextNode("This is different text", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

    def test_type_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_type_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        
    def test_type_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_type_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_type_link(self):
        node = TextNode("This is a code node", TextType.LINK, url = "https://www.boot.dev" )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        
    def test_type_image(self):
        node = TextNode("image could not display properly", TextType.IMAGE,url = "https://www.boot.dev" )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "image could not display properly"},)
        
if __name__ == "__main__":
    unittest.main()