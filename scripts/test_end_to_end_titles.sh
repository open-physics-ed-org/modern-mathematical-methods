#!/bin/bash
# End-to-end test: edit _content.yml, run preprocessor, check menu titles
set -e
cd "$(dirname "$0")/.."

# 1. Backup _content.yml
cp _content.yml _content.yml.bak

# 2. Edit a title in _content.yml (mechanics, first file)
sed -i '' 's/title: "19 Sep 23 - The Duffing Oscillator"/title: "TEST_TITLE_UNIQUE_123"/' _content.yml

# 3. Run preprocessor and test
python3 scripts/test_preprocess_content_yml.py

# 4. Restore _content.yml
mv _content.yml.bak _content.yml
