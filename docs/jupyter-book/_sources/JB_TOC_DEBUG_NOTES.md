# Jupyter Book TOC Conversion & Build Debugging Notes

## Summary
We are attempting to convert a custom `_content.yml` (with a nested menu structure) into Jupyter Book's `_config.yml` and `_toc.yml` using the script `convert_content_to_jupyterbook.py`. The goal is to produce a Jupyter Book that builds cleanly and preserves the intended menu structure.

## What We Tried
- **Scripted conversion** from `_content.yml` to `_toc.yml` and `_config.yml`.
- **Automated tests** for:
  - YAML syntax validity (`validate_yaml.py`)
  - Duplicate file detection in TOC (`validate_jb_toc.py`)
  - Visual tree print of TOC structure (`print_toc_tree.py`)
  - Jupyter Book build smoke test (`test_jb_build.sh`)
  - All-in-one test runner (`test_all.sh`)
- **Iterative script fixes** to:
  - Remove duplicate root file entries
  - Ensure the root file is the first chapter
  - Only use `part` for grouping, and only after the root file
  - Flatten or nest as required by Jupyter Book's TOC schema
- **Manual inspection** of generated `_toc.yml` and error messages from Jupyter Book

## Problems Remaining
- **Jupyter Book build still fails** with:
  - `entry does not contain one of {'file', 'glob', 'url'} @ '/chapters/0'`
- **Root-level TOC structure**: Jupyter Book expects the first entry in `chapters` to be a `file` (the home/index page), followed by `part` entries. Our script attempts to do this, but the build still fails, possibly due to subtle schema or ordering issues.
- **Ambiguity in Jupyter Book TOC schema**: The documentation and error messages are not always clear about the allowed combinations of `file`, `part`, and `chapters` at each level, making it difficult to automate conversion robustly.
- **No clear feedback** from Jupyter Book about exactly which structure is accepted, beyond the error message.

## What We Know Works
- The YAML is valid and the TOC tree matches the intended structure.
- There are no duplicate file entries in the TOC.
- The root file is not repeated in the chapters list.

## What We Could Try Next
- **Manually craft a minimal working `_toc.yml`** for Jupyter Book and compare it to the generated one.
- **Incrementally add parts/chapters** to a working TOC to see where the build fails.
- **Consult Jupyter Book source/tests** for canonical TOC examples.
- **Try the `jupyter-book toc migrate` tool** as suggested in the error message.
- **Ask the Jupyter Book community** for clarification on the expected TOC schema for complex nested menus.

## Scripts Created
- `convert_content_to_jupyterbook.py` — main conversion script
- `validate_yaml.py` — YAML syntax check
- `validate_jb_toc.py` — duplicate file check
- `print_toc_tree.py` — visual TOC tree
- `test_jb_build.sh` — build smoke test
- `test_all.sh` — run all tests

---

**Status:**
- Conversion and validation scripts are in place and working.
- Jupyter Book build still fails due to TOC schema issues.
- Further debugging or schema clarification is needed.

*Leaving this note for future reference. Good night!*
