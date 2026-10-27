## Explanation

**Purpose.** `ATMSTRUCT_MOD` holds the structure of the atmosphere, point by point, for the stitched output of the whole star. It replaces `COMMON/ATMSTRUCT/` (MHP via Claude, 10/14/26); `JSON` comes from `DIMENSIONS_MOD`.

**What its variables hold, who sets them, who reads them.** All are set by [[envint.f#ENVINT|`ENVINT`]] during the atmosphere integration, and read only by [[stitch.f#STITCH|`STITCH`]], which joins them to the envelope and the interior: `NUMATM`, the number of points; at each point $\log P$, $\log T$, $\log\rho$, $\log r$ (`ATMOP`, `ATMOT`, `ATMOD`, `ATMOR`), the three gradients `ADELS(3,·)`, `ABETAS` ($\beta$), `AGAM1` ($\Gamma_1$), `AQDT`, the ionization fractions `AFXIONS(3,·)`, the opacity `ATMOO` and $c_P$ `ATMOCP`.

**Changed since `rp_1`.** New file: `COMMON/ATMSTRUCT/` as a module.
