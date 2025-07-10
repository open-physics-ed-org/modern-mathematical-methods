#!/bin/bash
# Test that .autogen/_menu.yml uses the correct titles from _content.yml
set -e
cd "$(dirname "$0")/.."
python3 scripts/test_menu_titles.py
