"""Kernels: small, stateless numerical routines and named constants.

The bottom of the layering; imports nothing from pyrec. Compute kernels are
module-level functions (Numba where hot); classes orchestrate.

Modules
-------
constants : Physical constants (cgs, with sources) and the species indices of HCOMP.
numerics : Splines, tridiagonal and banded solvers, LU, interpolation, quadrature, Fermi integrals.
odeint : OdeRhs and the Bulirsch-Stoer step.
logger : Logger, for the .short file and timings.

Counterpart: new-fortran/kernels.md
"""
