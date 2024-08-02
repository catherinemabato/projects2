"""Check is a matrix is left stochastic."""

import numpy as np

from toqito.matrix_props import is_nonnegative, is_square


def is_left_stochastic(mat: np.ndarray) -> bool:
    r"""Verify matrix is right stochastic.

    A matrix is right stochastic if it is a square matrix with nonegative elements such that the columns sum up to 1
     :cite:WikiStichasticMatrix.

    Examples
    ========
    The elements an identity matrix and a Pauli X matrix are nonnegative and the rows sum up to 1. The same cannot be
    said about a Pauli Z matrix.

    .. math::
     Id = \begin{pmatrix}
               1 & 0 & 0 & 0 & 0\\
               0 & 1 & 0 & 0 & 0\\
               0 & 0 & 1 & 0 & 0\\
               0 & 0 & 0 & 1 & 0\\
               0 & 0 & 0 & 0 & 1\\
          \end{pmatrix}

     >>> import numpy as np
     >>> from toqito.matrix_props import is_left_stochastic
     >>> id_mat = np.eye(5)
     >>> is_left_stochastic(id_mat)
     True

     .. math::
     PauliX = \begin{pmatrix}
               0 & 1 \\
               1 & 0\\
          \end{pmatrix}

     >>> from toqito.matrices import pauli
     >>> from toqito.matrix_props import is_left_stochastic
     >>> x_mat = pauli("X")
     >>> is_left_stochastic(x_mat)
     True

     .. math::
     PauliY = \begin{pmatrix}
               1 & 0 \\
               0 & -1\\
          \end{pmatrix}

     >>> from toqito.matrices import pauli
     >>> from toqito.matrix_props import is_left_stochastic
     >>> z_mat = pauli("Z")
     >>> is_left_stochastic(z_mat)
     False




    References
    ==========
    .. bibliography::
          :filter: docname in docnames

     :param rho: Matrix of interest

    """
    if is_square(mat) and is_nonnegative(mat) and np.all(np.sum(mat, axis=0) == 1.0):
        return True

    return False
