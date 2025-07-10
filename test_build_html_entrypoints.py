# test_build_html_entrypoints.py

from glob import glob
from build_html import build_html_for_files

def build_all():
    md_files = glob('content/**/*.md', recursive=True)
    ipynb_files = glob('content/**/*.ipynb', recursive=True)
    all_files = md_files + ipynb_files
    print(f"[TEST] Building all {len(all_files)} files...")
    build_html_for_files(all_files, debug=True)

def build_one(file_path):
    print(f"[TEST] Building single file: {file_path}")
    build_html_for_files([file_path], debug=True)

if __name__ == "__main__":
    # Example: build all
    build_all()
    # Example: build a single notebook
    build_one('content/notebooks/3_waves/notes-waves_intro.ipynb')
    # Example: build a single markdown file
    build_one('content/about.md')
