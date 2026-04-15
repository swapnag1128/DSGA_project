"""
===========================================
Property-Based Testing for Graph Algorithms
===========================================

Team Members:
- Swapna Gundeboyina

Algorithms Tested:
- Shortest Path (Dijkstra)
- Minimum Spanning Tree (MST)
- Connected Components

Description:
This file contains property-based tests using Hypothesis to validate
core invariants, postconditions, metamorphic properties, idempotence,
and boundary conditions of graph algorithms implemented in NetworkX.
"""

# ========================
# Imports
# ========================
import networkx as nx
from hypothesis import given, strategies as st


# ========================
# Graph Generation Helpers
# ========================

@st.composite
def undirected_graphs(draw):
    n = draw(st.integers(min_value=1, max_value=10))
    m = draw(st.integers(min_value=0, max_value=n*(n-1)//2))
    seed = draw(st.integers(min_value=0, max_value=10_000))

    return nx.gnm_random_graph(n, m, seed=seed)


@st.composite
def weighted_graphs(draw):
    G = draw(undirected_graphs())

    for u, v in G.edges():
        G[u][v]['weight'] = draw(st.integers(min_value=1, max_value=10))

    return G


# ========================
# Shortest Path Tests
# ========================

@given(weighted_graphs())
def test_triangle_inequality(G):
    """
    Property: Triangle Inequality for Shortest Paths

    Ensures that for any nodes u, v, x:
        d(u, v) ≤ d(u, x) + d(x, v)

    Importance:
    This is a fundamental property of shortest path algorithms.
    Any violation indicates incorrect distance computation.

    Graphs:
    Random weighted graphs with positive weights.

    Assumptions:
    Nodes must be connected for paths to exist.

    Failure Meaning:
    Indicates incorrect implementation of Dijkstra or path relaxation logic.
    """
    nodes = list(G.nodes())
    if len(nodes) < 3:
        return

    u, v, x = nodes[:3]

    try:
        d_uv = nx.dijkstra_path_length(G, u, v)
        d_ux = nx.dijkstra_path_length(G, u, x)
        d_xv = nx.dijkstra_path_length(G, x, v)

        assert d_uv <= d_ux + d_xv
    except nx.NetworkXNoPath:
        pass


@given(weighted_graphs())
def test_shortest_path_validity(G):
    """
    Property: Path Validity

    Ensures that the computed shortest path:
    - Starts at source
    - Ends at destination
    - Uses valid edges

    Importance:
    Guarantees correctness of returned path structure.

    Failure Meaning:
    Indicates invalid path construction.
    """
    nodes = list(G.nodes())
    if len(nodes) < 2:
        return

    u, v = nodes[0], nodes[-1]

    try:
        path = nx.dijkstra_path(G, u, v)

        assert path[0] == u
        assert path[-1] == v

        for i in range(len(path)-1):
            assert G.has_edge(path[i], path[i+1])
    except nx.NetworkXNoPath:
        pass


@given(weighted_graphs(), st.integers(min_value=1, max_value=5))
def test_weight_scaling(G, factor):
    """
    Property: Weight Scaling (Metamorphic)

    Scaling all edge weights by a factor should scale shortest path
    distance by the same factor.

    Importance:
    Validates correctness under transformation of weights.

    Failure Meaning:
    Indicates incorrect handling of weights.
    """
    nodes = list(G.nodes())
    if len(nodes) < 2:
        return

    u, v = nodes[0], nodes[-1]

    try:
        d1 = nx.dijkstra_path_length(G, u, v)

        G2 = G.copy()
        for a, b in G2.edges():
            G2[a][b]['weight'] *= factor

        d2 = nx.dijkstra_path_length(G2, u, v)

        assert d2 == d1 * factor
    except nx.NetworkXNoPath:
        pass


# ========================
# MST Tests
# ========================

@given(weighted_graphs())
def test_mst_edge_count(G):
    """
    Property: MST Edge Count

    A spanning tree must have at most (n - 1) edges.

    Importance:
    Ensures tree structure (no cycles).

    Failure Meaning:
    Indicates cycles or incorrect MST construction.
    """
    if len(G.nodes()) == 0:
        return

    T = nx.minimum_spanning_tree(G)

    assert len(T.edges()) <= len(G.nodes()) - 1


@given(weighted_graphs())
def test_mst_is_forest(G):
    """
    Property: Acyclic Structure

    MST must not contain cycles.

    Importance:
    Fundamental property of trees.

    Failure Meaning:
    Indicates incorrect edge selection.
    """
    T = nx.minimum_spanning_tree(G)
    assert nx.is_forest(T)


@given(weighted_graphs(), st.integers(min_value=1, max_value=10))
def test_mst_weight_shift(G, c):
    """
    Property: Weight Shift Invariance

    Adding constant to all weights should not change MST structure.

    Importance:
    MST depends only on relative ordering.

    Failure Meaning:
    Indicates algorithm incorrectly depends on absolute weights.
    """
    if len(G.edges()) == 0:
        return

    T1 = nx.minimum_spanning_tree(G)

    G2 = G.copy()
    for u, v in G2.edges():
        G2[u][v]['weight'] += c

    T2 = nx.minimum_spanning_tree(G2)

    assert set(T1.edges()) == set(T2.edges())


# ========================
# Connected Components Tests
# ========================

@given(undirected_graphs())
def test_components_cover_all_nodes(G):
    """
    Property: Partition Coverage

    All nodes must appear in exactly one connected component.

    Importance:
    Ensures correctness of component detection.

    Failure Meaning:
    Missing or duplicated nodes in components.
    """
    comps = list(nx.connected_components(G))
    union = set().union(*comps) if comps else set()

    assert union == set(G.nodes())


@given(undirected_graphs())
def test_components_disjoint(G):
    """
    Property: Disjoint Components

    Connected components must be pairwise disjoint.

    Importance:
    Defines valid partition.

    Failure Meaning:
    Overlapping components indicate incorrect grouping.
    """
    comps = list(nx.connected_components(G))

    for i in range(len(comps)):
        for j in range(i+1, len(comps)):
            assert comps[i].isdisjoint(comps[j])


@given(undirected_graphs())
def test_adding_edge_reduces_components(G):
    """
    Property: Edge Addition (Metamorphic)

    Adding an edge cannot increase number of components.

    Importance:
    Connectivity is monotonic under edge addition.

    Failure Meaning:
    Indicates incorrect connectivity computation.
    """
    nodes = list(G.nodes())
    if len(nodes) < 2:
        return

    before = nx.number_connected_components(G)

    G.add_edge(nodes[0], nodes[-1])

    after = nx.number_connected_components(G)

    assert after <= before


# ========================
# Boundary Tests
# ========================

def test_empty_graph():
    """
    Property: Empty Graph Behavior

    Ensures algorithms handle empty graphs correctly.

    Importance:
    Edge-case robustness.

    Failure Meaning:
    Algorithm does not handle base cases properly.
    """
    G = nx.Graph()

    assert list(nx.connected_components(G)) == []
