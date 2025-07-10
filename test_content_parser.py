import pytest
from content_parser import load_and_validate_content_yml, get_menu_structure, get_all_content_files, get_group_page_info, ContentValidationError

def test_valid_content(tmp_path):
    yml = tmp_path / "_content.yml"
    yml.write_text('''
site:
  title: "Modern Mathematical Methods"
  author: "Danny Caballero"
  description: "A modern, open-source course in mathematical methods for physics and astrophysics."
  logo: "static/images/logo.png"
  favicon: "static/images/favicon.ico"
  theme:
    default: "dark"
    light: "light"
    dark: "dark"
  language: "en"
  github_url: "https://github.com/dannycab/modern-mathematical-methods"
toc:
  - title: "Home"
    menu: true
    file: content/index.md
  - title: "Chapters"
    menu: true
    file: content/chapters.md
    children:
      - title: "Mechanics"
        file: content/1_mechanics/overview.md
        children:
          - title: "Activity: What is a Model?"
            file: content/notebooks/1_mechanics/modeling/activity-what_is_a_model.ipynb
static:
  images:
    - path: "static/images/"
      description: "Site-wide images and figures"
  css:
    - path: "static/css/"
      description: "Custom CSS files"
  js:
    - path: "static/js/"
      description: "Custom JavaScript files"
  templates:
    - path: "static/templates/"
      description: "HTML templates"
  themes:
    - path: "static/themes/"
      description: "Theme files"
build:
  outputs:
    - "html"
    - "pdf"
    - "docx"
    - "md"
    - "tex"
  output_dir: "_build/"
  docs_dir: "docs/"
  sources_dir: "docs/sources/"
  notebooks_dir: "content/notebooks/"
  static_dir: "static/"
  images_dir: "static/images/"
''')
    content = load_and_validate_content_yml(str(yml))
    menu = get_menu_structure(content)
    files = get_all_content_files(content)
    group = get_group_page_info(content, "Mechanics")
    assert len(menu) == 2
    assert files == [
        "content/index.md",
        "content/chapters.md",
        "content/1_mechanics/overview.md",
        "content/notebooks/1_mechanics/modeling/activity-what_is_a_model.ipynb"
    ]
    assert group['title'] == "Mechanics"
    assert 'children' in group

def test_invalid_missing_file(tmp_path):
    yml = tmp_path / "_content.yml"
    yml.write_text('''
site:
  title: "Modern Mathematical Methods"
  author: "Danny Caballero"
  description: "desc"
  logo: "logo.png"
  favicon: "favicon.ico"
  theme:
    default: "dark"
    light: "light"
    dark: "dark"
  language: "en"
  github_url: "url"
toc:
  - title: "Home"
    menu: true
static:
  images: []
  css: []
  js: []
  templates: []
  themes: []
build:
  outputs: ["html"]
  output_dir: "_build/"
  docs_dir: "docs/"
  sources_dir: "docs/sources/"
  notebooks_dir: "content/notebooks/"
  static_dir: "static/"
  images_dir: "static/images/"
''')

    with pytest.raises(ContentValidationError):
        load_and_validate_content_yml(str(yml))


# Test for .autogen and append_children support
def test_autogen_and_append_children(tmp_path):
    import os
    from content_parser import _process_special_keys
    # Setup a temp directory with files
    section_dir = tmp_path / "notebooks" / "section"
    section_dir.mkdir(parents=True)
    # Create files to be autogen'd
    for fname in ["a.md", "b.md"]:
        (section_dir / fname).write_text(f"# {fname}")
    # YAML with .autogen and append_children
    toc = [
        {".autogen": "notebooks/section/*.md"},
        {"file": "notebooks/section/parent", "append_children": "notebooks/section"}
    ]
    # Use the temp dir as base_path
    result = _process_special_keys(toc, str(tmp_path))
    # .autogen expands to two files
    autogen_files = [e["file"] for e in result if "file" in e and e["file"].endswith(".md")]
    assert any(f.endswith("a.md") for f in autogen_files)
    assert any(f.endswith("b.md") for f in autogen_files)
    # append_children adds children to parent
    parent = [e for e in result if e.get("file", "").endswith("parent")][0]
    assert "children" in parent
    child_files = [c["file"] for c in parent["children"]]
    assert any(f.endswith("a.md") for f in child_files)
    assert any(f.endswith("b.md") for f in child_files)


# Test for .autogen and append_children support
def test_autogen_and_append_children(tmp_path):
    import os
    from content_parser import _process_special_keys
    # Setup a temp directory with files
    section_dir = tmp_path / "notebooks" / "section"
    section_dir.mkdir(parents=True)
    # Create files to be autogen'd
    for fname in ["a.md", "b.md"]:
        (section_dir / fname).write_text(f"# {fname}")
    # YAML with .autogen and append_children
    toc = [
        {".autogen": "notebooks/section/*.md"},
        {"file": "notebooks/section/parent", "append_children": "notebooks/section"}
    ]
    # Use the temp dir as base_path
    result = _process_special_keys(toc, str(tmp_path))
    # .autogen expands to two files
    autogen_files = [e["file"] for e in result if "file" in e and e["file"].endswith(".md")]
    assert any(f.endswith("a.md") for f in autogen_files)
    assert any(f.endswith("b.md") for f in autogen_files)
    # append_children adds children to parent
    parent = [e for e in result if e.get("file", "").endswith("parent")][0]
    assert "children" in parent
    child_files = [c["file"] for c in parent["children"]]
    assert any(f.endswith("a.md") for f in child_files)
    assert any(f.endswith("b.md") for f in child_files)

def test_autogen_and_append_children(tmp_path):
    import os
    from content_parser import _process_special_keys
    # Setup a temp directory with files
    section_dir = tmp_path / "notebooks" / "section"
    section_dir.mkdir(parents=True)
    # Create files to be autogen'd
    for fname in ["a.md", "b.md"]:
        (section_dir / fname).write_text(f"# {fname}")
    # YAML with .autogen and append_children
    toc = [
        {".autogen": "notebooks/section/*.md"},
        {"file": "notebooks/section/parent", "append_children": "notebooks/section"}
    ]
    # Use the temp dir as base_path
    result = _process_special_keys(toc, str(tmp_path))
    # .autogen expands to two files
    autogen_files = [e["file"] for e in result if "file" in e and e["file"].endswith(".md")]
    assert any(f.endswith("a.md") for f in autogen_files)
    assert any(f.endswith("b.md") for f in autogen_files)
    # append_children adds children to parent
    parent = [e for e in result if e.get("file", "").endswith("parent")][0]
    assert "children" in parent
    child_files = [c["file"] for c in parent["children"]]
    assert any(f.endswith("a.md") for f in child_files)
    assert any(f.endswith("b.md") for f in child_files)
