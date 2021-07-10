#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2021 Stéphane Caron <stephane.caron@normalesup.org>
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

"""Solver interface for MOSEK"""

from typing import Optional

import cvxopt.msk
import mosek

from numpy import ndarray

from .cvxopt_ import cvxopt_solve_qp
from .typing import CvxoptReadyMatrix


def mosek_solve_qp(
    P: CvxoptReadyMatrix,
    q: CvxoptReadyMatrix,
    G: CvxoptReadyMatrix,
    h: CvxoptReadyMatrix,
    A: Optional[CvxoptReadyMatrix] = None,
    b: Optional[CvxoptReadyMatrix] = None,
    initvals: Optional[CvxoptReadyMatrix] = None,
    verbose: bool = False,
) -> Optional[ndarray]:
    """
    Solve a Quadratic Program defined as:

    .. math::

        \\begin{split}\\begin{array}{ll}
        \\mbox{minimize} &
            \\frac{1}{2} x^T P x + q^T x \\\\
        \\mbox{subject to}
            & G x \\leq h                \\\\
            & A x = h                    \\\\
            & lb \\leq x \\leq ub
        \\end{array}\\end{split}

    using the `MOSEK interface from CVXOPT
    <https://cvxopt.org/userguide/coneprog.html#optional-solvers>`_.

    Parameters
    ----------
    P : numpy.ndarray, cvxopt.matrix or cvxopt.spmatrix
        Symmetric quadratic-cost matrix.
    q : numpy.ndarray, cvxopt.matrix or cvxopt.spmatrix
        Quadratic-cost vector.
    G : numpy.ndarray, cvxopt.matrix or cvxopt.spmatrix
        Linear inequality constraint matrix.
    h : numpy.ndarray, cvxopt.matrix or cvxopt.spmatrix
        Linear inequality constraint vector.
    A : numpy.ndarray, cvxopt.matrix or cvxopt.spmatrix
        Linear equality constraint matrix.
    b : numpy.ndarray, cvxopt.matrix or cvxopt.spmatrix
        Linear equality constraint vector.
    initvals : numpy.ndarray, optional
        Warm-start guess vector.
    verbose : bool, optional
        Set to `True` to print out extra information.

    Returns
    -------
    x : numpy.ndarray
        Solution to the QP, if found, otherwise ``None``.
    """
    cvxopt.solvers.options["mosek"] = {mosek.iparam.log: 1 if verbose else 0}
    return cvxopt_solve_qp(P, q, G, h, A, b, "mosek", initvals)
