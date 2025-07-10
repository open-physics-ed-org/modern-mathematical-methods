import nbformat
nb = nbformat.read("content/notebooks/3_waves/notes-waves_intro.ipynb", as_version=4)
print("Cells:", len(nb['cells']))
for i, cell in enumerate(nb['cells']):
    print(f"Cell {i+1}: type={cell['cell_type']}")
