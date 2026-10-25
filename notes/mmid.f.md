## Explanation

**Purpose.** The modified midpoint method of Numerical Recipes ("this SR from Numerical Recipes, p.562"): it advances three variables $y$ from $x$ to $x + H$ in $n$ substeps. It is the inner step of the Bulirsch–Stoer integrator [[bsstep.f#BSSTEP|BSSTEP]], which [[envint.f#ENVINT|ENVINT]] uses to integrate the envelope.

**How it fits.**
- **Who calls it:** only [[bsstep.f#BSSTEP|BSSTEP]], with a sequence of $n$ (`NSEQ`).
- **What it calls:** the derivative routine passed in as `DERIV` (an `EXTERNAL` argument; the site cannot resolve it statically). All the arguments after `DERIV` (`B`, `FPL`, `FTL`, `GL`, `LATMO`, …, `KSAHA`) are only passed through to it.
- **Output:** `YOUT`, the values at $x+H$.

**The method.** With $h = H/n$, $z_0 = y(x)$, $z_1 = z_0 + h\,y'(x)$,
$$z_{m+1} = z_{m-1} + 2h\,f(x + m h, z_m),\quad m = 1,\dots,n-1,\qquad y(x+H) \approx \tfrac12\left[z_n + z_{n-1} + h\,f(x+H, z_n)\right].$$
`YOUT` holds the derivatives in between, to save an array.

**Design.** The size is fixed at three variables (`Y(3)`), whatever `NVAR` is.
