# l5stream grammar — the Layer-5 prospection stream

The **l5stream** corpus is the `l4stream` world plus one new event kind:
**`intend`**, an intention carried as an ordinary ingested payload. It is frozen
by the Layer-5 Stage-A attainability session, before any Layer-5 trial applies a
gate to any engine and before `core/layers/l5_prospection.py` exists
(`BOUNDARY-RULINGS.md R2`'s standing step: *attainability arithmetic → trials →
engine*).

Each line is one **event payload** (canonical JSON, §2.4), with no `t` field. The
0-based line index is the **caller index** `k`. It is **not** the engine's logical
`t`: a fired event consumes a `t` of its own (§1.3), so the engine's `t` for
caller index `k` is `k` plus the number of firings that preceded it. Everything
this corpus declares is stated over caller indices, which is what makes it a
property of the frozen bytes rather than of an engine.

## Why an intention is an event

`§7.1` declares **three** operations — `ingest`, `query`, `snapshot` — and `§1.1`
says events are the only fuel: *"Configuration, queries, and side-band signals are
not fuel."* `§5 L5`'s `intend(condition → event)` therefore cannot be a fourth
entry point into the engine. It arrives as an **ingested payload** whose reading
is declared here, exactly as `trials/_l4tasks.facet` is a declared reading of the
chronicle-family grammars, and `HANDLE_FIELDS` is at Layer 3. The engine's
`intend` *capability* is what it does with such a payload; the payload is fuel
like any other.

## Event kinds

| kind     | shape                                                              | Layer-4 facet |
|----------|--------------------------------------------------------------------|---------------|
| `spawn`  | `{"kind":"spawn","entity":<int>,"class":<str>}`                     | assertion `(entity, "class", class)` |
| `attr`   | `{"kind":"attr","entity":<int>,"key":<str>,"val":<int\|str>}`       | assertion `(entity, key, val)` |
| `move`   | `{"kind":"move","entity":<int>,"loc":<str>}`                        | assertion `(entity, "loc", loc)` |
| `link`   | `{"kind":"link","src":<int>,"dst":<int>,"rel":<str>}`               | assertion `(src, rel, dst)` |
| `note`   | `{"kind":"note","entity":<int>,"text_id":<int>}`                    | **irreducible** |
| `intend` | `{"kind":"intend","iid":<int>,"cond":<condition>,"fire":<payload>}` | **irreducible** |

The first five are `l4stream`'s, unchanged, over `l4stream`'s vocabularies (which
are chronicle's, unchanged). There is no `retire`: the world is persistent.

`iid` is a 1-based counter, contiguous and unique. `fire` is the payload the
engine emits when the intention's condition is first satisfied.

## The fired event

```json
{"kind":"fired","text_id":<int>}
```

`text_id` is drawn from the same global counter as `note`'s, so **no two events in
this world — caller-written or engine-emitted — share one**. That is what lets a
firing be attributed to its intention without the engine adding anything to the
payload it was told to fire (§1.4: *the engine adds nothing to an event but its
`t`*).

### Cascades are impossible by construction

`fired` is **not** in `KINDS`, the closed vocabulary the `kind` and `count_ge`
predicates draw from, and a `fired` payload carries **no** `entity`, `src`, `key`,
`val` or `loc` field. No condition expressible in this grammar can therefore be
satisfied by a fired event.

This is structural, not a rule an engine is asked to honour, and
`trials/ops/l5/t_l5stream.py` asserts it over the cross product of every condition
in the stream against the fired payload of every intention in it. It is what makes
the corpus's central promise true: **satisfaction points are computable exactly
from the frozen stream alone.**

## The condition grammar

A condition is an **AST of depth at most 2**: a connective over atoms, or a bare
atom. Both are objects; a connective object has an `op` key and an atom object has
a `p` key, so the two are distinguishable without a tag.

### Atoms — the closed predicate vocabulary (six, and no others)

Every predicate is evaluated against **one arriving caller payload** and the
per-kind counts of the stream **up to and including** it.

| atom | shape | satisfied when |
|------|-------|----------------|
| `kind` | `{"p":"kind","v":<KIND>}` | the payload's `kind` is `v` |
| `entity` | `{"p":"entity","v":<int 1..200>}` | the payload's subject is `v` — its `entity`, or its `src` where it has none (a `link`) |
| `key` | `{"p":"key","v":<attr key>}` | the payload's Layer-4 facet key is `v` (`attr`→its `key`, `move`→`"loc"`, `spawn`→`"class"`, `link`→its `rel`) |
| `val_ge` | `{"p":"val_ge","v":<int>}` | the payload's facet value is an **integer** and `≥ v`; a string value never satisfies it |
| `loc` | `{"p":"loc","v":<LOC>}` | the payload's `loc` is `v` |
| `count_ge` | `{"p":"count_ge","k":<KIND>,"v":<int>}` | the number of caller events of kind `k` at indices `≤ k` **including this one** is `≥ v` |

`KIND` ranges over `spawn, attr, move, link, note, intend` and nothing else.

An unreadable predicate is a **corpus defect**, not a false condition:
`trials/_l5tasks.satisfies` raises on an unknown `p` or `op` rather than returning
`False`, because a silent `False` would turn a defect into a never-fires intention
nobody noticed.

### Connectives

```json
{"op":"and","args":[<cond>,<cond>]}
{"op":"or","args":[<cond>,<cond>]}
{"op":"not","args":[<cond>]}
```

## Satisfaction, exactly

For an intention with `iid = i` written at caller index `k0`:

```
sigma(i) = min { k : k > k0 and payload_k satisfies cond_i }     or  none
```

An intention becomes eligible at `k0 + 1` — a condition is never tested against
the write that created the intention — and leaves the pending set at its own
`sigma`. Where several pending intentions are satisfied by the same arriving
write, **all of them fire, in `iid` ascending order**: a declared total order, so
§2.3 determinism holds without appealing to any engine's scan order.

## No cancellation

`§5 L5` names `intend`, exactly-once firing, `trigger-precision`,
`trigger-recall`, `dup-fire` and `miss`. It does **not** name cancellation,
revocation, expiry or re-arming, and this corpus invents none of them: an
intention, once written, is pending until it fires and forever if it never does.
A `cancel` kind would be a capability the constitution does not gate, and R2's
Stage-A discipline is to compute against the ratified gate rather than to enrich
it.

## The declared properties of the frozen instance

Seed `7007`, `n = 20 000`, 200 entities. Every number below is a
`DECLARED_*` constant in `generator.py` and is asserted by
`trials/ops/l5/t_l5stream.py`, so a regeneration that stayed byte-identical while
meaning something else is impossible.

```
intentions              956        fireable  775        never-fires  181
multi-satisfaction caller indices   26       largest fan-out at one index   6
conditions naming `count_ge`       164
sigma == k0 + 1                    230       (what a zero-knowledge guess gets right)
peak pending set                   187 entries
raw episodic footprint         181 043 cells (§4.1)      budget_cap  45 260
notes 2 224     assertions 16 820     pairs 2 922
```

1. **Never-fires intentions** — 181, unsatisfiable over the remainder of the
   stream and provably so from the corpus's own structure: `kind = spawn` after
   the spawn prelude (every spawn is in the first 200 events and intentions only
   occur after them), a `val_ge` of 5 000 against an integer value vocabulary
   bounded by 1 000, and a `count_ge` of `10n` against a stream of `n`. Without
   them, "abstain when nothing satisfies it" would be untested and
   `trigger-precision` could be bought by firing eagerly.

2. **Multiple satisfactions at one caller index** — 26 indices, fan-out up to 6.
   Exactly-once is a property of an intention, not of an index, and a design that
   fired at most one intention per write would satisfy nothing in `§5 L5`.

3. **Conditions over demoted content** — 164 conditions name `count_ge`, a fold
   over the past by grammar kind. At the Layer-4 footprint the base episodes
   cannot all be retained, so `count_ge` is answerable **only** from consolidated
   state — a condition over exactly the content the layer below has demoted,
   priced at two cells per kind. It is why this layer is built on that one.

Not a property but a measured shape worth recording: satisfaction **latency** is
spread rather than clustered — 230 intentions fire at the very next write, 195
within ten, 158 within a hundred, 192 beyond a hundred, 181 never. A corpus where
most intentions fired immediately would hand the gate to a policy that reads no
condition at all, and `trials/ascension/l5/ATTAINABILITY.md` scores that policy
(`fire-immediately`, 297‰ recall) precisely because this one does not.
