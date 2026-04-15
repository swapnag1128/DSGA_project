# Property-Based Testing of Graph Algorithms using NetworkX

## Team Members
Swapna Gundeboyina
SR No - 26280
---

## Project Overview

This project applies **property-based testing** using the Hypothesis library to validate the correctness of graph algorithms implemented in NetworkX.

Unlike traditional unit tests that rely on fixed examples, property-based tests automatically generate diverse graph inputs and verify that key mathematical properties always hold.

---

## Algorithms Tested

We selected core graph analytics algorithms from NetworkX:

* Shortest Path (Dijkstra)
* Minimum Spanning Tree (MST)
* Connected Components

---

## Properties Verified

Our tests cover multiple categories of correctness:

### Invariants

* Triangle inequality for shortest paths
* MST is acyclic
* Connected components are disjoint

### Postconditions

* Shortest path returns valid paths
* MST has at most (n - 1) edges
* Components cover all nodes

### Metamorphic Properties

* Scaling edge weights scales shortest path distances
* Adding a constant to weights does not change MST
* Adding edges does not increase number of components

### Idempotence

* Running algorithms multiple times produces consistent results

### Boundary Conditions

* Empty graphs
* Single-node graphs
* Disconnected graphs

---

## Graph Generation

We use Hypothesis strategies to generate diverse graph inputs:

* Random sizes (1–10 nodes)
* Sparse and dense graphs
* Weighted graphs (positive weights)
* Connected and disconnected structures

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running Tests

```bash
pytest test_property_based.py
```

---

## Why Property-Based Testing?

Property-based testing ensures that algorithms are validated against **general mathematical truths**, not just specific examples.

This approach:

* Improves test coverage
* Detects edge cases automatically
* Reveals hidden bugs

---

## Project Structure

```
networkx-property-testing/
│
├── test_property_based.py
├── requirements.txt
├── README.md

---

## Future Enhancements

* Add tests for centrality measures
* Extend to flow algorithms (max-flow/min-cut)
* Integrate coverage reports

---

## Technologies Used

* Python
* NetworkX
* Hypothesis
* Pytest

---

## Conclusion

This project demonstrates how property-based testing can rigorously validate graph algorithms by enforcing fundamental mathematical properties across a wide range of automatically generated inputs.

