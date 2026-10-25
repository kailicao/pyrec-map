## Explanation

**Purpose.** `KURUCZ2` is [[kurucz.f#KURUCZ|`KURUCZ`]] for the second Kurucz table (the second metallicity, used when `L2Z` is set).

**How it fits.** Called only by [[getopac.f#GETOPAC|`GETOPAC`]], right after `KURUCZ`, which then interpolates $\log\kappa$ and its derivatives linearly in $Z$ between `ZKUR1` and `ZKUR2`. Its COMMON blocks are the second table's: `GKRZ2`, `KRZ2` (filled by [[setkrz.f#SETKRZ|`SETKRZ`]]), `INTPL22` (by [[ykoeff.f#YKOEFF|`YKOEFF`]]), `KIPM2`. Calls `FINDEX` and `INTPOL`. Alternate return as in `KURUCZ`.

**The method.** That of `KURUCZ`, except that it does not test the corner $\log\rho \le -3$, $\log T \le 4.1$. This makes no difference now: `GETOPAC` calls `KURUCZ2` only after `KURUCZ` has passed that test (a failed test in `KURUCZ` jumps past the call).

## Questions for the experts

1. **Duplicated code.** A single routine with the table passed as arguments would keep the two from drifting apart (they differ already in the corner test, harmless only because of the order of the calls in `GETOPAC`).

### KURUCZ2

`KURUCZ` on the second-$Z$ table, without the corner test (made by `KURUCZ` before it).
