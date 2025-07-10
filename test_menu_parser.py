"""
Test for menu_parser.py
"""
import pytest
from menu_parser import get_menu_tree

def test_menu_tree_extraction(tmp_path):
    # Minimal valid _content.yml with menu items and children
    yml = tmp_path / "_content.yml"
    yml.write_text('''
site:
  title: "Test"
  author: "A"
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
    file: content/index.md
  - title: "Chapters"
    menu: true
    file: content/chapters.md
    children:
      - title: "Mechanics"
        file: content/1_mechanics/overview.md
        children:
          - title: "Activity"
            file: content/notebooks/1_mechanics/modeling/activity-what_is_a_model.ipynb
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
    menu = get_menu_tree(str(yml))
    assert isinstance(menu, list)
    assert len(menu) == 2
    assert menu[0]['title'] == "Home"
    assert menu[1]['title'] == "Chapters"
    assert 'children' in menu[1]
    assert menu[1]['children'][0]['title'] == "Mechanics"
    assert menu[1]['children'][0]['children'][0]['title'] == "Activity"
