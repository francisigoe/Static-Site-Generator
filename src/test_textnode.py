import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_or_not(self):
        node = TextNode("This is the same text", TextType.BOLD)
        node2 = TextNode("This is the same text", TextType.BOLD)
        node3 = TextNode("This is different text", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

if __name__ == "__main__":
    unittest.main()