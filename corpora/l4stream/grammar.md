# l4stream grammar — the Layer-4 consolidation stream

The **l4stream** corpus is the chronicle world with a different *shape of
history*: the same vocabularies, the same event kinds, but a **bounded, persistent
population whose attributes are superseded over and over**. It exists because
`trials/ascension/l4/ATTAINABILITY.md` measured that the frozen chronicle family
cannot admit the ratified Layer-4 gate under **any** consolidation policy — the
chronicle grammar asserts each `(entity, key)` pair **1.197 times on average**, so
there is nearly nothing to consolidate and 35% of any exact history schema goes on
*identifying* pairs rather than on their values.

Each line is one **event payload** (canonical JSON, §2.4), with no `t` field — the
0-based line index is the logical time `t` the engine assigns (§1.3). Payloads use
only integers and strings. There is **no `importance` field**: Layer 4 weights
every coverage target `1` (§3.2's default), so this stream carries no weight
profile and none of the Layer-3 pressure machinery.

## Event kinds

| kind    | shape                                                          | facet |
|---------|----------------------------------------------------------------|-------|
| `spawn` | `{"kind":"spawn","entity":<int>,"class":<str>}`                 | assertion `(entity, "class", class)` |
| `attr`  | `{"kind":"attr","entity":<int>,"key":<str>,"val":<int\|str>}`   | assertion `(entity, key, val)` |
| `move`  | `{"kind":"move","entity":<int>,"loc":<str>}`                    | assertion `(entity, "loc", loc)` |
| `link`  | `{"kind":"link","src":<int>,"dst":<int>,"rel":<str>}`           | assertion `(src, rel, dst)` |
| `note`  | `{"kind":"note","entity":<int>,"text_id":<int>}`                | **irreducible** |

There is **no `retire`**: the world is persistent. That is a declared design
choice, not an oversight — a churning population spends its schema budget on
identity, and identity is exactly what chronicle's arithmetic showed cannot be
afforded at a quarter of the raw footprint.

`link` is an assertion on `(src, rel)` whose value is the target. That is
Graphiti's bitemporal edge (GAPMAP **S3**, `3bb2d0b` `edges.py:263–280`) with the
two LLM calls it needs replaced by integer interval arithmetic: the current value
of `(src, rel)` is the currently-valid target, its history is the edge's
validity intervals, and its participation set is the distinct values of the chain.

## Vocabularies (fixed — chronicle's, unchanged)

Imported directly from `corpora/chronicle/generator.py`, so this is the same
language, not a dialect:

- **class**: `node agent record token vault relay ledger beacon`
- **attr key**: `status level owner tag size region tier mode`
- **attr string value**: `alpha beta gamma delta idle active sealed open north south east west`
- **attr int value**: uniform in `[0, 999]`
- **rel**: `owns links parent mirrors feeds guards`
- **loc**: `hall_a hall_b vault_1 vault_2 gate yard depths spire`

The per-entity key space is therefore `8` attr keys `+ {class, loc} + 6` rels =
**16 keys**, and the whole pair universe is `ENTITIES × 16 = 3200` — bounded by
the grammar, which chronicle's is not (its entity ids are discovered from the
data and grow without limit).

## Generation rules (deterministic)

1. **The spawn prelude.** Events `0 … ENTITIES-1` spawn entities `1 … ENTITIES`
   in order, each with a uniform `class`. Nothing else creates an entity, and
   nothing ever destroys one.
2. Each remaining step draws a bucket from `prng.below(100)`:
   `[0,74)` → `attr`, `[74,84)` → `move`, `[84,94)` → `link`, `[94,100)` → `note`.
3. `attr`: entity uniform in `[1, ENTITIES]`; `key` uniform; `val` is an int in
   `[0,999]` with probability 1/2, else a string chosen uniformly.
4. `move`: entity uniform; `loc` uniform.
5. `link`: `src` uniform; `dst` uniform over the other `ENTITIES-1` entities;
   `rel` uniform.
6. `note`: entity uniform; `text_id` is a counter starting at `1`, so **every
   `text_id` occurs exactly once in the stream**.

No feasibility repair is needed: the population is fixed before the first
assertion, so every reference is valid by construction.

## The three declared properties

These are what the Layer-4 gate rests on, and each is asserted by
`trials/ops/l4/t_l4stream.py` against the `DECLARED_*` constants in
`generator.py`. The byte-match law (§8.3) freezes the bytes; these freeze what
the bytes are *for*.

1. **Bounded population.** Exactly `ENTITIES = 200` entities, all spawned in the
   first 200 events, none retired.

2. **Declared assertion redundancy.** `18 788` assertions over `2 951` pairs —
   a mean supersession chain of **6.367**, against chronicle's 1.197 and murk's
   1.305. Chain lengths run from 1 to 19. Only **157‰** of assertions are their
   pair's latest (chronicle: 836‰), so a current-value table with no history
   answers 157‰ of the assertion facet here and 836‰ there — the gap that makes
   the as-of battery a test of history rather than a second copy of Q1.

3. **A declared irreducible tier.** `1 212` `note` events, each carrying a
   globally unique `text_id`. Notes are grammar-redundant with nothing: no schema
   regenerates one. They exist so reconstruction fidelity is bounded **below
   1000 by construction** — the best state at footprint 250‰ reconstructs
   `19 642 / 20 000` events for `F = 984‰` — and the `F ≥ 900` gate therefore
   measures honest lossy compression rather than a corpus with nothing to lose.

## What this corpus does *not* do

It is **not** a pressure stream. Layer 3's 10×-budget streams (`l3stream`,
`l3streamb`) stay exactly what they are and keep gating Layer 3; the Form-B
eviction debt recorded in `core/layers/README-l3.md §0.4` comes due against
`l3streamb`, not here. `l4stream` isolates one variable — grammar redundancy —
so the footprint gate measures compression and not eviction.

## Frozen output

- seed `6006`, scale `n = 20000` → `l4stream.s6006.n20000.jsonl`.
- Verify: `python3 -m corpora.l4stream.generator --check`.
- Rewrite (only when legitimately (re)forging): `... --write`.
