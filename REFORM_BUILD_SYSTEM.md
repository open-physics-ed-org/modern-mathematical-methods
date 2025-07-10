# Refactoring the Build System: Unified Parsing and Schema Validation

## Overview

To make the course site generator robust, maintainable, and future-proof, we propose a refactor that combines two powerful ideas:

1. **Unify all YAML parsing and navigation logic in a shared Python library.**
2. **Enforce strict schema validation on `_content.yml` before any build step.**

This approach will ensure that all tools (build scripts, preprocessors, etc.) use a single, authoritative source for content structure, and that errors in the YAML are caught early and reported clearly.

---


## 1. Unified Parsing Logic in a Shared Library

- **Python module `content_parser.py`** now:
  - Loads and validates `_content.yml` using strict, recursive schema logic (see also `YAML_STRUCTURE_GUIDE.md`).
  - Enforces maximum navigation depth (menu > group > subgroup > page) with robust recursion and clear error reporting.
  - Provides functions to extract:
    - The menu structure (for navigation)
    - The list of all content files (for building)
    - Group/page lookup and other metadata
  - Includes debug output for troubleshooting recursion and schema issues.
- **All build scripts and preprocessors** must import and use this module for all YAML parsing and navigation logic.
- **Benefits:**
  - No code duplication: parsing logic is written once and reused everywhere.
  - Easy to update: changes to the YAML structure only require updates in one place.
  - Consistent behavior across all tools.
  - Early detection of navigation or schema errors, including excessive depth.

---


## 2. YAML Schema Validation

- **Schema is enforced in `content_parser.py`**:
  - Required fields (`title`, `file` for leaves, etc.)
  - Allowed structure (menu > group > subgroup > page, max depth, etc.)
  - No extra/unknown fields (future: add explicit check for unknown keys)
  - Correct types (lists, dicts, strings, booleans)
- **Validate `_content.yml`** at the start of every build. If invalid, print clear errors and abort.
- **Benefits:**
  - Early error detection: schema validation catches mistakes before the build runs.
  - Debug output available for troubleshooting recursion and structure issues.
# Recent Advancement (July 2025)

- The parser now includes debug output and has been tested to enforce maximum navigation depth strictly.
- Validation logic is robust for all top-level sections and recursive navigation.
- Test YAMLs (`good_content.yml`, `bad_content.yml`) and test scripts confirm correct and incorrect structures.

# Next Steps for Refactoring `build-web.py`

1. **Refactor `build-web.py` to use `content_parser.py`** for all content and navigation parsing:
   - Replace any direct YAML loading or ad-hoc parsing with calls to `load_and_validate_content_yml` and related functions.
   - Use `get_menu_structure`, `get_all_content_files`, and other helpers for navigation and file lists.
   - Remove any duplicate or legacy parsing logic.
2. **Add error handling**:
   - If validation fails, abort the build and print the error.
   - Optionally, add a command-line option to print debug output or validate only.
3. **(Optional) Add explicit unknown-key checks** in the parser for even stricter schema enforcement.
4. **Update documentation** to reflect the new workflow and developer onboarding.
  - Clear, actionable error messages for content authors.
  - Prevents subtle bugs and broken navigation.

---

## 3. Refactoring `build-web.py`

- **Replace all direct YAML parsing** with calls to the shared parser module.
- **On startup:**
  1. Load and validate `_content.yml` using the schema.
  2. Use the parser to extract:
     - Menu structure for navigation
     - List of all files to build (notebooks, markdown, etc.)
     - Any group/section/metadata info needed for templates
- **Build logic** (HTML, notebooks, etc.) uses these parsed structures, not hardcoded assumptions about YAML layout.
- **No need for `.autogen` files** unless you want to keep them for debugging or external tools.
- **Benefits:**
  - Cleaner, more maintainable code.
  - No repeated parsing logic, less risk of bugs.
  - Always up-to-date with the latest YAML structure.

---

## 4. Example Implementation Plan

1. **Write a schema** for `_content.yml` (YAML or Python dict).
2. **Implement `content_parser.py`** with functions like:
   - `validate_content_yml(path)`: Validates against the schema.
   - `get_menu_structure(content)`: Returns menu items for navigation.
   - `get_all_content_files(content)`: Returns all files to build.
   - `get_group_page_info(content, group_title)`: Returns info for group pages.
3. **Update `build-web.py`** to use these functions and structures.
4. **Test** with various valid and invalid YAML files to ensure robust error handling.

---

## 5. Example Usage in `build-web.py`

```python
from content_parser import (
    load_and_validate_content_yml,
    get_menu_structure,
    get_all_content_files,
    get_group_page_info,
)

content = load_and_validate_content_yml('_content.yml')  # raises on error
menu = get_menu_structure(content)
files_to_build = get_all_content_files(content)
# ...proceed with build using these structures...
```

---

## 6. Summary

- **Step 1:** Write a schema and a parser module for your YAML.
- **Step 2:** Refactor all build scripts to use this parser.
- **Step 3:** Validate YAML before every build.
- **Step 4:** Use the parsed, validated structures for all build logic.

This approach will make your build system robust, extensible, and easy to maintain as your course grows.
