# Chronicle grammar

The **chronicle** corpus is a log of a small, self-consistent world of
**entities** changing over logical time. It is the primary substrate for Recall,
Range, Aggregation, and Association capabilities (Layers 1–4).

Each line of a frozen chronicle file is one **event payload** (canonical JSON,
§2.4), with no `t` field — the ingestion order (0-based line index) *is* the
logical time `t` the engine will assign (BOUNDARY.md §1.3). Payloads use only
integers and strings.

## Event kinds

| kind     | shape                                                        | meaning                              |
|----------|-------------------------------------------------------------|--------------------------------------|
| `spawn`  | `{"kind":"spawn","entity":<int>,"class":<str>}`             | a new entity appears                 |
| `attr`   | `{"kind":"attr","entity":<int>,"key":<str>,"val":<int\|str>}`| set/overwrite an attribute value     |
| `link`   | `{"kind":"link","src":<int>,"dst":<int>,"rel":<str>}`       | relate two live entities             |
| `move`   | `{"kind":"move","entity":<int>,"loc":<str>}`                | relocate an entity                   |
| `retire` | `{"kind":"retire","entity":<int>}`                          | an entity leaves the world           |

## Vocabularies (fixed)

- **class**: `node agent record token vault relay ledger beacon`
- **attr key**: `status level owner tag size region tier mode`
- **attr string value**: `alpha beta gamma delta idle active sealed open north south east west`
- **attr int value**: uniform in `[0, 999]`
- **rel**: `owns links parent mirrors feeds guards`
- **loc**: `hall_a hall_b vault_1 vault_2 gate yard depths spire`

## Generation rules (deterministic)

1. Entity ids are assigned sequentially starting at `1`. A `live` list tracks
   currently-live entity ids in insertion order.
2. Each step draws an action bucket from `prng.below(100)`:
   - `[0,20)` → `spawn`, `[20,60)` → `attr`, `[60,75)` → `link`,
     `[75,90)` → `move`, `[90,100)` → `retire`.
3. **Feasibility repair** (keeps every reference valid and `live` non-empty):
   - If `live` is empty, the action becomes `spawn`.
   - `link` needs ≥2 live entities; if fewer, it becomes `attr`.
   - `retire` is only taken when `live > 1` (the world never empties after its
     first spawn); otherwise it becomes `attr`.
4. `spawn`: new id, `class` chosen uniformly; appended to `live`.
5. `attr`: entity chosen uniformly from `live`; `key` uniform; `val` is an int
   in `[0,999]` with probability 1/2, else a string chosen uniformly.
6. `link`: two **distinct** live entities chosen uniformly (`src`, `dst`);
   `rel` uniform.
7. `move`: entity chosen uniformly from `live`; `loc` uniform.
8. `retire`: entity chosen uniformly from `live`, removed by swap-pop.

All randomness comes from `corpora/prng.py` seeded by the explicit seed. Two
runs at the same `(seed, n)` produce byte-identical output (byte-match law,
§8.3).

## Frozen output

- seed `1001`, scale `n = 50000` → `chronicle.s1001.n50000.jsonl`.
- Regenerate & verify: `python3 -m corpora.chronicle.generator --check`.
- Rewrite the frozen file (only when legitimately (re)forging): `... --write`.
