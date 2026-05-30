import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
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
if __name__ == "__main__":
    unittest.main()