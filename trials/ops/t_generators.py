"""ops/ — structural correctness of the clean base generators (chronicle, sessions).

Checks event shapes, referential integrity, and that payloads use only integers
and strings. The murk generator is validated separately (t_murk.py), since it
deliberately injects defects.
"""

from _harness import require
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen

_CHRONICLE_KINDS = {"spawn", "attr", "link", "move", "retire"}
_SESSION_KINDS = {"session_start", "msg", "tool", "session_end"}


def _only_ints_and_strings(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, int) or isinstance(value, str):
        return True
    if isinstance(value, list):
        return all(_only_ints_and_strings(v) for v in value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and _only_ints_and_strings(v)
                   for k, v in value.items())
    return False


def trial_chronicle_structure_and_refs():
    spawned = set()
    for ev in chronicle_gen.generate(1001, 3000):
        require(ev["kind"] in _CHRONICLE_KINDS, f"unknown chronicle kind: {ev}")
        k = ev["kind"]
        if k == "spawn":
            require(isinstance(ev["entity"], int) and isinstance(ev["class"], str),
                    f"bad spawn: {ev}")
            require(ev["entity"] not in spawned, f"entity id reused in clean base: {ev}")
            spawned.add(ev["entity"])
        elif k == "attr":
            require(ev["entity"] in spawned, f"attr references unspawned entity: {ev}")
            require(isinstance(ev["key"], str), f"bad attr key: {ev}")
            require(isinstance(ev["val"], (int, str)) and not isinstance(ev["val"], bool),
                    f"attr val must be int or str: {ev}")
        elif k == "link":
            require(ev["src"] in spawned and ev["dst"] in spawned,
                    f"link references unspawned entity: {ev}")
            require(ev["src"] != ev["dst"], f"link must relate distinct entities: {ev}")
        elif k == "move":
            require(ev["entity"] in spawned, f"move references unspawned entity: {ev}")
            require(isinstance(ev["loc"], str), f"bad move loc: {ev}")
        else:  # retire
            require(ev["entity"] in spawned, f"retire references unspawned entity: {ev}")


def trial_chronicle_payloads_ints_and_strings():
    for ev in chronicle_gen.generate(1001, 1500):
        require(_only_ints_and_strings(ev), f"chronicle payload has a bad type: {ev}")


def trial_sessions_structure_refs_and_turns():
    open_turns = {}   # sid -> running msg count
    for ev in sessions_gen.generate(2002, 3000):
        require(ev["kind"] in _SESSION_KINDS, f"unknown session kind: {ev}")
        k = ev["kind"]
        if k == "session_start":
            require(ev["sid"] not in open_turns, f"sid reopened while open: {ev}")
            require(isinstance(ev["user"], str), f"bad user: {ev}")
            open_turns[ev["sid"]] = 0
        elif k == "msg":
            require(ev["sid"] in open_turns, f"msg in a closed/unknown session: {ev}")
            require(ev["role"] in ("user", "agent"), f"bad role: {ev}")
            require(isinstance(ev["text_id"], int), f"bad text_id: {ev}")
            open_turns[ev["sid"]] += 1
        elif k == "tool":
            require(ev["sid"] in open_turns, f"tool in a closed/unknown session: {ev}")
            require(isinstance(ev["name"], str) and 0 <= ev["code"] <= 9,
                    f"bad tool event: {ev}")
        else:  # session_end
            require(ev["sid"] in open_turns, f"session_end without a start: {ev}")
            require(ev["turns"] == open_turns[ev["sid"]],
                    f"session_end turns mismatch: {ev} expected {open_turns[ev['sid']]}")
            del open_turns[ev["sid"]]


def trial_sessions_text_ids_are_unique_and_monotonic():
    last = 0
    for ev in sessions_gen.generate(2002, 3000):
        if ev["kind"] == "msg":
            require(ev["text_id"] == last + 1,
                    f"text_id not strictly monotonic: {ev['text_id']} after {last}")
            last = ev["text_id"]


def trial_scale_targets_match_doctrine():
    require(chronicle_gen.N == 50000, "chronicle scale target must be 50000 (§8.6)")
    require(sessions_gen.N == 5000, "sessions scale target must be 5000 (§8.6)")
