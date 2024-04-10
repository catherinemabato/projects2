"""Test is_separable."""

import numpy as np
import pytest

from toqito.channels import partial_trace
from toqito.matrix_props import is_density
from toqito.rand import random_density_matrix
from toqito.state_props.is_separable import is_separable
from toqito.states import basis, bell, tile


@pytest.mark.parametrize(
    "test_input",
    [
        # Ensure separability of non-positive semidefinite matrix is invalid
        (np.array([[-1, -1], [-1, -1]])),
    ],
)
def test_werner_state_invalid(test_input):
    """Test function works as expected for an invalid input."""
    with pytest.raises(ValueError):
        is_separable(test_input)


p_var, a_var, b_var = 0.4, 0.8, 0.64
rho_chen = np.array(
    [
        [p_var * a_var**2, 0, 0, p_var * a_var * b_var],
        [0, (1 - p_var) * a_var**2, (1 - p_var) * a_var * b_var, 0],
        [0, (1 - p_var) * a_var * b_var, (1 - p_var) * a_var**2, 0],
        [p_var * a_var * b_var, 0, 0, p_var * a_var**2],
    ]
)


@pytest.mark.parametrize(
    "test_input",
    [
        # Determined to be entangled via the PPT criterion.
        (bell(0) * bell(0).conj().T),
        # Determined to be entangled by using Theorem 1 and Remark 1 of :cite:`Chen_2003_Matrix`.
        (rho_chen),
    ],
)
def test_not_is_separable(test_input):
    """Check an expected non seperable test input is identified correctly."""
    assert not is_separable(test_input)


e_0, e_1, e_2 = basis(3, 0), basis(3, 1), basis(3, 2)
psi = 1 / np.sqrt(3) * e_0 + 1 / np.sqrt(3) * e_1 + 1 / np.sqrt(3) * e_2

e_0, e_1 = basis(2, 0), basis(2, 1)
phi = np.kron((1 / np.sqrt(2) * e_0 + 1 / np.sqrt(2) * e_1), psi)


@pytest.mark.parametrize(
    "test_input",
    [
        # Every positive semidefinite matrix is separable when one of the local dimensions is 1.
        (np.identity(2)),
        # Determined to be separable via sufficiency of the PPT criterion in small dimensions.
        (phi * phi.conj().T),
    ],
)
def test_is_separable(test_input):
    """Check an expected seperable test input is identified correctly."""
    # without an input for the dimension
    assert is_separable(test_input)
    # wth int dim
    assert is_separable(test_input, 2)


def test_ppt_low_rank():
    """Determined to be separable via the operational criterion for low-rank operators."""
    m = 6
    n = m
    rho = random_density_matrix(m)
    u, s, v_h = np.linalg.svd(rho)
    rho_cut = u[:, : m - 1] @ np.diag(s[: m - 1]) @ v_h[: m - 1]
    rho_cut = rho_cut / np.trace(rho_cut)
    pt_state_alice = partial_trace(rho_cut, [1], [3, 2])

    assert is_density(rho_cut)
    assert is_density(np.array(pt_state_alice))
    assert np.linalg.matrix_rank(rho_cut) + np.linalg.matrix_rank(pt_state_alice) - 2 * m * n - m - n + 2 <= 1e-1
    # TODO
    # np.testing.assert_equal(is_separable(rho), True)


def test_entangled_realignment_criterion():
    """Determined to be entangled via the realignment criterion."""
    # Construct bound entangled state:
    # :math:`\rho = \frac{1}{4} \mathbb{I}_3 \otimes \mathbb{I}_3 - \sum_{i=0}^4 | \psi_i \rangle \langle \psi_i |`
    rho = np.identity(9)
    for i in range(5):
        rho = rho - tile(i) * tile(i).conj().T
    rho = rho / 4
    assert is_density(rho)
    assert not is_separable(rho)
