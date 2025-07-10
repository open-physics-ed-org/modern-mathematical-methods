import nbformat, markdown
nb = nbformat.read("content/notebooks/3_waves/notes-waves_intro.ipynb", as_version=4)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        html = markdown.markdown(''.join(cell['source']))
        print(f"Cell {i+1} HTML:\n{html}\n{'-'*40}")
