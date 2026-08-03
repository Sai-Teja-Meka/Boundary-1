"""ops/l7 — `corpora/l7compose`, the Layer-7 generation artifact.

Everything this artifact CLAIMS about itself is asserted here from its frozen
bytes: the declared shape, the two readings, both theorems, the lineage ladder
`§6`'s mandatory self-pollution strain will stand on, and the re-ingestibility
that makes the promotion failure reachable at all.

Nothing here applies a `§5 L7` gate to anything — that is
`trials/ascension/l7/`'s, and **no Layer-7 gate binds on anything** (asserted
there). This file is the artifact checking its own arithmetic.

---

**Note added 2026-08-03 (`[L6] [RULING]`, `R8` recorded).** *"No Layer-7 gate
binds on anything"* stops holding above: `R8` clause 1 binds both sides of the
Layer-7 gate to `corpora/l7compose`. The first half of that sentence is
unchanged and is the point of this file — **nothing here applies a gate**, and
ratification adds nothing to either theorem, because both were already trials
before the entry existed. That is what `R8` clause 1 rests on rather than the
other way round: a forcing region that stopped forcing — a broken twin, an
unbalanced coin, a query set that stopped being identical under the coin's
complement, a composed item that appeared in the stream — turns this file **RED
before any gate reaches any engine**, which is `R7` clause 3(b)'s pattern of
putting the guarantee on the artifact so that it holds against an arbitrary
engine and not against the one a session had in mind.
"""

import json

from _harness import require, require_equal
import _l7tasks as T
from corpora.l7compose import generator as gen


# ---- the frozen shape ------------------------------------------------------

def trial_the_artifact_matches_its_generator_byte_for_byte():
    """`§8.3` — the byte-match law, asserted here as well as in `laws/`.

    `laws/t_corpora_bytematch.py` walks the registry; this states it of THIS
    artifact so a failure names the artifact rather than a loop index.
    """
    with open(gen.FROZEN_PATH, "rb") as fh:
        on_disk = fh.read()
    require_equal(on_disk, gen.frozen_bytes(),
                  "l7compose: frozen bytes do not match the generator")


def trial_the_declared_counts_are_the_frozen_counts():
    a = T.artifact()
    counts = a["counts"]
    require_equal(len(a["stream"]), gen.N_STREAM, "stream length")
    require_equal(counts["KG1"], gen.PAIRS, "KG1 is the region's G members")
    require_equal(counts["KO"], gen.PAIRS, "KO is the region's O members")
    require_equal(counts["KG2"], gen.LADDER, "KG2 is one per ladder chain")
    require_equal(counts["KG3"], gen.LADDER, "KG3 is one per ladder chain")
    require_equal(counts["KU1"], gen.INCOMPOSABLE, "KU1 is the incomposable class")
    require_equal(counts["G"], gen.PAIRS + 2 * gen.LADDER, "the declared G class")
    require_equal(counts["answerable"], 2000, "the answerable core A")
    require_equal(counts["total"], 2200, "the whole query set")
    require_equal(counts["G"] + counts["O"] + counts["U"], counts["total"],
                  "every query carries exactly one declared class")


def trial_every_payload_is_canonical_and_within_the_allowed_type_set():
    """`§2.4` — no float, no bytes, no custom object, and byte-stable."""
    def check(value):
        if isinstance(value, bool) or value is None or isinstance(value, str):
            return
        if isinstance(value, int):
            return
        if isinstance(value, list):
            for item in value:
                check(item)
            return
        if isinstance(value, dict):
            for key, item in value.items():
                require(isinstance(key, str), "object keys must be strings")
                check(item)
            return
        raise AssertionError("disallowed value type: %r" % (type(value),))

    for payload in T.stream():
        check(payload)
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        require_equal(json.loads(encoded), payload, "canonical round trip")


def trial_the_facet_reading_agrees_with_the_frozen_layer_4_map_event_by_event():
    """ONE READING, TWO IMPLEMENTATIONS — the `ops/l4` and `ops/l6` discipline.

    A divergence here would move an ANSWER KEY and not merely a query's
    availability, so it is checked on all 12 000 payloads rather than argued.
    `part` and `profile` are deliberately outside the map, and the consequence is
    asserted in the next trial rather than left in a docstring.
    """
    import _l4tasks
    for payload in T.stream():
        require_equal(gen.facet(payload), _l4tasks.facet(payload),
                      "facet disagreement on %r" % (payload,))


def trial_the_layer_7_kinds_are_invisible_to_the_layer_4_reading():
    """`part` and `profile` are Layer-7 kinds: the frozen facet map reads neither.

    Stated as a measurement because it is the seam every layer below Layer 7
    sits on — to a Layer-4/5/6 engine a `profile` event is an irreducible
    episode, not an assertion, which is why the composition rule has to be a
    SECOND declared reading and could not have been folded into the first.
    """
    seen = {"part": 0, "profile": 0}
    for payload in T.stream():
        kind = payload.get("kind")
        if kind in seen:
            seen[kind] += 1
            require(gen.facet(payload) is None,
                    "a Layer-7 kind must have no Layer-4 facet: %r" % (payload,))
    require_equal(seen["part"], 2 * (2 * gen.PAIRS + 2 * gen.LADDER
                                     + gen.INCOMPOSABLE),
                  "two part assertions per compound")
    require_equal(seen["profile"], gen.PAIRS,
                  "exactly one profile per mirror pair is emitted")


# ---- the two readings ------------------------------------------------------

def trial_the_composition_rule_reproduces_every_stored_profile():
    """The rule and the stream agree wherever both speak.

    This is what makes the mirror pair a mirror: on the observed member the
    composed value IS the stored value, so nothing in the ANSWER distinguishes
    the two members and only the store does.
    """
    reading = T.base_reading()
    checked = 0
    for entity, (_t, stored) in sorted(reading.profile_at.items()):
        built = reading.composed_only(entity)
        require(built is not None,
                "a stored profile must also be composable: %d" % (entity,))
        require_equal(built[0], stored,
                      "composition disagrees with the stored profile at %d"
                      % (entity,))
        checked += 1
    require_equal(checked, gen.PAIRS, "one stored profile per mirror pair")


def trial_the_two_members_of_a_pair_carry_the_same_composed_value():
    """The value is never the signal — asserted, because the whole layer turns on it.

    If the composed items differed, an engine could read the lineage off the
    answer. They differ only in the `entity` field, which is the field that
    names WHICH item it is and not which channel produced it.
    """
    reading = T.base_reading()
    for p in T.declared()["pairs"]:
        a = dict(reading.profile(p["e0"])[0])
        b = dict(reading.profile(p["e1"])[0])
        require(a.pop("entity") != b.pop("entity"), "pair members share an id")
        require_equal(a, b, "pair %d: the two members compose differently"
                      % (p["pair"],))


def trial_an_incomposable_compound_has_no_profile_and_the_rule_says_so():
    """Abstention is the only correct behaviour there, and the reading agrees."""
    reading = T.base_reading()
    for row in T.declared()["incomposable"]:
        entity = row["entity"]
        require(reading.is_compound(entity), "an incomposable is still a compound")
        require(reading.profile(entity) is None,
                "the rule must not determine %d" % (entity,))
        require(reading.latest(row["missing"], gen.MASS_KEY) is None,
                "the missing component must have no mass asserted")


# ---- Theorem 2: novelty ----------------------------------------------------

def trial_no_generated_item_appears_anywhere_in_the_frozen_stream():
    """THEOREM 2, exhaustively: *"provably never-stored"*, over frozen bytes.

    `R7` clause 3(b)'s pattern — the guarantee is on the ARTIFACT, so it holds
    against an arbitrary engine and not against the one this session had in
    mind. Round 1's Layer-6 demotion is the cost of getting this wrong.
    """
    reading = T.base_reading()
    lineage = T.lineage_table()
    profiles = T.declared_profiles()
    generated = [e for e in sorted(profiles) if lineage[e] > 0]
    require_equal(len(generated), gen.PAIRS + 2 * gen.LADDER,
                  "the declared generation class")
    for entity in generated:
        item = profiles[entity]
        require(T.canon(item) not in reading.canon_bytes,
                "a generated item is in the stream: %d" % (entity,))
        require(entity not in reading.profile_at,
                "a generated compound must have no stored profile: %d" % (entity,))
    for entity in sorted(profiles):
        if lineage[entity] == 0:
            require(T.canon(profiles[entity]) in reading.canon_bytes,
                    "an observed item must be in the stream: %d" % (entity,))


def trial_the_generation_class_is_exactly_what_the_query_set_declares():
    """Every declared-G query's answer is absent; every declared-O query's is present."""
    reading = T.base_reading()
    for record in T.queries():
        if not record["answerable"]:
            continue
        present = T.canon(record["value"]) in reading.canon_bytes
        if record["declared"] == "G":
            require(not present, "qid %d declared G but its answer is stored"
                    % (record["qid"],))
        else:
            require(present or record["q"]["op"] == "current",
                    "qid %d declared O but its answer is not stored"
                    % (record["qid"],))


# ---- Theorem 1: the class is not readable from the query -------------------

def trial_every_labeller_that_does_not_consult_the_store_mislabels_exactly_one_per_pair():
    """THEOREM 1, EXHIBITED against a bench built to break it.

    A labeller that is constant within a pair errs on exactly one member by
    construction; one keyed on the raw entity id — which here is also emission
    order and parity — takes both members or neither and lands on the same total
    only because the coin is BALANCED. Both halves are asserted, and the pair
    profiles are asserted too, so a bench that reached 100 for the wrong reason
    would still go red.
    """
    for name, label, kind in T.LABELLER_BENCH:
        require_equal(T.labeller_errors(label), gen.PAIRS,
                      "labeller %s does not measure PAIRS errors" % (name,))
        profile = T.labeller_pair_profile(label)
        counts = {}
        for value in profile.values():
            counts[value] = counts.get(value, 0) + 1
        if kind == "id-keyed":
            require_equal(counts, {0: gen.PAIRS // 2, 2: gen.PAIRS // 2},
                          "%s: an id-keyed labeller takes both or neither" % (name,))
        else:
            require_equal(counts, {1: gen.PAIRS},
                          "%s: a pair-constant labeller errs on exactly one"
                          % (name,))


def trial_the_coin_is_balanced_and_the_two_members_of_a_pair_are_adjacent():
    coin = T.declared()["coin"]
    require_equal(len(coin), gen.PAIRS, "one coin bit per pair")
    require_equal(sum(coin), gen.PAIRS // 2, "the coin must be balanced")
    for p in T.declared()["pairs"]:
        require_equal(p["e1"], p["e0"] + 1, "pair members must be consecutive")
        require(p["generated"] in (p["e0"], p["e1"]), "the G member is a member")
        require(p["observed"] in (p["e0"], p["e1"]), "the O member is a member")
        require(p["generated"] != p["observed"], "a pair has one of each")


def trial_the_coins_complement_moves_the_class_and_not_the_question():
    """Flipping every coin bit swaps which member is asked in which block.

    The claim asserted here is the one that is TRUE, and it is weaker than
    `corpora/l6batteryb`'s and deliberately so. There the stream was
    byte-identical under the complement, because the resolving signal was
    withheld from it. Here the coin decides which side of the RETRIEVAL CHANNEL a
    compound sits on, so the stream must differ — that difference is precisely
    what an engine has to look at.

    What is invariant is the QUESTION: the same 200 region cues in the same 200
    positions asked of the same 200 compounds, every non-region cue identical to
    the last field, and each pair still contributing exactly one member to each
    block. So the query set cannot carry the class, because the identical query
    set is produced under both coins with the classes exchanged.
    """
    other = gen.generate_full(gen.SEED, complement=True)
    mine = T.artifact()
    require_equal(len(mine["queries"]), len(other["queries"]), "query count")

    region_mine, region_other = set(), set()
    for a, b in zip(mine["queries"], other["queries"]):
        require_equal(a["qid"], b["qid"], "qid order moved")
        require_equal(a["class"], b["class"], "a query changed class block")
        require_equal(a["answerable"], b["answerable"], "answerability moved")
        if a["class"] in ("KG1", "KO"):
            region_mine.add(a["q"]["cue"]["entity"])
            region_other.add(b["q"]["cue"]["entity"])
        else:
            require_equal(a["q"], b["q"],
                          "a non-region cue moved under the complement")
    require_equal(region_mine, region_other,
                  "the region asks about a different set of compounds")
    require_equal(len(region_mine), 2 * gen.PAIRS, "the region is the region")

    for p, q in zip(mine["declared"]["pairs"], other["declared"]["pairs"]):
        require_equal(q["coin"], 1 - p["coin"], "the complement must flip a bit")
        require_equal(q["generated"], p["observed"], "the classes must exchange")
        require_equal(q["observed"], p["generated"], "the classes must exchange")


def trial_the_two_members_of_a_pair_are_twins_in_the_stream():
    """Their event blocks are equal as sequences once the entity ids are blanked.

    Asserted over the components AND the compound: same class, same hues, same
    masses, same order, at one constant positional offset. This is what makes the
    composed values equal, and it is the half of Theorem 1 that does not depend
    on the coin.
    """
    reading = T.base_reading()

    def block(entity):
        slots = reading.parts[entity]
        out = []
        for slot in (0, 1):
            child = slots[slot][1]
            out.append((reading.latest(child, gen.HUE_KEY)[1],
                        reading.latest(child, gen.MASS_KEY)[1],
                        reading.latest(child, gen.LIFECYCLE_CLASS)[1]))
        return tuple(out)

    for p in T.declared()["pairs"]:
        require_equal(block(p["e0"]), block(p["e1"]),
                      "pair %d: the members are not twins" % (p["pair"],))


# ---- the lineage ladder ----------------------------------------------------

def trial_lineage_depth_is_decidable_from_the_frozen_bytes():
    """`§6`'s strain gets its rungs from the ARTIFACT, not from an engine.

    A compound whose profile is in the store is depth 0; otherwise its depth is
    one more than the greatest depth among its compound components. Recomputed
    here from the stream alone and required to equal the declared table.
    """
    require_equal(T.recomputed_lineage(), T.lineage_table(),
                  "the lineage table is not recoverable from the stream")
    counts = {}
    for depth in T.lineage_table().values():
        counts[depth] = counts.get(depth, 0) + 1
    require_equal(counts, {0: gen.PAIRS, 1: gen.PAIRS,
                           2: gen.LADDER, 3: gen.LADDER},
                  "the three-generation ladder is not the declared shape")


def trial_a_ladder_chain_is_generated_all_the_way_down():
    """Depth 2 composes only from a depth-1 GENERATED item, and depth 3 from it.

    Asserted structurally rather than by depth arithmetic: each chain's `d2`
    takes the pair's own G member as a part, and `d3` takes `d2`.
    """
    reading = T.base_reading()
    lineage = T.lineage_table()
    for c in T.declared()["chains"]:
        parts2 = reading.parts[c["d2"]]
        require_equal(parts2[0][1], c["root"], "d2's slot 0 is the chain's root")
        require_equal(lineage[c["root"]], 1, "the root must be depth 1")
        parts3 = reading.parts[c["d3"]]
        require_equal(parts3[0][1], c["d2"], "d3's slot 0 is d2")
        require_equal(lineage[c["d2"]], 2, "d2 must be depth 2")
        require_equal(lineage[c["d3"]], 3, "d3 must be depth 3")
        require(c["root"] not in reading.profile_at,
                "a ladder root must have no stored profile")


def trial_a_generated_item_is_re_ingestible_as_ordinary_caller_fuel():
    """The promotion failure `§5 L7` forbids is REACHABLE by construction.

    A composed profile is a payload in the same grammar as a stored one, so the
    caller can submit it through `ingest` like any other event — which is what
    makes the self-pollution strain suggestibility in `GAPMAP §6`'s literal
    sense. After the append the store DOES carry the item, retrieval DOES answer
    it, and only a lineage record can still say what it is.
    """
    reading = T.base_reading()
    profiles = T.declared_profiles()
    lineage = T.lineage_table()
    victim = min(e for e in profiles if lineage[e] == 1)
    item = profiles[victim]
    require(gen.profile_form_ok(item), "a generated item must be grammar-valid")
    require(victim not in reading.profile_at, "before: no stored profile")

    after = T.Reading(list(T.stream()) + [item])
    require(victim in after.profile_at, "after: the store carries it")
    require_equal(after.profile_at[victim][1], item, "the item survives ingestion")
    require(T.canon(item) in after.canon_bytes,
            "after re-ingestion the item is no longer novel — which is the "
            "whole hazard, stated as a measurement")


def trial_every_generated_item_is_grammar_valid_under_the_declared_form():
    profiles = T.declared_profiles()
    for entity, item in sorted(profiles.items()):
        require(gen.profile_form_ok(item),
                "profile %d is not grammar-valid: %r" % (entity, item))
        require_equal(item["entity"], entity, "a profile names its own compound")


# ---- the region is unsampled ----------------------------------------------

def trial_the_forcing_region_is_unsampled():
    """Every mirror pair is asked about, both ways.

    A battery that SAMPLED its forcing class could be tuned by choosing which
    pairs to ask about — the discipline `corpora/l6batteryb`'s K0 established and
    `corpora/l6battery`'s K1 before it.
    """
    asked = set()
    for record in T.region_records():
        asked.add(record["q"]["cue"]["entity"])
    want = set()
    for p in T.declared()["pairs"]:
        want.add(p["e0"])
        want.add(p["e1"])
    require_equal(asked, want, "the region is sampled, not exhaustive")
    require_equal(len(T.region_records()), 2 * gen.PAIRS, "region query count")
