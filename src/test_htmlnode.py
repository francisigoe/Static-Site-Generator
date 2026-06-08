import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])   
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("a", "child2")
        parent_node = ParentNode("div", [child_node1,child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><a>child2</a></div>")
if __name__ == "__main__":
    unittest.main()