from collections import defaultdict
from typing import Dict, List, Set, Tuple

import networkit as nk
from loguru import logger

from config import (
    NUM_WORKERS,
)


def construct_graph(
    set_of_duplicate_pairs: Set[Tuple[str, str]],
) -> Tuple[nk.Graph, Dict[str, int]]:
    """
    Constructs a graph where nodes represent document IDs, and edges represent duplicate pairs.

    Parameters:
        set_of_duplicate_pairs (Set[Tuple[str, str]]): A set of tuples where each tuple represents
                                                        a pair of duplicate document IDs.

    Returns:
        Tuple[nk.Graph, Dict[str, int]]: A tuple containing:
            - The constructed graph (nk.Graph).
            - A mapper dictionary that maps document IDs to graph node IDs.
    """
    G = nk.Graph()
    mapper = {}
    for node1_name, node2_name in set_of_duplicate_pairs:
        if node1_name not in mapper:
            mapper[node1_name] = G.addNode()
        if node2_name not in mapper:
            mapper[node2_name] = G.addNode()
        G.addEdge(mapper[node1_name], mapper[node2_name])
    return G, mapper


def find_connected_components(G: nk.Graph) -> Tuple[List[List[int]], int]:
    """
    Finds the connected components in the given graph.

    Parameters:
        G (nk.Graph): The graph object containing nodes and edges.

    Returns:
        Tuple[List[List[int]], int]: A tuple containing:
            - A list of components, where each component is a list of node IDs.
            - The number of connected components.
    """
    cc = nk.components.ConnectedComponents(G)
    cc.run()
    return cc.getComponents(), cc.numberOfComponents()


def generate_connected_components_mp(
    generated_dup_pairs: list[list[str]],
) -> Dict[str, Set[int]]:
    """
    Generates connected components for documents based on duplicate pairs,
    identifies documents to be removed due to high similarity, and returns a mapping of file names
    to duplicate document line indices.

    Parameters:
        generated_dup_pairs: A nested list of duplicate document pairs.

    Returns:
        Dict[str, Set[int]]: A dictionary mapping file names to sets of duplicate document indices.
    """
    logger.info("Started graph building")
    # load pickled duplicate pairs
    set_of_duplicate_pairs = {
        tuple(line.strip().split(" :: "))
        for item in generated_dup_pairs
        for line in item
        if line.strip().split(" :: ")[0] != line.strip().split(" :: ")[1]
    }
    logger.info(f"length of the set of duplicates:{len(set_of_duplicate_pairs)}")

    # generate a graph using id's as nodes and a pair of ids as an edge
    nk.setNumberOfThreads(NUM_WORKERS)
    G, mapper = construct_graph(set_of_duplicate_pairs)
    components, n_components = find_connected_components(G)
    logger.info(f"number of connected components:{n_components}")

    reversed_mapper = {value: key for key, value in mapper.items()}

    duplicates = defaultdict(set)
    n_duplicate_docs = 0
    for component in components:
        for j in range(1, len(component)):
            doc = reversed_mapper[component[j]]
            file_name, line_idx = doc.split("@")
            duplicates[file_name].add(int(line_idx))
            n_duplicate_docs += 1

    logger.info(f"number of duplicate documents that will be removed:{n_duplicate_docs}")

    return duplicates
