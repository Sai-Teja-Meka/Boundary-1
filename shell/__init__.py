"""shell/ — the impure rim (BOUNDARY.md §2.6).

`shell/` may import `core/`; `core/` may never import `shell/`. Everything the
constitution forbids inside the engine — file I/O, argument parsing, reading the
environment — lives on this side of the purity boundary.
"""
