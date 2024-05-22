import networkx as nx
from typing import List
from multilevel_graphs import DecGraph, Supernode


def enumerate_all_cliques(dec_graph: DecGraph, reciprocal: bool = False) -> List[List[Supernode]]:
    """
    Enumerates all the cliques in the given decontractible graph as a set of sets of supernodes.
    The cliques are calculated on the undirected version of the given decontractible graph, obtained by
    keeping only edges that appear in both directions in the original digraph or not, depending on the value of the
    reciprocal parameter.
    The cliques are found using the Bron-Kerbosch algorithm.

    :param dec_graph: the decontractible graph
    :param reciprocal: If True, cliques are calculated on the undirected version of the given decontractible graph
     conteining only edges that appear in both directions in the original decontractible graph.
    """
    undirected_graph = dec_graph._graph.to_undirected(reciprocal=reciprocal)
    cliques = list(nx.find_cliques(undirected_graph))
    return list(map(lambda c: list(map(lambda n: dec_graph.V[n], c)), cliques))