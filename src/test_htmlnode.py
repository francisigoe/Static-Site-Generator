import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props = {
    "href": "https://www.google.com",
    "target": "_blank",
    })
        node2 = HTMLNode(props = {
    "href": "https://www.google.com",
    "target": "_blank",
    })
        node3 = HTMLNode(props = {})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        self.assertNotEqual(node.props_to_html(), node3.props_to_html())
        self.assertNotEqual(node2.props_to_html(), node3.props_to_html())
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2  = LeafNode("a", "Whatup Earth?")
        node3  = LeafNode("a", "Whatup Earth?", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<a>Whatup Earth?</a>")
        self.assertEqual(node3.to_html(), "<a href=\"https://www.google.com\">Whatup Earth?</a>")
if __name__ == "__main__":
    unittest.main()