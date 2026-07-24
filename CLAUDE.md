# CLAUDE.md — Standing Instructions

Read this every session, in full, before you touch anything.

This repository root **is** the `boundary-1-memory/` root. `BOUNDARY.md` is the
frozen constitution; this file is the operating procedure. Where the two ever
seem to conflict, `BOUNDARY.md` wins and you stop and log the conflict.

## 1. Start-of-session ritual (in this order)

1. Read **`BOUNDARY.log`** in full — the entire append-only history.
2. Read **`BOUNDARY.md`** — the constitution.
3. Read the **most recent layer's README** (the highest-numbered layer under
   `core/layers/` that exists; if none exists yet, there is no layer README to
   read and you are pre-Layer-1).

Only after all three do you act.

## 2. Exactly one move

Execute **exactly ONE** move this session, taken from the move set in
`BOUNDARY.md §9`:

`{ FORGE, AUTOPSY, GAPMAP, ASCEND, STRAIN, DOGFOOD, PULSE, PACKAGE }`

Not two. Not "one and a small extra." One.

## 3. Green or nothing commits

`trials/run.py` must **exit 0** before any commit. No exceptions — including
"it's just docs." A red suite means: **no commit**, and the session ends with a
line in `BOUNDARY.log` explaining the failure.

Run it with:

```
python3 trials/run.py
```

## 4. Log every committed move

After every committed move, append **one** line to `BOUNDARY.log`:

```
[L<current>] [MOVE] <what> <suite: N/N green> <anchors: intact|extended>
```

`<current>` is the current layer number (`L0` until Layer 1 is claimed).

## 5. Never edit the frozen

Never edit: `BOUNDARY.md`, frozen layers, frozen trials, frozen corpora,
anchors, or old `BOUNDARY.log` lines. If something frozen seems wrong, **log the
objection and stop.** The human decides. You do not rewrite the sky.

## 6. Purity is a habit, not just a trial

Core purity is enforced by the `laws/` trials — but also by habit. If you find
yourself wanting a **float**, the **wall clock**, or a **package**: the design
is wrong, not the law. Stop and reconsider the design.
