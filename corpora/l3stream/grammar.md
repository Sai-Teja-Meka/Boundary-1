# L3 pressure-stream grammar

The **l3stream** corpus is the substrate for the Layer-3 (Forgetting) ascension
and humility trials. It is a stream of length `10 × BUDGET` (`BUDGET = 1000`,
`N = 10000`) of memory **items**, each carrying an integer **importance** weight.

Each line is one event payload (canonical JSON, §2.4); the 0-based line index is
the logical time `t`. Payloads use only integers and strings.

## Event shape

| kind   | shape                                                                 |
|--------|-----------------------------------------------------------------------|
| `item` | `{"kind":"item","id":<int>,"key":<str>,"val":<int>,"importance":<int>}` |

- **id**: sequential from `1`.
- **key**: one of `alpha beta gamma delta epsilon zeta eta theta`.
- **val**: uniform in `[0, 999]`.
- **importance**: an integer weight, **non-decreasing in position** (§ below).

## The binding precondition: importance uniformly-to-late

Importance weights are **non-decreasing in `t`** — the profile ranges from uniform
to late-loaded, and is **never front-loaded**. This is a *binding precondition*
of the Layer-3 humility argument (BOUNDARY.md §5 L3;
`trials/humility/l3/IMPOSSIBILITY.md`):

- The budget law (§4.1) forces a capped fill-then-refuse engine to keep the
  **earliest** `BUDGET` items and refuse the rest.
- Because importance never decreases, those earliest items carry the **least**
  importance mass. At the frozen seed the first `BUDGET` items hold ≈ 10‰ of the
  total mass — far below the 300‰ humility ceiling.
- So the capped engine cannot exceed the ceiling **by luck**; only genuine
  importance-weighted eviction (the real Layer-3 capability) can clear the
  ascension gate.

The generator enforces non-decreasing importance; `trials/ops/t_l3stream.py`
checks it, and checks that the first `BUDGET` items hold ≤ 300‰ of total mass.

## Frozen output

- seed `4004`, scale `n = 10000`, budget `1000` → `l3stream.s4004.n10000.jsonl`.
- Verify: `python3 -m corpora.l3stream.generator --check`.
- Rewrite (only when legitimately (re)forging): `... --write`.
