"""ops/packaging — `packaging/CATALOG.md`, checked against the repository it describes.

`CATALOG.md` is the `[L7] [PACKAGE]` deliverable that carries three things a
reader cannot get out of `BOUNDARY.md §5`: the seven-sin map in its complete
Phase-3 form, the three **catalog extensions** the ladder minted, and — adjacent
to those and deliberately not inside them — the **four-kind impossibility
taxonomy**.

Every one of those is a claim about files in this repository, so every one of
them is checked here rather than trusted. The failure this guards against is the
one `autopsy/GAPMAP.md §2` convicts four engines of: a document that records the
metadata which would make it correct and is then read by nothing. A catalog whose
rows name trials that do not exist is that failure wearing a catalog's clothes.

Three kinds of check, and the second is the one with teeth:

1. **every trial the catalog names exists**, under the class the catalog puts it
   in — so a row cannot survive the trial it rests on being renamed or retired;
2. **every quotation is the source's own text**, compared under one whitespace
   normalization of both sides (markdown wraps, so a verbatim line-for-line
   compare would be a compare of line breaks);
3. **the load-bearing distinctions are still stated** — the trial-class migration
   of the denominator law, the instrument-versus-engine reading of the novelty
   horizon, and the taxonomy being a humility axis rather than an eighth sin.
   Those three sentences are the reason the file exists; a catalog that lost them
   would still parse.
"""

import os
import re

from _harness import PROJECT_ROOT, require, require_equal

CATALOG = os.path.join(PROJECT_ROOT, "packaging", "CATALOG.md")
TRIALS = os.path.join(PROJECT_ROOT, "trials")
HUMILITY = os.path.join(TRIALS, "humility")

# `class/lN::trial_name` is how the catalog cites a trial. Anything else in the
# file is prose and is not a citation.
CITATION = re.compile(r"`(laws|ops|ascension|humility|inheritance|strain|anchors)"
                      r"/(l\d)::(trial_[a-z0-9_]+)`")

# The four one-sentence forms, each keyed to the layer it names, and each a span
# of `trials/humility/l7/IMPOSSIBILITY.md §3` — the document that named the four
# kinds. Checked as *fragments the catalog must carry and the source must
# contain*, under one normalization, so that markdown wrapping cannot make a
# true quotation look false.
TAXONOMY_QUOTES = {
    "L4": "so no injective map exists and the answers are unreachable",
    "L5": "nothing is missing from the state, and what is missing is a verb",
    "L6": "Confidence emitted is not confidence calibrated",
    "L7": "no reading of held state produces an item the store never contained",
}

# The novelty horizon, quoted from `core/layers/README-l7.md §2.2`.
NOVELTY_HORIZON_SOURCE = os.path.join(PROJECT_ROOT, "core", "layers",
                                      "README-l7.md")

# The lateness theorem, quoted from `core/layers/README-l5.md §4`.
LATENESS_SOURCE = os.path.join(PROJECT_ROOT, "core", "layers", "README-l5.md")


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _flat(text):
    """One normalization, applied to both sides of every comparison.

    Markdown wraps prose and quotes it behind `>`, so a line-for-line compare
    would be a compare of line breaks and blockquote markers. Emphasis marks go
    too: a source that gained a bold on one word of a sentence has not changed
    the sentence.
    """
    lines = [re.sub(r"^\s*>+\s?", "", line) for line in text.split("\n")]
    return " ".join(" ".join(lines).replace("*", "").replace("`", "").split())


def _catalog():
    return _read(CATALOG)


# ---- 1. every named trial exists, in the class the catalog claims -----------

def trial_every_trial_the_catalog_names_exists_in_the_class_it_names():
    """A row you cannot run is a row that has already started to rot.

    The catalog's own §1 rule. Checked by walking the citations out of the file
    and looking for each `def trial_…` under the class directory the citation
    puts it in — the class matters, because §2.1's whole finding is that the
    denominator law CHANGED CLASS and an audit looking in the wrong one would
    conclude it was dropped.
    """
    citations = CITATION.findall(_catalog())
    require(len(citations) >= 15,
            "the catalog names only %d trials; §1 alone has seven rows and every "
            "one of them is supposed to carry at least one"
            % (len(citations),))
    for klass, layer, name in citations:
        directory = os.path.join(TRIALS, klass, layer)
        require(os.path.isdir(directory),
                "CATALOG.md cites %s/%s::%s but %s/%s is not a trial directory"
                % (klass, layer, name, klass, layer))
        found = [fn for fn in sorted(os.listdir(directory))
                 if fn.startswith("t_") and fn.endswith(".py")
                 and ("def %s(" % (name,)) in _read(os.path.join(directory, fn))]
        require(found,
                "CATALOG.md cites %s/%s::%s and no file under trials/%s/%s "
                "defines it — either the trial was renamed and the catalog was "
                "not, or the row is describing something that does not run"
                % (klass, layer, name, klass, layer))


def trial_the_seven_sins_are_all_present_and_each_carries_a_tier():
    """§1 is complete or it is not the Phase-3 form it claims to be."""
    flat = _flat(_catalog())
    for sin in ("Transience", "Absent-mindedness", "Blocking", "Misattribution",
                "Suggestibility", "Bias", "Persistence"):
        require(sin in flat,
                "CATALOG.md §1 no longer carries the sin %r — the map is "
                "advertised as complete and a missing row makes that false"
                % (sin,))
    require("the mandatory Layer 7 self-pollution strain" in flat,
            "the catalog no longer records that suggestibility is the one sin "
            "the CONSTITUTION schedules in its own frozen text (§6), which is "
            "what distinguishes it from the six the catalog merely maps")


# ---- 2. the quotations are the sources' own text ---------------------------

def trial_the_four_one_sentence_forms_are_the_taxonomys_own_words():
    """`humility/l7/IMPOSSIBILITY.md §3` named the four kinds; this quotes it.

    Compared under one normalization of both sides. A quotation that drifted
    would be this file inventing a taxonomy rather than publishing one, which is
    exactly the direction `packaging/` is forbidden to move in: it describes and
    never redefines.
    """
    catalog = _flat(_catalog())
    source = _flat(_read(os.path.join(HUMILITY, "l7", "IMPOSSIBILITY.md")))
    for layer, quote in sorted(TAXONOMY_QUOTES.items()):
        needle = _flat(quote)
        require(needle in source,
                "%s: the taxonomy source no longer contains %r — the catalog is "
                "quoting a document that has moved" % (layer, quote))
        require(needle in catalog,
                "%s: CATALOG.md no longer carries the one-sentence form %r"
                % (layer, quote))
    for word in ("absent bits", "absent machinery", "absent order",
                 "absent generativity"):
        require(word in source and word in catalog,
                "the taxonomy's own word %r is missing from one side" % (word,))


def trial_every_impossibility_document_exists_and_the_taxonomy_covers_l4_to_l7():
    """`§6` requires one per humility trial; the catalog names four KINDS, not six.

    Both halves are checked, because the honest statement is the awkward one:
    there are **six** `IMPOSSIBILITY.md` files and **four** named kinds, and the
    catalog has to say what `l2` and `l3` are rather than quietly counting them
    in. A taxonomy applied backwards to documents that did not claim it would be
    this file redefining rather than describing.

    The catalog's own hedge — that the taxonomy is final only *below*
    `BOUNDARY-HIGH.md` — has to still be there too, or the file claims more than
    the ladder has earned.
    """
    layers = sorted(name for name in os.listdir(HUMILITY)
                    if os.path.isdir(os.path.join(HUMILITY, name))
                    and re.fullmatch(r"l\d+", name))
    for layer in layers:
        path = os.path.join(HUMILITY, layer, "IMPOSSIBILITY.md")
        require(os.path.exists(path),
                "trials/humility/%s ships no IMPOSSIBILITY.md, which §6 requires "
                "of every humility trial" % (layer,))
    for layer in ("l4", "l5", "l6", "l7"):
        require(layer in layers,
                "the taxonomy names a kind for %s and there is no humility "
                "directory for it" % (layer,))
    flat = _flat(_catalog())
    require_equal(len(TAXONOMY_QUOTES), 4, "the taxonomy is four kinds")
    if len(layers) > len(TAXONOMY_QUOTES):
        outside = [layer for layer in layers if layer not in ("l4", "l5", "l6", "l7")]
        require("there are six of them" in flat or "six" in flat,
                "there are %d IMPOSSIBILITY.md files and four named kinds; "
                "CATALOG.md §3 must say what %s are rather than leaving a "
                "reader to assume the taxonomy covers the class"
                % (len(layers), ", ".join(outside)))
        for layer in outside:
            require(layer in flat,
                    "CATALOG.md §3 does not account for trials/humility/%s, "
                    "which ships an IMPOSSIBILITY.md the taxonomy does not name"
                    % (layer,))
    require("BOUNDARY-HIGH.md" in flat,
            "CATALOG.md no longer records that the taxonomy is final only BELOW "
            "the unwritten threshold document — without that hedge it claims to "
            "be final full stop, which no session may claim")


def trial_the_novelty_horizon_is_quoted_from_the_layer_readme():
    """`60 → 30 → 0`, and the two clauses that hold while it falls.

    The numbers are the point and so is what does NOT move beside them: the
    catalog's whole claim is that this is an instrument's failure and not an
    engine's, which is only true because `tagging` holds at 1000 and `promotion`
    stays 0 across the same three rungs.
    """
    source = _flat(_read(NOVELTY_HORIZON_SOURCE))
    catalog = _flat(_catalog())
    for fragment in ("60 -> 30 -> 0",
                     "while tagging holds at 1000 and promotion stays 0",
                     "a byte-comparison would call this engine a liar about "
                     "every item it made"):
        require(fragment in source,
                "core/layers/README-l7.md §2.2 no longer contains %r"
                % (fragment,))
        require(fragment in catalog,
                "CATALOG.md §2.2 no longer quotes %r" % (fragment,))


def trial_the_lateness_theorem_is_quoted_and_carries_its_three_applications():
    """One sentence, three applications, and the refusal is the middle one."""
    source = _flat(_read(LATENESS_SOURCE))
    catalog = _flat(_catalog())
    sentence = ("A condition over a layer fires when the layer is CLAIMED; the "
                "store can watch for a fact, not for the moment before it")
    require(sentence in source,
            "core/layers/README-l5.md §4's lateness note no longer states the "
            "theorem in the form the catalog quotes")
    require(sentence in catalog,
            "CATALOG.md §2.3 no longer carries the theorem in the source's own "
            "words")
    for fragment in ("iid 1", "iid 2", "iid 3", "R7 clause 7's bequest"):
        require(fragment in catalog,
                "CATALOG.md §2.3 no longer records the application %r — the "
                "middle one is a REFUSAL to arm and is the useful half"
                % (fragment,))
    require("a promise worth arming is one whose right moment is a fact this "
            "reading can assert" in catalog,
            "the rule as applied at arming time is gone from the catalog")


# ---- 3. the load-bearing distinctions --------------------------------------

def trial_the_denominator_laws_trial_class_migration_is_recorded():
    """§2.1's one indispensable sentence, and it is checked in both directions.

    The law was born a **strain** at Layer 6 and is applied as **law in the
    ascension battery** at Layer 7, because `R8` clause 3 promoted `R7` clause
    3(a)'s ground into a general holding. An audit that looked only in `strain/`
    would find nothing at Layer 7 and conclude the law was dropped. So the
    catalog must say so — and the two facts it says must both be true: there IS
    a Layer-6 strain, and there is NO Layer-7 strain carrying it.
    """
    flat = _flat(_catalog())
    require("An audit that looks only in strain/ will conclude it was dropped" in flat,
            "CATALOG.md §2.1 no longer records the trial-class migration, which "
            "is the one thing about the denominator law a reader cannot "
            "reconstruct from the trial names")
    require("fourth species" in flat,
            "the catalog no longer names the denominator law as R8 clause 3's "
            "fourth species of gate clause")

    l6 = _read(os.path.join(TRIALS, "strain", "l6", "t_calibration_seam.py"))
    require("def trial_the_calibration_denominator_computes_exactly_under_any_abstention("
            in l6,
            "the Layer-6 strain the migration starts from no longer exists")
    l7dir = os.path.join(TRIALS, "strain", "l7")
    carried = [fn for fn in sorted(os.listdir(l7dir))
               if fn.startswith("t_") and "denominator" in _read(
                   os.path.join(l7dir, fn)).lower()
               and "def trial_the_calibration_denominator" in _read(
                   os.path.join(l7dir, fn))]
    require(not carried,
            "trials/strain/l7 now carries a denominator trial (%s); the catalog "
            "records that the law changed class and lives in the ascension "
            "battery at this layer" % (carried,))


def trial_the_novelty_horizon_is_stated_as_an_instrument_failure():
    """The category difference, which is the whole reason §2.2 is not an eighth sin."""
    flat = _flat(_catalog())
    require("It is a failure of an INSTRUMENT, and every one of the seven sins "
            "is a failure of an ENGINE" in flat,
            "CATALOG.md §2.2 no longer states the category difference; without "
            "it the novelty horizon reads as a defect of the engine, which is "
            "the opposite of what strain/l7 measures")
    require("Quoting it without saying which store it was measured against" in flat,
            "the citation rule the horizon forces is gone")


def trial_the_taxonomy_is_stated_as_adjacent_to_the_catalog_and_not_inside_it():
    """A humility axis and a strain catalog are two different kinds of claim.

    A strain is a way an engine WITH a capability fails at it; an
    `IMPOSSIBILITY.md` argues that an engine WITHOUT it cannot reach a ceiling.
    Folding the second into the first would make the taxonomy look like an
    eighth sin, and `§6` would have nowhere to point.
    """
    flat = _flat(_catalog())
    require("This is a humility axis and it is stated beside the strain "
            "catalog, not inside it" in flat,
            "CATALOG.md §3 no longer states that the taxonomy is adjacent to "
            "the catalog rather than a member of it")
    require("measured against make_engine(layer_cap = N-1)" in flat
            or "make_engine(layer_cap = N−1)" in _catalog(),
            "the catalog no longer says what the humility axis is measured "
            "against, which is what makes it a different claim")


def trial_the_catalog_states_what_a_competing_system_would_have_to_show():
    """§4 — the catalog is only worth publishing if somebody else can settle it."""
    flat = _flat(_catalog())
    require("What a competing system would have to show" in flat,
            "CATALOG.md dropped §4; a catalog with no falsification column is a "
            "list of things we happen to have measured")
    for axis in ("the seven-sin map", "the denominator law",
                 "the novelty horizon", "the four-kind taxonomy"):
        require(axis in flat, "§4 no longer names the axis %r" % (axis,))
    for commit in ("455306d", "3c0900a"):
        require(commit in flat,
                "§4 no longer pins its comparison to commit %s; an unpinned "
                "claim about somebody else's system is not a claim this "
                "repository makes" % (commit,))
