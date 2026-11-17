## Explanation

**Purpose.** `CENV_MOD` holds the option to move the envelope's fitting point: `LSENV0` and `SENV0`, $`\log_{10}(m_\mathrm{fit}/M_\star)`$. It replaces `COMMON/CENV/` (MHP via Claude, 10/14/26).

**Who sets them, who reads them.** The [main program](main.f.md#file-level) copies them from the run's settings for each run (`LSENV0A`, `SENV0A`); [`STARIN`](starin.f.md#starin) reads them, makes `SENV0` negative and at most $`-10^{-12}`$ ($`\tau = 2/3`$), and moves the fitting point there.

**Changed since `rp_1`.** New file: `COMMON/CENV/` as a module.
