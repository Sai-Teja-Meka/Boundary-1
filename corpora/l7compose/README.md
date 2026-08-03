# corpora/l7compose — the Layer-7 generation artifact

`[L6] [ASCEND]`, Layer-7 Stage A, 2026-08-03. Seed **10010**, 12 000 events,
2 200 queries, one canonical JSON object. Admitted to `registry.GENERATED`, so
`§8.3`'s byte-match law covers it.

**NO LAYER-7 GATE BINDS ON IT.** `trials/ascension/l7/ATTAINABILITY.md` computes
the arithmetic and `trials/ascension/l7/RULING-R8-DRAFT.md` asks a human to bind
it; appending a ruling is what freezes, and the session that built this artifact
does not append. `trials/ascension/l7/t_attainability.py::trial_no_layer_7_gate_binds_on_anything`
asserts the same absence from the other side.

## Why it exists — the fifth substrate kill

`§5 L7`'s `novelty = 1000` is *"provably never-stored"*, so a gate citing it can
only bind where some query's correct answer is **not in the stream**. Across
every artifact this project has frozen plus `§8.8`'s one `REAL` entry — **85 954
answerable queries**, drawn from the frozen batteries those artifacts already
carry — **not one answer is absent from its own stream**. `§8.7`'s *dirt is
always paired with the answer key* is the cause, and it is a virtue of those
artifacts rather than a defect: an answer key that names the `t`s it touches
cannot force a composition.

So on every existing artifact the generation-required class is **empty**,
`tagging`'s denominator is empty, and a gate citing it measures nothing. That is
the **fifth substrate kill** — after `l3stream` (`R1`), the chronicle family
(`R4`) and `l6battery` (`R7`) — and the first to fall on the whole stock rather
than on one artifact. **Nothing is demoted**: nothing here was ever a Layer-7
candidate, so what is recorded is a refusal to bind, in `R4` clause 1's form.

## The grammar

A **compound** is formed from exactly two components by two `part` assertions; a
component carries a `hue` and a `mass`. The declared rule `COMPOSITION_FORM`
determines the compound's `profile` item:

```
profile(c) = {"kind":"profile", "entity":c,
              "grade": GRADES[(HUES.index(h0) + HUES.index(h1)) % len(GRADES)],
              "hue":   h0,
              "mass":  m0 + m1}
```

A compound component's `(hue, mass)` is **its own profile's**, which closes the
rule under composition and gives the self-pollution ladder its rungs. Integer
arithmetic only; no float appears anywhere (`§2.2`).

`part` and `profile` are **outside** the frozen Layer-4 facet map, deliberately:
to every engine below Layer 7 a `profile` event is an irreducible episode and not
an assertion, which is why the composition reading had to be a *second* declared
reading — in the shape `ASSERTION_FORMS` (L4), `INTENTION_FORM` (L5) and
`SET_ONCE_KEYS` (L6) already have.

## The two theorems

**THEOREM 1 — the class is not readable from the query.** 100 **mirror pairs**
`(e0, e1 = e0 + 1)` whose two members are **twins**: one material is drawn per
slot and instantiated twice, so their event blocks are equal as sequences once
the entity ids are blanked and they compose to the *same item but for its
`entity` field*. **The value is never the signal.** A **balanced coin** decides
which member's profile the stream carries. Blank the entity id and the two cues
are the same object, so any policy whose lineage decision is a function of the
query alone mislabels **exactly one member of every pair — 100 errors** — and the
two handles that leaves, the raw id and the emission order (the same handle
here), are closed by the coin's balance. Exhibited against a bench of six
labellers, every one measuring 100. Under the coin's complement the identical
query set is produced with the classes exchanged.

**THEOREM 2 — novelty.** For every generation-required compound the composed
item's canonical bytes (`§2.4`) appear **nowhere** in the frozen stream, asserted
by exhaustive comparison against all 12 000 payloads and structurally besides.
`R7` clause 3(b)'s pattern: the guarantee is on the **artifact**, so it holds
against an arbitrary engine.

This is a **different** theorem from `corpora/l6batteryb`'s. There the resolving
signal was withheld from the *stream*, so no reader could be right. Nothing is
withheld from a correct **composer** here: what is withheld is the *item*, from
the *retrieval channel*.

## The classes

| class | n | query | answerable | declared |
|---|---:|---|---|---|
| **KG1** | 100 | `generate` profile, region **G** member | yes | **G**, depth 1 |
| **KO** | 100 | `generate` profile, region **O** member | yes | **O** |
| **KG2** | 30 | `generate` profile, ladder depth 2 | yes | **G**, depth 2 |
| **KG3** | 30 | `generate` profile, ladder depth 3 | yes | **G**, depth 3 |
| **KR** | 1 740 | `current(entity,key)` | yes | **O** |
| **KU1** | 100 | `generate` profile, **incomposable** compound | **no** | U |
| **KU2** | 100 | `current(entity,key)`, never asserted | **no** | U |

`A = 2 000` answerable, `N = 2 200` total, `|G| = 160`, `g = 160/2000 = 80‰` —
above the `1/18 = 55.5‰` at which a blanket hedger survives `F ≥ 950`.

`KU1` is a class no earlier artifact here has had: a **generation-shaped
unanswerable probe**. One of its components' `mass` is never asserted, so the
rule does not determine the item and abstention is the only correct behaviour;
composing anything there is a fabrication, priced 0 by `§3.0`.

## The self-pollution ladder

30 chains, each rooted in one of the region's own **G** compounds: a depth-2
compound is formed from that root and a fresh component, a depth-3 from the
depth-2 and another, and every one of those profiles is withheld. Declared
lineage: `{depth 0: 100, depth 1: 100, depth 2: 30, depth 3: 30}`.

**Lineage depth is decidable from the frozen bytes** — a compound whose profile
is in the store is depth 0, otherwise one more than the greatest depth among its
compound components — and the recomputation is required to equal the declared
table. So `§6`'s mandatory self-pollution strain takes its rungs from the
artifact rather than from an engine's account of itself.

A composed profile is an ordinary payload in the same grammar, so **re-ingestion
is the caller's act** and the promotion failure `§5 L7` forbids is reachable by
construction: append the item and the store carries it, retrieval answers it, and
only a lineage record can still say what it is.

## One artifact, one byte-match

Substrate, declared class table and query set are one canonical JSON object, for
`corpora/l6batteryb`'s reason: the guarantees are a **joint** property of the
three, and three separately byte-matched files could be paired across generations
and lose it while every individual check stayed green.

Randomness comes solely from `corpora/prng.py`; output is canonical JSON with a
trailing newline. Same `seed` → byte-identical (`§8.3`).

```
python3 -m corpora.l7compose.generator --check     # byte-match
python3 -m corpora.l7compose.generator --write     # re-freeze
```

Asserted by `trials/ops/l7/t_l7compose.py` (the shape, both readings, both
theorems, the ladder, re-ingestibility) and by
`trials/ascension/l7/t_attainability.py` (the Stage-A arithmetic).
