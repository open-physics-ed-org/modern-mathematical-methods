# Modern Mathematical Methods Course Site Refactor: Navigation, Head, and Footer

## Overview
This refactor modularizes and automates the generation of navigation, head, and footer HTML for the course site, using a strict YAML schema and templates. The goal is to ensure a single source of truth for all site structure and metadata, with robust validation and maintainable, DRY code.

---

## Progress Summary

### 1. Strict YAML Manifest (`_content.yml`)
- All navigation, site metadata, and footer content are now defined in `_content.yml`.
- The YAML schema is strictly validated for required fields and structure.
- The `footer:` section now holds the full HTML for the site footer, matching `index.html`.

### 2. Content and Menu Parsing
- **`content_parser.py`**
  - `load_and_validate_content_yml(path: str) -> dict`: Loads and validates `_content.yml`, raising errors for missing or malformed sections.
  - `validate_content(content: dict)`: Checks for required keys in `site`, `toc`, `footer`, `static`, and `build` sections.
  - `validate_menu_item(item: dict, level: int)`: Recursively validates menu structure and depth.
  - `get_menu_structure(content: dict) -> List[dict]`: Returns top-level menu items with `menu: true`.
  - `get_all_content_files(content: dict) -> List[str]`: Recursively collects all file paths from the TOC tree.
  - `get_group_page_info(content: dict, group_title: str) -> Optional[dict]`: Finds a group by title in the TOC.

- **`menu_parser.py`**
  - `get_menu_tree(yaml_path: str) -> List[dict]`: Loads and validates the YAML, returning the menu tree for HTML generation.

### 3. HTML Generation Scripts
- **`build_menu_html.py`**: Generates the full navigation menu HTML (with submenus) from YAML.
- **`build_top_menu_html.py`**: Generates only the top-level navigation menu HTML (no submenus), matching the nav bar in `index.html`.
- **`build_site_title_html.py`**: Generates the site title/logo block, including the subtitle (description), using values from YAML.
- **`build_footer_html.py`**: Generates the validated footer HTML from the YAML and the template in `static/templates/footer.html`.

### 4. Templates
- **`static/templates/head.html`**: Contains the `<head>` markup with placeholders for title and CSS paths. To be filled in by the build system per page.
- **`static/templates/footer.html`**: Contains the footer structure with a `{{ footer_text }}` placeholder, filled from YAML.

### 5. Tests
- **`test_content_parser.py`**: Pytest-based tests for YAML validation, menu extraction, and error handling.
- **`test_menu_parser.py`**: Tests for correct menu extraction from YAML.

---

## How the Functions Work

### content_parser.py
- **load_and_validate_content_yml(path: str) -> dict**
  - Loads `_content.yml` and validates all required sections.
  - Expands `.autogen` and `append_children` keys in the TOC.
  - Returns the validated content as a dictionary.

- **validate_content(content: dict)**
  - Checks for required keys in `site`, `toc`, `footer`, `static`, and `build`.
  - Validates types and presence of all required fields.
  - Raises `ContentValidationError` on any issue.

- **validate_menu_item(item: dict, level: int)**
  - Recursively checks each menu item for required fields and correct depth.

- **get_menu_structure(content: dict) -> List[dict]**
  - Returns a list of top-level menu items with `menu: true`.

- **get_all_content_files(content: dict) -> List[str]**
  - Recursively collects all file paths from the TOC tree.

- **get_group_page_info(content: dict, group_title: str) -> Optional[dict]**
  - Finds a group by title in the TOC and returns its dictionary.

### menu_parser.py
- **get_menu_tree(yaml_path: str) -> List[dict]**
  - Loads and validates the YAML, returning the menu tree for HTML generation.

### build_footer_html.py
- Loads and validates `_content.yml`.
- Reads `static/templates/footer.html`.
- Substitutes `{{ footer_text }}` with the value from `footer.text` in YAML.
- Prints the resulting HTML.

### build_site_title_html.py
- Loads and validates `_content.yml`.
- Extracts `site.title`, `site.logo`, and `site.description`.
- Generates the site title/logo HTML block, including the subtitle.

### build_menu_html.py / build_top_menu_html.py
- Use `menu_parser.get_menu_tree` to extract the menu structure.
- Generate HTML for the navigation menu, matching the classes and structure in `index.html`.

---


## July 2025: CLI Build Integration & HTML Output Testing

- Implemented `build-html.py --html --files ...` to build single or multiple HTML pages using modular, importable functions for YAML validation, menu/footer/title HTML, and Markdown conversion.
- All imports are now at the top of `build-html.py` for maintainability and testability.
- The build system now:
  - Loads and validates `_content.yml` for site config, menu, and footer.
  - Assembles the full HTML page from templates and YAML-driven content.
  - Writes output to `docs/`.
- Successfully tested building `index.html` from `content/index.md`.

### Issues Identified in Output Comparison (Legacy vs. New Build)
- Menu structure and order do not match legacy/expected output (legacy menu is flattened, new menu is strictly hierarchical).
- Theme toggle button missing in new build.
- Missing container and markdown-body wrappers around `<main>`.
- Header layout is different (row vs. column, subtitle present in new build).
- Menu classes/IDs are not fully matching legacy markup.
- Footer has extra `<p>` nesting in new build.


### Recently Completed (July 2025)
- Menu logic in build-html.py now includes all top-level YAML items as menu items, regardless of the `menu:` key, matching legacy and expected behavior.
- Debug mode (`--debug`) added to print menu extraction and structure for troubleshooting.
- Verified that Resources and About now appear in the top-level menu for all pages.

### Next Steps (July 2025)
1. Continue aligning other aspects of the output: theme toggle button, container/wrappers, header layout, and footer structure.
2. Add robust unit/integration tests for the build process.
3. Integrate the build process into CI and document usage.
4. Optionally, expand YAML/templates for more complex footers or per-page metadata.

---

**This refactor now supports modular, YAML-driven, and testable HTML builds. Output is being incrementally aligned with legacy/expected markup and styling.**
