## Explanation

**Purpose.** `TRIDI_MOD` holds a tridiagonal system $a_i u_{i-1} + b_i u_i + c_i u_{i+1} = d_i$ and its solution, shared between the routines that set up the implicit steps of rotational mixing and the routines that solve them. Shared by 6 routines. It replaces `COMMON/TRIDI/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.**
- `A`, `B`, `C`, `D` (`JSON` each): the sub-diagonal, diagonal, super-diagonal and right-hand side. Set by [[dcoeft.f#DCOEFT|`DCOEFT`]] (angular-momentum transport, solved by [[tridia.f#TRIDIA|`TRIDIA`]]) and [[ccoeft.f#CCOEFT|`CCOEFT`]] (composition transport, solved by [[ctridi.f#CTRIDI|`CTRIDI`]]), and by [[getqua.f#GETQUA|`GETQUA`]] (the quadrupole moment, solved in place).
- `U(JSON)`: the solution, set by `TRIDIA`, `CTRIDI` and `GETQUA`; read by `TRIDIA` (which turns it into the change of angular momentum), [[mixcom.f#MIXCOM|`MIXCOM`]] and `GETQUA` (`QUAD` in `QUADRU_MOD`).
- `GAMA(JSON)`: the Thomas algorithm's work array, set and read by the solvers; `DCOEFT` also uses it as work space while setting up.

**Design.** A blanket `USE TRIDI_MOD` in each routine. The one-letter names `A`, `B`, `C`, `D`, `U` are global in every file that uses the module, so a local of the same name added to one of them later would silently be the module's: the hazard [[runloop_mod.f#RUNLOOP_MOD|`RUNLOOP_MOD`]]'s header describes (KNOWN_ISSUES.md issue 22).

**Changed since `rp_1`.** New file: `COMMON/TRIDI/` as a module.
