## Explanation

**Purpose.** `MASSCHG2_MOD` holds the quantities of the (experimental) thermal response of the convective envelope to accretion, shared by [[massloss.f#MASSLOSS|`MASSLOSS`]], [[mdot.f#MDOT|`MDOT`]] and [[coefft.f#COEFFT|`COEFFT`]]. It replaces `COMMON/MASSCHG2/` (MHP via Claude, 10/14/26). All members are `REAL*8`.

**What its variables hold, who sets them, who reads them.**
- `SCEN`: the convective envelope's mass-averaged $(\mathcal R/\mu)(\tfrac32\ln T - \ln\rho)$ (an entropy per gram), computed by `MASSLOSS` and then set to 0 in both branches that follow; read by `MDOT`.
- `SACC`: the same quantity at the base of the envelope, set by `MASSLOSS`; read nowhere.
- `DLOGT`, `DLOGP`: the changes of $\log T$ and $\log P$ that `MDOT` derives from `SCEN` and applies to the envelope; read also by `COEFFT`, which adds them in its entropy terms with accretion. Since `SCEN` = 0, they are zero in practice (MDOT's and MASSLOSS's notes ask whether this code is kept for later work).
- `SMASS0`: the total mass (solar units) after the step's mass change, set by `MDOT`; read nowhere.

**Design.** A blanket `USE MASSCHG2_MOD`. At `rp_1`, MASSLOSS declared `DLOGT` and `DLOGP` in the opposite order from MDOT and COEFFT, so under COMMON's storage association each name there held the other's value; MASSLOSS uses neither, so this had no effect, and the module removes the hazard.

**Changed since `rp_1`.** New file: `COMMON/MASSCHG2/` as a module.

## Questions for the experts

1. **Unused members.** `SACC` and `SMASS0` are set and read nowhere. Can they go?
