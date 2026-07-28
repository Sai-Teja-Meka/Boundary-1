"""corpora/real_sessions.py — the loader and the scrub for the REAL corpus family.

`BOUNDARY.md §8.8` (the real-data rule) admits one kind of corpus that no
generator produces:

> *"A frozen, checksummed snapshot of real data is a **legal corpus**. It has no
> generator, so it is **exempt from the byte-match law**; instead it is bound by
> its recorded **SHA-256 checksum** (a checksum-match law replaces byte-match for
> real-data corpora). A real-data corpus ships a checksum manifest and is never
> edited."*

`corpora/real-sessions/` is the first one. It is a frozen snapshot of this
project's own accumulated dogfood store (`shell/dogfood/store/store.json`) —
the session summaries the project has written about itself, which are **already
in fuel format by construction**: the shell builds every one of them through
`shell/dogfood/event.build_payload`, so a snapshot is a copy, never a
conversion. `payloads_are_canonical_builds` asserts exactly that, per version.

## Why this module's name has an underscore and the directory has a hyphen

The corpus directory is `corpora/real-sessions/`, following the corpus naming
convention every other corpus uses in its file names. A hyphenated directory is
not an importable Python package, so the loader lives here, beside the corpora
package rather than inside the corpus, and reaches the tree by path. The data
directory holds no `.py` file at all — it is data, a manifest and a README.

## Versioning: `v1`, and why later PACKAGE moves re-freeze rather than re-write

The store grows every session, so any snapshot of it is a snapshot *as of* a
moment. §9.2 forbids editing a frozen artifact, so a later, larger snapshot is a
**new version directory** (`v2/`) with its own manifest and its own checksum;
`v1` keeps its bytes and its checksum forever. `VERSIONS` below is the ordered
list of what has been frozen; `LATEST` is the last of them.

## The scrub (`scrub_report`)

§8.8 says a real-data corpus is frozen and checksummed. It does not say what may
be *in* it, and this corpus is the first fuel in the project that a human wrote
in prose rather than a seeded generator emitting from a closed vocabulary. So
the freeze runs a scrub, and the scrub is a **trial** rather than a one-time
claim: `trials/ops/packaging/t_real_sessions.py` re-runs it over the frozen
bytes on every suite run, so a later version cannot be frozen with a secret in
it and a promise that somebody looked.

The families are declared in `SCRUB_PATTERNS`. They are the ones that would
matter for a corpus that travels: an address that identifies a person, a URL
that leaks an internal host, an absolute path from the machine that wrote it, a
credential-shaped token, a bare IP. The scrub **reports**; it never edits — a
finding stops the freeze and a human decides, which is the same discipline §9
applies to everything else here.
"""

import hashlib
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))

CORPUS_DIRNAME = "real-sessions"
CORPUS_ROOT = os.path.join(_HERE, CORPUS_DIRNAME)

VERSIONS = ("v1",)
LATEST = VERSIONS[-1]

MANIFEST_FILENAME = "MANIFEST.json"


# ---- the scrub -------------------------------------------------------------
#
# Deterministic, library-light, and stated as data so a reader can audit the
# whole scrub without reading code. Each entry is (family, pattern, why).

SCRUB_PATTERNS = (
    ("email",
     r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
     "an address identifies a person; a corpus that travels must not carry one"),
    ("url",
     r"https?://\S+",
     "a URL can name an internal host or a private artifact"),
    ("absolute_path",
     r"(?<![\w/])/(?:home|Users|root|tmp|var|etc|mnt|opt)/\S*",
     "an absolute path leaks the machine the session ran on; repo-relative "
     "paths are what the summaries are supposed to carry"),
    ("windows_path",
     r"[A-Za-z]:\\\\",
     "the same leak in the other shell"),
    ("credential",
     r"\b(?:sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}"
     r"|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}"
     r"|AKIA[0-9A-Z]{16})\b",
     "credential-shaped tokens, by their published prefixes"),
    ("long_hex",
     r"\b[0-9a-f]{32,}\b",
     "a 32+ hex run is a checksum, a key or a full commit sha; none of the "
     "three belongs in prose a corpus carries"),
    ("ipv4",
     r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
     "a bare address is either an internal host or noise"),
)


def scrub_report(text):
    """Every scrub finding in `text`, as an ordered list of dicts.

    Pure and read-only: it returns what it found and changes nothing. An empty
    list is the only result that lets a freeze proceed, and *that it was run* is
    recorded in the version's README whether or not it found anything.
    """
    findings = []
    for family, pattern, why in SCRUB_PATTERNS:
        for match in sorted(set(re.findall(pattern, text))):
            findings.append({"family": family, "match": match, "why": why})
    return findings


# ---- paths, manifests, payloads --------------------------------------------

def version_dir(version=LATEST):
    return os.path.join(CORPUS_ROOT, version)


def manifest_path(version=LATEST):
    return os.path.join(version_dir(version), MANIFEST_FILENAME)


def manifest(version=LATEST):
    """The version's checksum manifest (§8.8's 'ships a checksum manifest')."""
    with open(manifest_path(version), "r", encoding="utf-8") as fh:
        return json.load(fh)


def corpus_path(version=LATEST):
    return os.path.join(version_dir(version), manifest(version)["file"])


def frozen_bytes(version=LATEST):
    with open(corpus_path(version), "rb") as fh:
        return fh.read()


def sha256(version=LATEST):
    return hashlib.sha256(frozen_bytes(version)).hexdigest()


def payloads(version=LATEST):
    """The corpus as a list of event payloads — the fuel, in ingestion order."""
    text = frozen_bytes(version).decode("utf-8")
    return [json.loads(line) for line in text.split("\n") if line]


def real_entries():
    """Every frozen version as a `registry.REAL` entry (name / path / sha256).

    The checksum comes from the **manifest**, never from the file: the law trial
    hashes the file and compares it to this, so reading the recorded number out
    of the file it is supposed to bind would make the law vacuous.
    """
    entries = []
    for version in VERSIONS:
        m = manifest(version)
        entries.append({
            "name": "%s/%s" % (CORPUS_DIRNAME, version),
            "path": os.path.join(version_dir(version), m["file"]),
            "sha256": m["sha256"],
        })
    return entries
