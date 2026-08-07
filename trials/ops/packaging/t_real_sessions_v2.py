"""ops/packaging — the `real-sessions/v2` freeze that was ATTEMPTED and STOPPED.

`[L7] [PACKAGE]` repeated `v1`'s freeze procedure at current scale and the scrub
found something, so the freeze stopped where `v1`'s own README says a freeze
stops: *"a finding stops a freeze and a human decides."*
`corpora/real-sessions/V2-FREEZE-STOPPED.md` is the decision record.

A stop that is only a paragraph is a stop somebody can walk past. What this file
does is make the three things a human's decision rests on **checked on every
suite run**, so none of them can go stale, drift, or be quietly resolved by a
later session:

1. **the finding is still exactly what the record says it is** — one scrub hit,
   family `long_hex`, and the match is `v1`'s own recorded corpus checksum
   sitting in the `[L4] [PACKAGE]` summary that froze it. If it ever becomes two
   findings, or a different family, or a string that is genuinely a secret, the
   decision in front of the human is a different decision and this goes red;
2. **no `v2` was frozen** — `VERSIONS`, `REAL` and the version directories all
   still say one, so a later session cannot land the freeze without landing the
   ruling;
3. **§3's arithmetic** — freezing a `v2` moves `trials/_l7tasks.py`'s surveyed
   population, because a **frozen** Stage-A fixture reads the REAL corpus through
   a late-bound `LATEST`. The delta is asserted as a formula rather than as a
   number, because the store grows every session and the seam does not.

Nothing here gates a score, declares a gate constant, or touches a frozen
artifact. It is the record of a refusal, kept true.
"""

import json
import os
import re

from _harness import PROJECT_ROOT, require, require_equal
from corpora import canon, real_sessions, registry

import _l7tasks

RECORD = os.path.join(PROJECT_ROOT, "corpora", "real-sessions",
                      "V2-FREEZE-STOPPED.md")
STORE = os.path.join(PROJECT_ROOT, "shell", "dogfood", "store", "store.json")

# The finding, as the record states it. A bare count would match a different
# finding of the same size, so the family and the match are both pinned.
FINDING_FAMILY = "long_hex"
FINDING_MATCH = real_sessions.manifest("v1")["sha256"]
FINDING_MOVE = "[L4] [PACKAGE]"

# `trial_no_frozen_artifact_carries_a_generation_required_query` asserts this,
# and `R8` clause 1 records it as the fifth substrate kill's own population.
SURVEYED_ANSWERABLE = 85954


def _store_payloads():
    """The committed dogfood store's events, in ingest order — the freeze's input."""
    with open(STORE, "r", encoding="utf-8") as fh:
        body = json.load(fh)["body"]
    return [record["payload"] for record in body["events"]]


def _record_text():
    with open(RECORD, "r", encoding="utf-8") as fh:
        return fh.read()


# ---- 1. the finding --------------------------------------------------------

def trial_the_scrub_over_the_committed_store_still_finds_exactly_the_recorded_thing():
    """The stop, re-measured. A stop nobody re-runs is a claim somebody made once.

    Deliberately stated over PROPERTIES and not over counts: the store gains an
    event every session this project remembers itself, so an assertion on its
    size would be an assertion about how often the ritual ran. What cannot move
    without the decision changing is *what the scrub finds*.
    """
    payloads = _store_payloads()
    text = canon.encode_jsonl(payloads).decode("utf-8")
    findings = real_sessions.scrub_report(text)

    require_equal(len(findings), 1,
                  "the scrub over the committed store now finds %d thing(s), not "
                  "the one V2-FREEZE-STOPPED.md records: %s. The freeze decision "
                  "in front of a human is about a specific finding, so a second "
                  "one is a different decision and not a bigger version of the "
                  "same one"
                  % (len(findings),
                     ", ".join("%s=%r" % (f["family"], f["match"])
                               for f in findings)))
    require_equal(findings[0]["family"], FINDING_FAMILY,
                  "the scrub finding changed family")
    require_equal(findings[0]["match"], FINDING_MATCH,
                  "the scrub match is no longer v1's own recorded corpus "
                  "checksum. That is what makes it a TRUE positive of the "
                  "pattern and a FALSE positive of the purpose; a different "
                  "string might be neither")


def trial_the_finding_is_the_projects_own_published_number_and_not_a_secret():
    """The whole reason the stop is a *decision* and not an incident.

    The match is `v1`'s manifest checksum. It is printed in the manifest, in the
    corpus README and in the public scorecard, so nothing is being disclosed by
    the corpus that this repository does not publish about itself. What it still
    is, is a 64-character hex run inside prose a corpus would carry, which is the
    one thing `SCRUB_PATTERNS`'s `long_hex` family exists to refuse — and the
    refusal is a human's to lift, not a session's.
    """
    with open(os.path.join(real_sessions.version_dir("v1"), "README.md"),
              "r", encoding="utf-8") as fh:
        readme = fh.read()
    require(FINDING_MATCH in readme,
            "v1's README no longer carries the checksum the scrub matches, so "
            "the claim that the finding is a published number of this project's "
            "own is no longer checkable here")
    require_equal(real_sessions.sha256("v1"), FINDING_MATCH,
                  "v1's frozen bytes no longer hash to the string the scrub "
                  "found — one of the two moved and neither may")


def trial_the_finding_sits_in_the_session_that_wrote_the_scrub():
    """Which event carries it, and the detail that makes it one lapse and not a habit.

    The same decision names three checksums and shortens two of them. That is
    what keeps this a one-line inconsistency rather than a policy the corpus
    family would have to change, and it is asserted so a later reader does not
    have to take the record's word for it.
    """
    payloads = _store_payloads()
    carriers = [(t, p) for t, p in enumerate(payloads)
                if FINDING_MATCH in json.dumps(p, ensure_ascii=False)]
    require_equal(len(carriers), 1,
                  "the checksum now appears in %d store events; the record names "
                  "one" % (len(carriers),))
    t, payload = carriers[0]
    require(payload.get("log_line", "").startswith(FINDING_MOVE),
            "the event carrying the checksum is no longer the %s summary "
            "(it is %r)" % (FINDING_MOVE, payload.get("log_line", "")[:40]))
    decisions = [d for d in payload.get("decisions", []) if FINDING_MATCH in d]
    require_equal(len(decisions), 1, "more than one decision carries it")
    short = re.findall(r"\b[0-9a-f]{7,12}\b", decisions[0])
    require(len(short) >= 2,
            "the decision no longer shortens the other two checksums beside the "
            "one it writes in full — the finding would then be a habit rather "
            "than a lapse, which is a different report")
    require("store t = %d" % (t,) in _record_text(),
            "V2-FREEZE-STOPPED.md does not name `store t = %d`, the event the "
            "finding is actually at" % (t,))


# ---- 2. nothing was frozen -------------------------------------------------

def trial_no_v2_was_frozen_and_the_record_says_why():
    """A refusal is only a refusal while it is still visible in the ledger."""
    require_equal(real_sessions.VERSIONS, ("v1",),
                  "corpora/real_sessions.py declares a version beyond v1. The "
                  "v2 freeze was STOPPED by a scrub finding and stopping is a "
                  "human's decision to lift (V2-FREEZE-STOPPED.md); a session "
                  "that landed it silently would have relaxed the one "
                  "instrument that guards a corpus about to travel")
    require_equal(len(registry.REAL), 1,
                  "corpora/registry.py::REAL holds %d entries for one frozen "
                  "version" % (len(registry.REAL),))
    names = sorted(n for n in os.listdir(real_sessions.CORPUS_ROOT)
                   if os.path.isdir(os.path.join(real_sessions.CORPUS_ROOT, n)))
    require_equal(names, ["v1"],
                  "a version directory exists that VERSIONS does not declare: %s"
                  % (names,))
    require(os.path.exists(RECORD),
            "V2-FREEZE-STOPPED.md is missing — a freeze that stopped and left no "
            "record is indistinguishable from one nobody attempted")


def trial_the_record_states_the_three_refusals_a_session_could_have_taken():
    """The claims ledger discipline, applied to a decision record.

    A stop is worth nothing if the next session cannot see which shortcuts were
    available and declined. These three are the ones that existed.
    """
    flat = " ".join(_record_text().split())
    for fragment in ("freeze anyway", "the scrub reports; it never edits",
                     "fix or withdraw, never relax"):
        require(fragment in flat,
                "V2-FREEZE-STOPPED.md no longer records the refusal %r" % (fragment,))
    require("§9.2" in flat,
            "the record no longer names the clause that makes freezing "
            "irreversible")


# ---- 3. the seam a decision would have to handle ---------------------------

def trial_the_frozen_survey_still_reads_v1_and_the_delta_is_arithmetic():
    """§3 of the record, asserted rather than described.

    `trials/_l7tasks.py::_substrate_rows` is Stage-A code frozen at
    `[L6] [RULING]` and it reads the REAL corpus through a late-bound `LATEST`.
    While `VERSIONS == ("v1",)` that is exactly `v1`, and the frozen Layer-7
    trial's `85 954` describes the 25 events it has always described. The moment
    a `v2` lands, the surveyed population becomes `85 954 − 25 + |v2|` and the
    frozen assertion goes red **for a reason that is not its own finding**.

    Stated as a formula, because the store grows every session and the seam does
    not. What is pinned is the shape of the collision, not this week's size of it.
    """
    survey = _l7tasks.substrate_survey()
    real_rows = [row for row in survey if row["artifact"].startswith("real-sessions")]
    require_equal(len(real_rows), 1, "the survey carries %d REAL rows" % (len(real_rows),))
    row = real_rows[0]
    require_equal(row["artifact"], "real-sessions/v1",
                  "the survey's REAL row is labelled %r" % (row["artifact"],))
    require_equal(row["answerable"], len(real_sessions.payloads("v1")),
                  "the survey's REAL row no longer carries v1's payloads — the "
                  "late-bound default has already moved and the frozen trial is "
                  "measuring an artifact its own row does not name")
    require_equal(sum(r["answerable"] for r in survey), SURVEYED_ANSWERABLE,
                  "the surveyed answerable population moved; R8 clause 1 records "
                  "it and ascension/l7 asserts it")

    would_be = SURVEYED_ANSWERABLE - row["answerable"] + len(_store_payloads())
    require(would_be != SURVEYED_ANSWERABLE,
            "freezing a v2 at the store's current size would leave the surveyed "
            "population unchanged, which would mean the store has not grown "
            "since v1 — then §3 of the record describes nothing")
    require("85 979" in _record_text() or "85979" in _record_text(),
            "V2-FREEZE-STOPPED.md no longer records the figure the seam was "
            "measured at")


def trial_the_live_store_falls_inside_the_refused_class_by_the_same_instrument():
    """The property the seam does NOT threaten, measured so it cannot be assumed.

    `R8` clause 1's kill is that no frozen artifact carries a query whose answer
    is absent from its own stream. Read the live store through the survey's own
    fold and `absent = 0`: a `v2` would join the refused class and force no
    composition. So what a freeze would move is the POPULATION and never the
    FINDING — which is precisely why the red it would cause is the wrong red.

    Deliberately NOT written into `laws/t_rulings.py::REFUSED_STOCK`: extending a
    ruling's holding to an artifact a human never ruled on is a ruling's business
    and not a session's, and this measurement is the evidence such a ruling would
    be taken on.
    """
    payloads = _store_payloads()
    answerable, absent = _l7tasks._answer_values_in_stream(payloads, list(payloads))
    require_equal(answerable, len(payloads),
                  "the survey's own fold does not read every store event as an "
                  "answerable query")
    require_equal(absent, 0,
                  "the live store carries %d answer(s) absent from its own "
                  "stream — it would NOT join R8 clause 1's refused class, and "
                  "V2-FREEZE-STOPPED.md §3 says the opposite" % (absent,))
