import unittest

from multilevel_graphs import DecGraph, Supernode, Superedge, CyclesContractionScheme


class CycleContractionSchemeTest(unittest.TestCase):

    def test_contract_non_maximal(self):
        sample_graph = self._sample_dec_graph()
        contracted_graph = CyclesContractionScheme(maximal=False).contract(sample_graph)

        self.assertEqual(4, len(contracted_graph.V))
        self.assertEqual(6, len(contracted_graph.E))
        self.assertEqual(2, len(sample_graph.V[1].supernode.dec.nodes()))
        self.assertEqual(sample_graph.V[1].supernode, sample_graph.V[2].supernode)
        self.assertEqual(1, len(sample_graph.V[3].supernode.dec.nodes()))
        self.assertEqual(3, len(sample_graph.V[3].supernode.component_sets))
        self.assertEqual(2, len(sample_graph.V[4].supernode.component_sets))
        self.assertEqual(1, len(sample_graph.V[5].supernode.component_sets))
        self.assertEqual(sample_graph, contracted_graph.complete_decontraction())

    def test_contract_maximal(self):
        sample_graph = self._sample_dec_graph()
        contracted_graph = CyclesContractionScheme(maximal=True).contract(sample_graph)

        self.assertEqual(3, len(contracted_graph.V))
        self.assertEqual(4, len(contracted_graph.E))
        self.assertEqual(2, len(sample_graph.V[1].supernode.dec.nodes()))
        self.assertEqual(sample_graph.V[1].supernode, sample_graph.V[2].supernode)
        self.assertEqual(2, len(sample_graph.V[3].supernode.dec.nodes()))
        self.assertEqual(sample_graph.V[3].supernode, sample_graph.V[4].supernode)
        self.assertEqual(1, len(sample_graph.V[1].supernode.component_sets))
        self.assertEqual(2, len(sample_graph.V[3].supernode.component_sets))
        self.assertEqual(1, len(sample_graph.V[5].supernode.component_sets))
        self.assertEqual({sample_graph.E[(2, 4)], sample_graph.E[(2, 3)]},
                         contracted_graph.E[(sample_graph.V[1].supernode.key, sample_graph.V[3].supernode.key)].dec)
        self.assertEqual(sample_graph, contracted_graph.complete_decontraction())

    def test_contract_with_supernode_attr_function(self):
        def supernode_attr_function(supernode: Supernode):
            return {"weight": sum([node['weight'] for node in supernode.dec.nodes()]) + 1}

        sample_graph = self._sample_dec_graph()
        scheme = CyclesContractionScheme(supernode_attr_function=supernode_attr_function, maximal=True)
        contracted_graph = scheme.contract(sample_graph)

        self.assertEqual(self._sample_dec_graph(), contracted_graph.complete_decontraction())
        self.assertEqual(51, sample_graph.V[1].supernode['weight'])
        self.assertEqual(26, sample_graph.V[4].supernode['weight'])
        self.assertEqual(16, sample_graph.V[5].supernode['weight'])

    def test_contract_with_superedge_attr_function(self):
        def supernode_attr_function(supernode: Supernode):
            return {"weight": sum([node['weight'] for node in supernode.dec.nodes()])}

        def superedge_attr_function(superedge: Superedge):
            return {"weight": max(superedge.tail['weight'], superedge.head['weight'],
                                  *[edge['weight'] for edge in superedge.dec])}

        sample_graph = self._sample_dec_graph()
        scheme = CyclesContractionScheme(supernode_attr_function=supernode_attr_function,
                                         superedge_attr_function=superedge_attr_function, maximal=True)
        contracted_graph = scheme.contract(sample_graph)

        self.assertEqual(self._sample_dec_graph(), contracted_graph.complete_decontraction())
        self.assertEqual(50, contracted_graph.E[(sample_graph.V[1].supernode.key, sample_graph.V[3].supernode.key)]['weight'])
        self.assertEqual(30, contracted_graph.E[(sample_graph.V[3].supernode.key, sample_graph.V[5].supernode.key)]['weight'])

    def test_contract_with_c_set_attr_function(self):
        def supernode_attr_function(supernode: Supernode):
            return {"weight": sum([node['weight'] for node in supernode.dec.nodes()])}

        def c_set_attr_function(c_set):
            return {"weight": sum([node['weight'] + 1 for node in c_set])}

        sample_graph = self._sample_dec_graph()
        scheme = CyclesContractionScheme(supernode_attr_function=supernode_attr_function,
                                         c_set_attr_function=c_set_attr_function, maximal=False)
        contracted_graph = scheme.contract(sample_graph)

        self.assertEqual(self._sample_dec_graph(), contracted_graph.complete_decontraction())
        self.assertEqual({63, 79}, {c_set['weight'] for c_set in sample_graph.V[1].supernode.component_sets})
        self.assertEqual({79, 43}, {c_set['weight'] for c_set in sample_graph.V[4].supernode.component_sets})
        self.assertEqual({43}, {c_set['weight'] for c_set in sample_graph.V[5].supernode.component_sets})



    @staticmethod
    def _sample_dec_graph() -> DecGraph:
        graph = DecGraph()
        graph.add_node(Supernode(1, level=0, weight=30))
        graph.add_node(Supernode(2, level=0, weight=20))
        graph.add_node(Supernode(3, level=0, weight=10))
        graph.add_node(Supernode(4, level=0, weight=15))
        graph.add_node(Supernode(5, level=0, weight=15))
        graph.add_edge(Superedge(graph.V[1], graph.V[2], weight=5))
        graph.add_edge(Superedge(graph.V[2], graph.V[3], weight=10))
        graph.add_edge(Superedge(graph.V[3], graph.V[1], weight=20))
        graph.add_edge(Superedge(graph.V[2], graph.V[4], weight=10))
        graph.add_edge(Superedge(graph.V[4], graph.V[3], weight=5))
        graph.add_edge(Superedge(graph.V[3], graph.V[5], weight=30))
        graph.add_edge(Superedge(graph.V[5], graph.V[4], weight=10))
        return graph


if __name__ == '__main__':
    unittest.main()
