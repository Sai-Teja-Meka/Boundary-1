# `.github/` — harness scaffolding

Added by the `[L4] [PULSE]` session as **sanctioned maintenance**. Nothing in
this directory is frozen, nothing here is a trial, and nothing here carries a
constitutional number. It is the harness around the gate, not part of the gate.

## What is here

| file | what it does |
|---|---|
| `workflows/trials.yml` | runs `python3 trials/run.py` on every open PR's **merge preview** |

## Why it exists

`BOUNDARY.md §9.3` and `CLAUDE.md §3` bind the suite to the **commit**: green or
nothing. A session can honour that on its own branch and still be wrong about the
tree it is about to create, because the merge result is a tree no session ever
ran the suite on.

That is not hypothetical. `BOUNDARY.log` line 19 records it:

> *"the second run of the PULSE whose branch could not merge (PR #7 closed on a
> ledger collision: it was cut from a main lacking PR #6, and laws/t_rulings.py's
> byte-exact append-only prefix forbids resolving a `BOUNDARY.log`/store collision
> in place)."*

Both branches were green. The merge was not. `BOUNDARY.log`,
`BOUNDARY-RULINGS.md` and the dogfood store are strictly append-only ledgers
written by every session, so two sessions in flight collide on all three by
construction — and `t_rulings.py` is the trial that can tell, because it settles
append-only against `git log` rather than against a session's good intentions.

GitHub already builds the merge preview at `refs/pull/N/merge`;
`actions/checkout` takes it by default on the `pull_request` event. So the suite
runs against the tree the merge would produce, and a collision goes **red on the
PR** rather than on the default branch.

## What it deliberately does not do

* **No auto-merge.** `permissions: contents: read`. The workflow cannot merge,
  push, comment, label, or approve.
* **No PR-watching.** It reacts to the `pull_request` event and stops. It does
  not poll, subscribe, or re-run itself.
* **No verdict.** It reports a red suite; a human reads it and decides. §9 gives
  a session one move, and merging is not one of them.

## Two things a later session should know before changing it

* **`fetch-depth: 0` is load-bearing.** `t_rulings.py` walks every committed
  version of each ledger and requires it to be a byte-exact prefix of the file on
  disk. A shallow clone leaves that walk with no history, and the check becomes
  either red for the wrong reason or vacuously green. The workflow asserts the
  precondition in its own step so a vacuous green cannot pass unnoticed.
* **A conflicting PR has no merge preview at all.** If git cannot auto-merge the
  ledgers, `refs/pull/N/merge` does not exist and GitHub reports the conflict
  directly; this workflow is for the merges git *can* perform and that are
  nevertheless wrong. Both failures end in the same place — a human resolves it
  by rebasing onto the current default branch and re-running the suite, which is
  what the reland at `BOUNDARY.log` line 19 did.

There is no run on the default branch. Catching a collision after the merge is
not what this is for, and adding one is a later session's decision, not this
file's assumption.
