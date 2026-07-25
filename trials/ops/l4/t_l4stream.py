"""ops/l4 — the `corpora/l4stream` corpus properties the Layer-4 gate rests on.

The byte-match law (§8.3) freezes this corpus's **bytes**. This file freezes what
the bytes are **for**: a regeneration that stayed byte-identical while meaning
something else would still be caught here, and — more to the point — the
redundancy figures `trials/ascension/l4/ATTAINABILITY.md` builds its verdict on
cannot drift without a red suite.

Four properties, each a declared constant in `corpora/l4stream/generator.py`:

1. **Bounded, persistent population** — exactly `ENTITIES` entities, all spawned
   in the first `ENTITIES` events, none retired, and every reference valid.
2. **Declared assertion redundancy** — the pair count, the assertion count and
   the mean supersession chain, against `DECLARED_*`.
3. **A declared irreducible tier** — every `note` carries a `text_id` that occurs
   **exactly once** in the stream, so no schema can regenerate one.
4. **The redundancy contrast that motivates the corpus** — l4stream's mean chain
   is multiples of the chronicle family's, and its terminal share is a fraction
   of theirs. This is the load-bearing comparison of `ATTAINABILITY.md §5`, and
   it is asserted here rather than merely written down, mirroring how
   `ops/l3/t_l3streamb.py` checks `l3stream` to prove its own statistic is not
   vacuously satisfied.
"""

import collections
from fractions import Fraction

import _l4tasks
from _harness import require, require_equal
from core.state import event_cost
from corpora.l4stream import generator as l4gen


def _payloads():
    return list(l4gen.generate(l4gen.SEED, l4gen.N))


# ---- 1. the population is bounded and persistent ---------------------------

def trial_l4stream_population_is_bounded_and_persistent():
    payloads = _payloads()
    require_equal(len(payloads), l4gen.N, "l4stream length drifted")

    spawns = [p for p in payloads if p["kind"] == "spawn"]
    require_equal(len(spawns), l4gen.ENTITIES,
                  "l4stream spawned an entity outside the prelude — the "
                  "population is supposed to be fixed before the first assertion")
    require_equal([p["entity"] for p in spawns], list(range(1, l4gen.ENTITIES + 1)),
                  "the spawn prelude is not entities 1..ENTITIES in order")
    for i, p in enumerate(payloads[:l4gen.ENTITIES]):
        require_equal(p["kind"], "spawn",
                      "event %d is not part of the spawn prelude" % (i,))

    require(all(p["kind"] != "retire" for p in payloads),
            "l4stream contains a `retire` — the corpus declares a persistent "
            "world, and a churning population is exactly the shape whose "
            "identification cost ATTAINABILITY.md showed cannot be afforded")

    for p in payloads:
        for field in ("entity", "src", "dst"):
            who = p.get(field)
            if who is not None:
                require(1 <= who <= l4gen.ENTITIES,
                        "l4stream references entity %r outside [1, %d] — a "
                        "dangling reference the grammar forbids"
                        % (who, l4gen.ENTITIES))
        if p["kind"] == "link":
            require(p["src"] != p["dst"], "a link relates an entity to itself")


# ---- 2. the declared redundancy ------------------------------------------

def trial_l4stream_redundancy_is_as_declared():
    b = _l4tasks.corpus("l4stream")

    require_equal(len(b["chains"]), l4gen.DECLARED_PAIRS,
                  "l4stream's distinct (entity, key) pair count drifted")
    require_equal(b["assertions"], l4gen.DECLARED_ASSERTIONS,
                  "l4stream's assertion count drifted")
    require_equal(len(b["irreducible"]), l4gen.DECLARED_NOTES,
                  "l4stream's irreducible tier size drifted")
    require_equal(b["raw_cells"], l4gen.DECLARED_RAW_CELLS,
                  "l4stream's raw episodic footprint drifted under the §4.1 "
                  "cost model — every footprint permille in ATTAINABILITY.md "
                  "is a ratio against this number")
    require_equal(len(b["entities"]), l4gen.ENTITIES,
                  "l4stream asserted about an unexpected number of entities")

    lengths = [len(chain) for chain in b["chains"].values()]
    require_equal(max(lengths), l4gen.DECLARED_MAX_CHAIN,
                  "l4stream's longest supersession chain drifted")
    require(min(lengths) >= 1, "a pair with an empty chain was recorded")

    require(len(b["chains"]) <= l4gen.DECLARED_PAIR_UNIVERSE,
            "l4stream asserted more pairs than its grammar's key space admits "
            "(%d > %d) — the pair universe is supposed to be bounded by the "
            "grammar, which is what makes a positional encoding conceivable "
            "here and impossible on chronicle"
            % (len(b["chains"]), l4gen.DECLARED_PAIR_UNIVERSE))

    mean = _l4tasks.permille(Fraction(b["assertions"], len(b["chains"])))
    require_equal(mean, l4gen.DECLARED_MEAN_CHAIN_PERMILLE,
                  "l4stream's mean supersession chain drifted from its declared "
                  "redundancy — the single property the Layer-4 footprint gate "
                  "rests on")

    terminal = _l4tasks.permille(
        Fraction(len(b["chains"]), b["assertions"]))
    require_equal(terminal, l4gen.DECLARED_TERMINAL_SHARE_PERMILLE,
                  "l4stream's terminal-assertion share drifted — this is the "
                  "share a current-value table with no history could answer")


# ---- 3. the irreducible tier ---------------------------------------------

def trial_l4stream_notes_are_irreducible():
    payloads = _payloads()
    notes = [p for p in payloads if p["kind"] == "note"]
    require_equal(len(notes), l4gen.DECLARED_NOTES, "the note count drifted")

    seen = collections.Counter(p["text_id"] for p in notes)
    repeated = [tid for tid, c in seen.items() if c > 1]
    require(not repeated,
            "text_id %r occurs more than once — the irreducible tier is only "
            "irreducible if nothing in the stream repeats it, otherwise a schema "
            "could regenerate a note from another note" % (repeated[:3],))
    require_equal(sorted(seen), list(range(1, len(notes) + 1)),
                  "text_ids are not the contiguous counter the grammar declares")

    # And they really are outside the assertion facet: no note contributes to a
    # chain, so no interval table can ever reconstruct one.
    for p in notes:
        require(_l4tasks.facet(p) is None,
                "a note produced an (entity, key, value) facet — it would then "
                "be regenerable, and the F gate would have nothing to bite on")


# ---- 4. the contrast with the chronicle family ----------------------------

def trial_l4stream_is_more_redundant_than_the_chronicle_family():
    """The comparison ATTAINABILITY.md's verdict turns on, asserted not narrated.

    Without this, "chronicle is too high-entropy for the gate" would be a claim
    in a document. With it, the claim is a trial: if the chronicle family ever
    became as redundant as `l4stream`, or `l4stream` as sparse as chronicle, the
    suite goes red and the Layer-4 corpus choice is reopened.
    """
    l4 = _l4tasks.corpus("l4stream")
    l4_mean = Fraction(l4["assertions"], len(l4["chains"]))
    require(l4_mean >= 4,
            "l4stream's mean supersession chain fell to %s — the footprint gate "
            "demands ≥4× compression, and a chain shorter than 4 cannot pay for "
            "its own pair identification" % (l4_mean,))

    for name in ("chronicle", "murk"):
        b = _l4tasks.corpus(name)
        mean = Fraction(b["assertions"], len(b["chains"]))
        require(mean < 2,
                "%s's mean supersession chain rose to %s — it is no longer the "
                "write-once world ATTAINABILITY.md measured, and the Layer-4 "
                "corpus finding must be recomputed" % (name, mean))
        require(l4_mean > 3 * mean,
                "l4stream is no longer materially more redundant than %s "
                "(%s vs %s) — the corpus it was built to replace"
                % (name, l4_mean, mean))

        terminal = Fraction(len(b["chains"]), b["assertions"])
        require(terminal > Fraction(3, 4),
                "%s's terminal-assertion share fell to %s — the property that "
                "lets a history-free current-value table nearly tie its oracle"
                % (name, terminal))


# ---- the cost model this corpus is priced under ---------------------------

def trial_l4stream_event_costs_are_the_frozen_model():
    """Per-kind costs, so a change in `payload_cost` cannot silently move a gate."""
    expected = {"spawn": 7, "attr": 9, "move": 7, "link": 9, "note": 7}
    seen = {}
    for p in _payloads():
        seen.setdefault(p["kind"], set()).add(event_cost(p))
    for kind, costs in sorted(seen.items()):
        require_equal(sorted(costs), [expected[kind]],
                      "l4stream %s events no longer cost %d cells under the "
                      "frozen §4.1 model" % (kind, expected[kind]))
    require_equal(sorted(seen), sorted(expected),
                  "l4stream's kind vocabulary drifted")
