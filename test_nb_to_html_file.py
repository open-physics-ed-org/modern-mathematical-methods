import nbformat, markdown
nb = nbformat.read("content/notebooks/3_waves/notes-waves_intro.ipynb", as_version=4)
body = []
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        body.append(markdown.markdown(''.join(cell['source'])))
    elif cell['cell_type'] == 'code':
        body.append('<pre><code>{}</code></pre>'.format(''.join(cell['source'])))
with open("docs/test-notebook.html", "w") as f:
    f.write("<html><body>{}</body></html>".format('\n'.join(body)))
print("Wrote docs/test-notebook.html")
