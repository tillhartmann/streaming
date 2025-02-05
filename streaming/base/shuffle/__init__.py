# Copyright 2023 MosaicML Streaming authors
# SPDX-License-Identifier: Apache-2.0

"""Shuffle epochs of samples from different shards across worker partitions."""

from typing import Any
import numpy as np
# from numpy.typing import NDArray

from streaming.base.shuffle.py1s import get_shuffle_py1s
from streaming.base.shuffle.py2s import get_shuffle_py2s

algos = {
    'py1s': get_shuffle_py1s,
    'py2s': get_shuffle_py2s,
}


def get_shuffle(algo: str, shard_sizes: Any, num_canonical_nodes: int, seed: int,
                epoch: int) -> Any:
    """Get the shuffled global ordering of samples for an epoch.

    The assignment of shards to nodes is fixed across epochs, but each grouping of shards is
    processed concurrently in a different order by each node's workers each epoch.

    Args:
        algo (str): Which shuffling algorithm to use.
        shard_sizes (Any): Number of samples contained in each shard, in order.
        num_canonical_nodes (int): Number of canonical nodes.
        seed (int): Base random seed, which is held constant over an entire training run.
        epoch (int): Current epoch, which is added to the seed to get a different deterministic
            shuffle each epoch.

    Returns:
        Any: 1:1 mapping of sample ID to shuffled sample ID.
    """
    get = algos[algo]
    return get(shard_sizes, num_canonical_nodes, seed, epoch)
