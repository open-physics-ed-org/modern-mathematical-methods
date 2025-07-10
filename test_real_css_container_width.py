# Test if .container class from the real site CSS constrains width as expected
html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Test Real CSS Container Width</title>
  <link rel="stylesheet" href="static/css/theme-light.css">
  <style>
    body { background: #ccc; }
  </style>
</head>
<body>
  <main class="site-main container">
    <h1>Test Content</h1>
    <p>This should be centered and no wider than 900px (from your real CSS).</p>
    <div style="background: #faa; height: 40px;">Visual width test</div>
  </main>
</body>
</html>
'''

with open("test_real_css_container_width.html", "w") as f:
    f.write(html)

print("[OK] test_real_css_container_width.html written. Open it in a browser to verify max-width and centering with your real CSS.")
