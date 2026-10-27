## Explanation

**Purpose.** `AEOS06_MOD` holds the OPAL 2006 equation-of-state tables and their grids, shared by 5 routines. It replaces `COMMON/AEOS06/` (MHP via Claude, 10/20/26), whose member `M` is now named `MIDX`; the table dimensions (`MX` = 5, `MV` = 10, `NR` = 169, `NT` = 197) are private to the module, since each user declares its own.

**What its variables hold, who sets them, who reads them.**
- `XZ(MX,MV,NT,NR)`: the tables, for each of the five $X$ values, ten quantities on the $(T_6, \rho)$ grid; read in by [[readcoeos06.f#READCOEOS06|`READCOEOS06`]], read by [[esac06.f#ESAC06|`ESAC06`]] and [[rhoofp06.f#RHOOFP06|`RHOOFP06`]].
- `T6LIST(NR,NT)`, `RHO(NR)`, `T6A(NT)`: the grids, from `READCOEOS06`; read by `ESAC06`, `RHOOFP06`, [[eqbound06.f#EQBOUND06|`EQBOUND06`]] and [[t6rinteos06.f#T6RINTEOS06|`T6RINTEOS06`]].
- `DFSX(MX)`, `DFS(NT)`, `DFSR(NR)`: inverse grid spacings in $X$, $T_6$ and $\rho$, set by `READCOEOS06`; read by `ESAC06` and `T6RINTEOS06`.
- `ESK(NT,NR)`, `ESK2(NT,NR)`: values interpolated in $X$, set by `ESAC06` and read by it and `T6RINTEOS06`.
- `MIDX`: read from the table file by `READCOEOS06`; `MF`: the $X$ index, set in `ESAC06`.
- `XA(MX)`: the five $X$ values, 0, 0.2, 0.4, 0.6, 0.8 (a `DATA` statement moved from `ESAC06`); read by `ESAC06` and `RHOOFP06`.

**Design.** A blanket `USE AEOS06_MOD`; the table alone holds $5 \times 10 \times 197 \times 169$ values (about 13 MB).

**Changed since `rp_1`.** New file: `COMMON/AEOS06/` as a module, `M` renamed `MIDX`, `XA`'s values moved from ESAC06.
