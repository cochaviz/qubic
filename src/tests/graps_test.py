from unittest import TestCase

from src.graph import Graph


class GraphTest(TestCase):

    def test_no_cycle(self):
        g = Graph()
        g.add_edge('a', 'b', 'x1')
        g.add_edge('b', 'c', 'x2')

        assert g.get_cycle('b') is None

    def test_one_node(self):
        g = Graph()
        g.add_node('1')

        assert g.get_cycle('1') is None

    def test_two_node_cycle(self):
        g = Graph()
        g.add_edge('1', '2', 'a')
        g.add_edge('1', '2', 'b')

        [nodes, edges] = g.get_cycle('1')
        assert sorted(nodes) == sorted(['1', '2'])
        assert sorted(edges) == sorted(['a', 'b'])

    def test_two_node_cycle_revered(self):
        g = Graph()
        g.add_edge('1', '2', 'a')
        g.add_edge('2', '1', 'b')

        [nodes, edges] = g.get_cycle('1')
        assert sorted(nodes) == sorted(['1', '2'])
        assert sorted(edges) == sorted(['a', 'b'])

    def test_three_nodes_cycle(self):
        g = Graph()
        g.add_edge('1', '2', 'ab')
        g.add_edge('2', '3', 'bc')
        g.add_edge('3', '1', 'ca')

        [nodes, edges] = g.get_cycle('1')
        assert sorted(nodes) == sorted(['1', '2', '3'])
        assert sorted(edges) == sorted(['ca', 'bc', 'ab'])

    def test_random_cycle(self):
        g = Graph()
        g.add_edge('1', '2', 'a')
        g.add_edge('2', '3', 'b')
        g.add_edge('5', '6', 'c')
        g.add_edge('3', '5', 'd')
        g.add_edge('3', '6', 'e')

        res = g.get_cycle('6')
        assert res is not None

        [nodes, edges] = res
        assert sorted(nodes) == sorted(['3', '5', '6'])
        assert sorted(edges) == sorted(['d', 'c', 'e'])

    def test_remove_cycle_on_random_graph(self):
        g = Graph()
        g.add_edge('1', '2', 'a')
        g.add_edge('2', '3', 'b')
        g.add_edge('5', '6', 'c')
        g.add_edge('3', '5', 'd')
        g.add_edge('3', '6', 'e')

        g.remove_cycle([['3', '5'], ['b', 'c', 'd', 'e']])
        print(g.nodes)
        print(g.edges)
        assert g.has_node('1')
        assert g.has_node('2')
        assert not g.has_node('3')
        assert not g.has_node('5')
        assert g.has_node('6')
