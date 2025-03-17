import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.derp.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.herp.com")
        self.assertNotEqual(node, node2)
    
    def test_nourl_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.derp.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.derp.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode("a", "This is a link node", {"href": "www.derp.com"}))
        self.assertEqual(html_node.props["href"], "www.derp.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.derp.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node, LeafNode("img", "", {"source": "www.derp.com", "alt": "This is an image node"}))
        
    def test_invalid(self):
        node = TextNode("This is not a node", "not a valid type", "www.derp.com")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()