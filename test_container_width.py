# Test if .container class constrains width in a minimal HTML+CSS example
html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Test Container Width</title>
  <style>
    .container {
      max-width: 900px;
      width: 100%;
      margin-left: auto;
      margin-right: auto;
      background: #eee;
      border: 2px solid #333;
      padding: 1em;
    }
    body { background: #ccc; }
  </style>
</head>
<body>
  <main class="site-main container">
    <h1>Test Content</h1>
    <p>This should be centered and no wider than 900px.</p>
    <div style="background: #faa; height: 40px;">Visual width test</div>
  </main>
</body>
</html>
'''

with open("test_container_width.html", "w") as f:
    f.write(html)

print("[OK] test_container_width.html written. Open it in a browser to verify max-width and centering.")
