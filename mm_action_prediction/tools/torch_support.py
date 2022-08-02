"""Additional utilities for torch tensors.

Author: Satwik Kottur
"""


from __future__ import absolute_import, division, print_function, unicode_literals

import torch


def flatten(tensor, batch_size, num_rounds):
    """Flattens a tensor based on batch_size(B) and num_rounds(N).

    Args:
      tensor: Size [B, N, D1, D2, D3, ...]
      batch_size: B
      num_rounds = N

    Returns:
      flat_tensor: Size [B * N, D1, D2, ...]
    """
    old_size = tensor.shape
    assert old_size[0] == batch_size, f"Expected dim 0 as {batch_size}"
    assert old_size[1] == num_rounds, f"Expected dim 1 as {num_rounds}"
    new_size = (-1,) + old_size[2:]
    return tensor.reshape(new_size)


def unflatten(tensor, batch_size, num_rounds):
    """Unflatten a tensor based on batch_size(B) and num_rounds(N).

    Args:
      tensor: Size [B*N, D1, D2, D3, ...]
      batch_size: B
      num_rounds = N

    Returns:
      unflat_tensor: Size [B, N, D1, D2, ...]
    """
    old_size = tensor.shape
    expected_first_dim = batch_size * num_rounds
    assert (
        old_size[0] == expected_first_dim
    ), f"Expected dim 0 as {expected_first_dim}"

    new_size = (batch_size, num_rounds) + old_size[1:]
    return tensor.reshape(new_size)


def gather_states(all_states, indices):
    """Gathers states from relevant indices given all states.

    Args:
        all_states: States for all indices (N x T x d)
        indices: Indices to extract states from (N)

    Returns:
        gathered_states: States gathers at given indices (N x d)
    """
    return torch.cat([ss[ii].unsqueeze(0) for ss, ii in zip(all_states, indices)])
