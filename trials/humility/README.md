# trials/humility/

Adversarial trials whose queries are **unanswerable by construction**; the only
correct behavior is calibrated abstention. Scored by the abstention-aware table
(§3.0) and bounded by each layer's humility failure ceiling (§5).

**The fairness rule (§6).** A humility trial must pose the **same task** through
the **same generic interface** (`trials/adapters/INTERFACE.md`) as its paired
ascension trial — no capability hints, no special-casing — differing only in
that its queries have no correct non-abstaining answer.

**Every humility trial ships an `IMPOSSIBILITY.md`** giving a *structural*
argument (not an empirical observation) for why no correct non-abstaining answer
can exist. Without that argument the ceiling would be arbitrary; with it the
ceiling is principled.

Empty at Phase 0 — populated alongside ascension trials.
