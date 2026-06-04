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
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
if __name__ == "__main__":
    unittest.main()