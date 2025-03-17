import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("a", "This is a link", None, {"href": "www.derp.com"})
        self.assertNotEqual(node, node2)

    def test_rep(self):
        node_self_rep = HTMLNode("a", "This is a link", None, {"href": "www.derp.com"}).__repr__()
        str_value = "HTMLNode(a, This is a link, None, {'href': 'www.derp.com'})"
        self.assertEqual(node_self_rep, str_value)

    def test_prop_func(self):
        prop_func = HTMLNode("a", "This is a link", None, {"href": "www.derp.com", "target": "_blank",}).props_to_html()
        str_value =  " href=\"www.derp.com\" target=\"_blank\""
        self.assertEqual(prop_func, str_value)
    
    def test_to_html(self):
        node = HTMLNode("a", "This is a link", None, {"href": "www.derp.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()

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
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><span>child2</span></div>",
        )

    def test_to_html_with_nested_parents(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node2 = ParentNode("div", [child_node2])
        parent_node = ParentNode("div", [child_node, parent_node2])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><div><span>child2</span></div></div>",
        )



if __name__ == "__main__":
    unittest.main()