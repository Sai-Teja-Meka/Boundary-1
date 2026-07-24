# Sessions grammar

The **sessions** corpus is a log of interleaved user/agent **sessions** — the
kind of data memtrials will eventually dogfood on. Multiple sessions are open at
once and their events interleave. It is a substrate for Recency/Range,
Association (by `sid`), and later DOGFOOD moves.

Each line is one **event payload** (canonical JSON, §2.4), no `t` field — the
0-based line index is the logical time `t`. Payloads use only integers and
strings.

## Event kinds

| kind            | shape                                                     | meaning                     |
|-----------------|-----------------------------------------------------------|-----------------------------|
| `session_start` | `{"kind":"session_start","sid":<int>,"user":<str>}`       | a session opens             |
| `msg`           | `{"kind":"msg","sid":<int>,"role":<str>,"text_id":<int>}` | a message turn              |
| `tool`          | `{"kind":"tool","sid":<int>,"name":<str>,"code":<int>}`   | a tool invocation + result  |
| `session_end`   | `{"kind":"session_end","sid":<int>,"turns":<int>}`        | a session closes; `turns` = its `msg` count |

## Vocabularies (fixed)

- **user**: `ada borg cleo dex echo fable gus hana`
- **role**: `user agent`
- **tool name**: `search read write exec fetch plan spawn commit`
- **tool code**: uniform in `[0, 9]` (0 = ok; nonzero = a failure code)
- **text_id**: a globally monotonic counter starting at `1` (each `msg` gets a
  fresh unique id)

## Generation rules (deterministic)

1. `sid` is assigned sequentially from `1`. An `open` list tracks currently-open
   sessions, each `{sid, turns}`, in open order.
2. Each step draws a bucket from `prng.below(100)`:
   `[0,15)` → `session_start`, `[15,70)` → `msg`, `[70,90)` → `tool`,
   `[90,100)` → `session_end`.
3. **Feasibility repair**: if `open` is empty the action becomes
   `session_start`; `msg`/`tool`/`session_end` require an open session.
4. `session_start`: new `sid`, `user` uniform; appended to `open`.
5. `msg`: open session chosen uniformly; `role` uniform; `text_id` = next
   counter; the session's `turns` increments.
6. `tool`: open session chosen uniformly; `name` uniform; `code` uniform `[0,9]`.
7. `session_end`: open session chosen uniformly; emits its `turns`; removed by
   swap-pop.

All randomness comes from `corpora/prng.py`. Same `(seed, n)` → byte-identical
output (§8.3).

## Frozen output

- seed `2002`, scale `n = 5000` → `sessions.s2002.n5000.jsonl`.
- Verify: `python3 -m corpora.sessions.generator --check`.
- Rewrite (only when legitimately (re)forging): `... --write`.
