"""ops/packaging — the transfer corpus `corpora/real-sessions/v1` (§8.8).

The first real-data corpus in the project. It has no generator, so the byte-match
law (§8.3) does not reach it and the **checksum-match** branch of
`laws/t_corpora_bytematch.py` binds it instead — a branch that has stood ready
with nothing to check since Layer 3 and is now live.

What this file adds beyond that law is everything the law cannot see:

  * that the corpus really is **fuel**, not a conversion of something else —
    every payload is byte-identical to `event.build_payload` applied to its own
    summary, so the transfer tier is grading the engine on the store's own
    events and not on a reshaped copy of them;
  * that the **scrub actually ran and still passes**, over the frozen bytes,
    every suite run — the difference between a scrub and a promise that someone
    looked once;
  * that the **manifest describes the file it ships with**, in every field a
    reader would rely on, so a manifest cannot drift away from its corpus;
  * that the **registry entry** exists and points at the same bytes, which is
    what makes the checksum law bind at all.

Nothing here gates a score. §8.8 admits the corpus; no ratified threshold binds
on it and none is invented — `packaging/README-public.md` states plainly that
the transfer tier is evidence about transfer and not a gate.
"""

import hashlib
import json
import os

from _harness import require, require_equal
from corpora import real_sessions, registry
from core.state import event_cost
from shell.dogfood import event as ev


def _bundle(version):
    return real_sessions.frozen_bytes(version), real_sessions.manifest(version)


def trial_every_frozen_version_is_present_and_hashes_to_its_manifest():
    require(len(real_sessions.VERSIONS) >= 1,
            "corpora/real_sessions.py declares no frozen version — the REAL "
            "family would be empty and the §8.8 branch vacuous again")
    for version in real_sessions.VERSIONS:
        data, manifest = _bundle(version)
        path = real_sessions.corpus_path(version)
        require(os.path.exists(path), "missing corpus file: %s" % (path,))
        require_equal(hashlib.sha256(data).hexdigest(), manifest["sha256"],
                      "%s: the frozen bytes do not hash to the manifest's "
                      "recorded checksum — §8.8 binds this corpus by that "
                      "number and it no longer describes the file" % (version,))
        require_equal(len(data), manifest["bytes"],
                      "%s: manifest byte count is stale" % (version,))


def trial_the_corpus_is_fuel_by_construction_not_by_conversion():
    """Every payload is exactly what the shell would build from its own summary.

    This is the claim the whole transfer tier rests on: the dogfood store's
    events are *already* in fuel format (`shell/dogfood/event.build_payload`),
    so freezing them is a copy. If it were a conversion, the transfer scores
    would be about the conversion.
    """
    for version in real_sessions.VERSIONS:
        payloads = real_sessions.payloads(version)
        require_equal(len(payloads), real_sessions.manifest(version)["events"],
                      "%s: manifest event count disagrees with the file" % (version,))
        for i, payload in enumerate(payloads):
            require_equal(sorted(payload.keys()), sorted(ev.PAYLOAD_KEYS),
                          "%s[%d]: not a session_summary payload" % (version, i))
            require_equal(payload["kind"], ev.KIND,
                          "%s[%d]: wrong kind" % (version, i))
            summary = ev.summary_of_payload(payload)
            require_equal(ev.build_payload(summary), payload,
                          "%s[%d]: the payload is NOT the canonical build of its "
                          "own summary — this corpus is a conversion, not a "
                          "snapshot, and every transfer score computed on it is "
                          "about the conversion" % (version, i))


def trial_the_corpus_is_canonical_jsonl_with_no_stray_bytes():
    """§2.4 canonical encoding, one event per line, exactly one trailing newline."""
    from corpora import canon
    for version in real_sessions.VERSIONS:
        data = real_sessions.frozen_bytes(version)
        require(data.endswith(b"\n"), "%s: corpus does not end with a newline" % (version,))
        require(b"\n\n" not in data, "%s: corpus contains a blank line" % (version,))
        payloads = real_sessions.payloads(version)
        require_equal(canon.encode_jsonl(payloads), data,
                      "%s: the corpus is not the canonical encoding of its own "
                      "events (§2.4) — a byte differs somewhere" % (version,))


def trial_the_scrub_still_finds_nothing_in_the_frozen_bytes():
    """The scrub is a trial, not a claim someone made once at freeze time."""
    for version in real_sessions.VERSIONS:
        data, manifest = _bundle(version)
        findings = real_sessions.scrub_report(data.decode("utf-8"))
        require_equal(findings, [],
                      "%s: the scrub found %d thing(s) in a FROZEN corpus: %s — "
                      "the corpus is frozen and never edited (§8.8, §9.2), so "
                      "this is a human's decision and not a session's"
                      % (version, len(findings),
                         ", ".join(sorted(set(f["family"] for f in findings)))))
        require_equal(manifest["scrub"]["findings"], findings,
                      "%s: the manifest's recorded scrub result disagrees with "
                      "re-running the scrub now" % (version,))
        require_equal(sorted(manifest["scrub"]["families"]),
                      sorted(family for family, _p, _w in real_sessions.SCRUB_PATTERNS),
                      "%s: the manifest records a different set of scrub families "
                      "than the scrub applies — a family added later would leave "
                      "the recorded pass describing a weaker check" % (version,))


def trial_the_manifest_describes_the_corpus_it_ships_with():
    for version in real_sessions.VERSIONS:
        manifest = real_sessions.manifest(version)
        payloads = real_sessions.payloads(version)
        require_equal(manifest["version"], version, "manifest version mismatch")
        require_equal(manifest["corpus"], real_sessions.CORPUS_DIRNAME,
                      "manifest corpus name mismatch")
        require_equal(manifest["raw_cells"], sum(event_cost(p) for p in payloads),
                      "%s: the manifest's raw episodic footprint is stale — the "
                      "Layer-4 transfer tier's budget cap is derived from it "
                      "(R4 clause 2)" % (version,))
        require("§8.8" in manifest["rule"],
                "%s: the manifest no longer names the rule that admits it" % (version,))
        source = manifest["source"]
        for field in ("store", "store_sha256", "store_state_checksum",
                      "store_next_t", "frozen_at_commit"):
            require(field in source and source[field] not in (None, ""),
                    "%s: the manifest does not record `%s` — a snapshot whose "
                    "provenance is not recorded is not a snapshot of anything"
                    % (version, field))
        require_equal(source["store_next_t"], len(payloads),
                      "%s: the manifest says the store held %d events at the "
                      "freeze but the corpus carries %d"
                      % (version, source["store_next_t"], len(payloads)))


def trial_the_registry_binds_every_version_to_the_checksum_law():
    """Without this, `laws/t_corpora_bytematch.py` would pass over the corpus."""
    entries = {entry["name"]: entry for entry in registry.REAL}
    for version in real_sessions.VERSIONS:
        name = "%s/%s" % (real_sessions.CORPUS_DIRNAME, version)
        require(name in entries,
                "corpora/registry.py::REAL does not carry %s — the §8.8 "
                "checksum law would silently skip it" % (name,))
        entry = entries[name]
        require_equal(os.path.abspath(entry["path"]),
                      os.path.abspath(real_sessions.corpus_path(version)),
                      "%s: the registry points at a different file" % (name,))
        require_equal(entry["sha256"], real_sessions.manifest(version)["sha256"],
                      "%s: the registry's checksum is not the manifest's" % (name,))
    require(len(registry.REAL) == len(real_sessions.VERSIONS),
            "corpora/registry.py::REAL holds %d entries for %d frozen versions"
            % (len(registry.REAL), len(real_sessions.VERSIONS)))


def trial_the_corpus_directory_holds_data_and_documentation_only():
    """No `.py` under the hyphenated tree: it is data, and it is not importable."""
    for version in real_sessions.VERSIONS:
        directory = real_sessions.version_dir(version)
        names = sorted(os.listdir(directory))
        require(not any(n.endswith(".py") for n in names),
                "%s: a Python file lives inside the corpus tree; the loader "
                "belongs in corpora/real_sessions.py (the directory name is "
                "hyphenated and cannot be a package)" % (version,))
        require("README.md" in names,
                "%s: a frozen real-data corpus ships its README" % (version,))
        require(real_sessions.MANIFEST_FILENAME in names,
                "%s: §8.8 requires a checksum manifest" % (version,))


def trial_the_manifest_is_itself_canonical_json():
    """A manifest a human hand-edited would be the easiest thing to get wrong."""
    for version in real_sessions.VERSIONS:
        with open(real_sessions.manifest_path(version), "r", encoding="utf-8") as fh:
            text = fh.read()
        doc = json.loads(text)
        require(isinstance(doc, dict), "%s: manifest is not an object" % (version,))
        require_equal(text, json.dumps(doc, indent=2, sort_keys=True,
                                       ensure_ascii=False) + "\n",
                      "%s: the manifest is not the canonical rendering of its own "
                      "content — re-emit it rather than hand-editing" % (version,))
