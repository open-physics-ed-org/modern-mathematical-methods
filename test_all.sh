#!/bin/sh
set -e
python validate_yaml.py
python validate_jb_toc.py
python print_toc_tree.py
sh test_jb_build.sh
