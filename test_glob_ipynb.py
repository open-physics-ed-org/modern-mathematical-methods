from glob import glob

md_files = glob('content/**/*.md', recursive=True)
ipynb_files = glob('content/**/*.ipynb', recursive=True)

print("Markdown files found:")
for f in md_files:
    print("  ", f)

print("Notebook files found:")
for f in ipynb_files:
    print("  ", f)
