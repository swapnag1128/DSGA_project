%%writefile test_property_based.py
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
core properties of graph algorithms implemented in NetworkX.
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


