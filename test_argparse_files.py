import sys
from build_html import main

# Simulate CLI: build-html.py --html --files content/notebooks/3_waves/notes-waves_intro.ipynb --debug
sys.argv = [
    "build-html.py",
    "--html",
    "--files",
    "content/notebooks/3_waves/notes-waves_intro.ipynb",
    "--debug"
]
main()
