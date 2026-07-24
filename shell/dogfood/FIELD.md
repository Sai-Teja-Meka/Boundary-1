# FIELD.md — what chafed, in use

The dogfood log. `README.md` says what the adapter decided; this file says what
it felt like to use, and it is only useful if it is honest. A note goes in when
something rubbed — a cue that should have worked and didn't, an operation that
needed a workaround, a field that could not be filled truthfully. Praise is not a
field note.

## Standing format

One entry per line, three fields, `|`-separated:

```
<YYYY-MM-DD> | <cue or operation> | <what chafed — one line>
```

The date is the session's date. The second field is the exact cue as typed
(`recall anchors l1`) or the operation (`backfill`, `remember`, `status`).
The third is one line: what chafed, not what to do about it. Entries are
append-only and in date order; nothing here is ever rewritten.

## Notes

2026-07-24 | backfill (13 lines) | `open_questions` is empty on all 13 backfilled events — the log records what a session decided and never what it left open, so the memory of the project's first eleven sessions is structurally thinner than every session after it, and no parser can fix that.
2026-07-24 | backfill (L1 FORGE, L2 ASCEND) | The two sessions that actually built the engine have the tersest log lines in the file — `retention` and `recall` — so they backfill to one decision and zero files each: the store's thinnest entries are its most important ones.
2026-07-24 | recall anchors l1 | Abstained as ambiguous across 3 events, and rightly, but `anchors` turns out to have df=13 — every log line ends with `<anchors: …>` metadata, so the log's own bookkeeping manufactures a token that is present everywhere and discriminates nothing.
2026-07-24 | recall humility ceiling | The cue I expected to hit found nothing: `ceiling` is a `BOUNDARY.md` word, not a `BOUNDARY.log` word, and the store only knows what the log wrote down — the memory is exactly as wide as its source, which is narrower than the project.
2026-07-24 | remember (schema design) | The cue surface had to be an object with the constant value `1`; a list (`["a","b"]`) index-qualifies to `tok.0=a` and a count (`3`) makes a different atom than a cue's `1` — the engine's flattener dictated the schema rather than the other way round, which is correct and still felt like being told.
2026-07-24 | backfill (files_touched) | Mechanical path extraction turned "grounded on README/templates.py:80" into the file `README/templates.py`, which does not exist — a derivation that is faithful to the line and wrong about the world, and the store cannot tell the difference.
2026-07-24 | backfill (decisions) | Splitting prose on `;` had to be taught about parentheses after the memoryagentbench line split mid-`(…)`; every clause is still a guess at what a "decision" was, and the weakest thing in the store is the field that sounds most authoritative.
2026-07-24 | remember (this session's live event) | Writing the observation down made it false: the live event's `open_questions` quote the cue `anchors l1`, so df(`anchors`) went 13 → 14 and the cue now matches 4 events instead of the 3 the note claims — a memory that records its own recall behaviour perturbs it, and the entry stays exactly as it was written.
2026-07-24 | remember --move | `move` cannot be validated against the §9.1 move set, because the log itself carries `FORGE-CORRECTION` and `THEORY`, which that set does not list — the constitution's vocabulary and the log's vocabulary have already drifted, at 13 lines.
