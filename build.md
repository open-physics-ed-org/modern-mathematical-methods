# Build System and Script Reference

This document provides a detailed overview of the build system and all scripts in the Modern Mathematical Methods repository. It is intended for developers and maintainers who need to understand or extend the build process.

---

## Main Build Script: build.py

- **Purpose:** Central entry point for building all site outputs (HTML, LaTeX, PDF, DOCX, Markdown, Jupyter Book, etc.)
- **Usage:**
  - `python build.py --all` — Build all outputs in sequence
  - `python build.py --html` — Build HTML output
  - `python build.py --tex` — Build LaTeX output
  - `python build.py --pdf` — Build PDF output
  - `python build.py --docx` — Build DOCX output
  - `python build.py --md` — Build Markdown output
  - `python build.py --jupyter` — Build Jupyter Book output
  - `python build.py --ipynb` — Copy flat notebooks
  - `python build.py --files file1.md file2.ipynb` — Build only specified files
  - Add `--debug` to any command for verbose output
- **Key Functions:**
  - `build_tex_all(debug=False)`: Build LaTeX for all files in the content tree
  - `build_tex_for_files(files, debug=False)`: Build LaTeX for specified files
  - `build_html_all(debug=False)`: Build HTML for all files
  - `build_html_for_files(files, debug=False)`: Build HTML for specified files
  - `build_jupyter_for_files(debug=False)`: Orchestrate Jupyter Book build, kernel fixes, and validation
  - `copy_static_assets(debug=False)`: Copy CSS and images to output locations
  - `render_download_buttons(file_path)`: Generate HTML for download buttons for each file
  - `debug_print(msg, debug)`: Print debug messages if enabled

---

## Content and Menu Scripts

- **content_parser.py**
  - Loads and validates _content.yml (the main content tree)
  - Provides utilities to extract all referenced files
  - Used by build.py for content discovery

- **menu_parser.py**
  - Parses menu YAML files for navigation structure
  - Used for building navigation menus in HTML outputs

- **build_menu_html.py**
  - Generates HTML for the site navigation menu
  - Used by build.py to inject navigation into HTML pages

- **build_footer_html.py**
  - Renders the site footer from a template and config
  - Used by build.py for consistent footers

- **build_site_title_html.py**
  - (If present) Generates or manages the site title HTML

- **build_top_menu_html.py**
  - (If present) Generates the top-level menu HTML

---

## Notebook and Kernel Utilities

- **notebook_kernel_utils.py**
  - Functions for fixing and validating Jupyter notebook kernels
  - Used to ensure all notebooks have correct kernel metadata before building

- **fix_notebook_kernels.py**
  - Script to batch-fix kernels in all notebooks
  - Called by `build_jupyter_for_files` and can be run standalone

- **check_notebook_kernels.py**
  - Checks all notebooks for valid kernel metadata
  - Used for validation before Jupyter Book builds

---

## Content Conversion and Validation

- **convert_content_to_jb_flat.py**
  - Converts _content.yml to a flat _toc.yml for Jupyter Book
  - Ensures compatibility with Jupyter Book's requirements

- **validate_yaml.py**
  - Validates YAML files for syntax errors
  - Used to check _toc.yml and other YAML configs

- **validate_jb_toc.py**
  - Checks _toc.yml for duplicate entries and structure issues

- **check_toc_no_empty_chapters.py**
  - Ensures no empty chapters in the content tree

- **check_toc_parts_after_root.py**
  - Validates that all parts in the TOC come after the root

- **check_toc_root_file.py**
  - Ensures the TOC has a valid root file

---

## Notebook and Markdown Copy/Conversion

- **copy_ipynb_flat.py**
  - Copies all notebooks to a flat directory for easy access and conversion
  - Used for building flat IPYNB and DOCX outputs

- **convert_content_to_jupyterbook.py**
  - Converts content to Jupyter Book-compatible format (if needed)

---

## Asset and Utility Scripts

- **sanitize_unicode.py**
  - Cleans up unicode characters in content files

- **remove_remote_images.py**
  - Removes or replaces remote image links in markdown files

- **all_python_code.txt**
  - (Reference) May contain all code snippets for review or export

---

## Scripts Directory (scripts)

- **`basic_yaml2json.py`**
  - Converts YAML files to JSON for debugging or external use

- **`md2html.py`**
  - Converts markdown files to HTML (standalone)

- **`preprocess_content_yml.py`**
  - Preprocesses _content.yml for custom needs

- **`test_end_to_end_titles.py`**
  - End-to-end test for title extraction and build

- **`test_menu_titles.py`**
  - Tests menu title extraction

- **`test_preprocess_content_yml.py`**
  - Tests preprocessing of content YAML

- **`theme_to_css.py`**
  - Converts theme YAML files to CSS

- **`fetch_youtube.py`**
  - (If present) Fetches YouTube metadata or content for embedding

- **`debuggers/compare_yaml.py`**
  - Compares YAML files for differences

- **`debuggers/test_parse_content_yml.py`**
  - Tests parsing of content YAML files

---

## Templates and Static Assets

- **templates**
  - Contains HTML templates for page, header, footer, theme toggle, etc.
- **css**
  - CSS files for site styling
- **images**
  - Images used in site outputs

---

## Adding or Modifying Scripts

- Place new helper scripts in the scripts directory or root as appropriate.
- Document the purpose and usage of each script at the top of the file.
- Update this BUILD.md if you add new build-related scripts.

---

*For a high-level overview, see README.md. For implementation details, see comments in each script.*