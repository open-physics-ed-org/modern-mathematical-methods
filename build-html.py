#!/usr/bin/env python3
print("[DEBUG] build-html.py script is executing!")
"""
build-html.py

Skeleton script for building site outputs with flexible CLI flags.
Supports: --html, --md, --docx, --tex, --pdf, --jupyter, --ppt, and --files FILE1 FILE2 ...

No build logic yet—just argument parsing and structure.
"""
import argparse
import sys


# --- Move build_html_all and build_html_for_files above main() ---


def build_html_all(debug=False):
    """Build HTML for all markdown and notebook files in content/ using top-level menu only."""
    from glob import glob
    md_files = glob('content/**/*.md', recursive=True)
    ipynb_files = glob('content/**/*.ipynb', recursive=True)
    all_files = md_files + ipynb_files
    if not all_files:
        print("[WARN] No markdown or notebook files found in content/.")
        return
    print(f"[INFO] Found {len(md_files)} markdown and {len(ipynb_files)} notebook files.")
    build_html_for_files(all_files, debug=debug)

from pathlib import Path
import os
import sys
try:
    import markdown
except ImportError:
    print("[ERROR] The 'markdown' package is required. Install with: pip install markdown", file=sys.stderr)
    sys.exit(1)
from content_parser import load_and_validate_content_yml
from build_menu_html import build_menu_ul
from build_footer_html import render_footer
from menu_parser import get_menu_tree

def build_html_for_files(files, debug=False):
    print("[DEBUG] build_html_for_files() is running!")
    """
    Build HTML for specified markdown and notebook files using YAML-driven templates and navigation.
    debug: if True, print debug output for menu and notebook processing.
    """
    # Load site config and menu
    content = load_and_validate_content_yml('_content.yml')
    site = content['site']
    try:
        menu = get_menu_tree('_content.yml')
        if isinstance(menu, dict) and 'toc' in menu:
            menu = menu['toc']
    except Exception as e:
        print(f"[ERROR] Could not load menu: {e}")
        menu = []

    def file_to_html_link(file_path, title):
        base, ext = os.path.splitext(os.path.basename(file_path))
        return f'<a href="{base}.html">{title}</a>'

    def first_child_file(node):
        if 'children' in node:
            for child in node['children']:
                if isinstance(child, dict):
                    if 'file' in child:
                        return child['file']
                    result = first_child_file(child)
                    if result:
                        return result
        return None

    def top_level_menu_items(menu):
        items = []
        if isinstance(menu, list):
            for node in menu:
                if not isinstance(node, dict):
                    continue
                title = node.get('title')
                file = node.get('file')
                if not file:
                    file = first_child_file(node)
                if title and (file or node.get('children')):
                    items.append((file, title))
        return items

    top_menu = top_level_menu_items(menu)

    menu_html = ['<ul class="site-nav-menu" id="site-nav-menu">']
    for file, title in top_menu:
        menu_html.append('<li>')
        menu_html.append(file_to_html_link(file, title))
        menu_html.append('</li>')
    menu_html.append('</ul>')
    menu_html = ''.join(menu_html)

    footer_text = content.get('footer', {}).get('text', '')
    footer_html = render_footer(footer_text)

    logo = site['logo']
    title = site['title']
    description = site.get('description', '')
    logo_web = './' + logo[len('static/'):] if logo.startswith('static/') else logo
    header_html = f'''
  <header class="site-header" style="display: flex; flex-direction: column; align-items: center; gap: 0.7em;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 1.2em; width: 100%;">
      <img src="{logo_web}" alt="Site logo" class="site-logo" style="height: 80px; width: 80px; border-radius: 18px; object-fit: cover;" />
      <div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">
        <h1 class="site-title" style="margin: 0; text-align: center; font-size: 3em; font-weight: 800; letter-spacing: -1.5px;">{title}</h1>
        <div class="site-subtitle" style="margin: 0; text-align: center; font-size: 1.2em; font-weight: 400; color: #666; max-width: 32em;">{description}</div>
      </div>
    </div>
  </header>
    '''

    # Theme toggle button (inserted after header)
    theme_toggle_html = '''
  <div class="theme-toggle-container" style="display: flex; justify-content: flex-end; width: 100%; margin: 0.5em 0 0.5em 0;">
    <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" style="padding: 0.4em 1.2em; font-size: 1em; border-radius: 1.2em; border: 1px solid #bbb; background: var(--theme-toggle-bg, #f8f8f8); cursor: pointer;">
      <span id="theme-toggle-icon" aria-hidden="true">🌙</span> <span id="theme-toggle-label">Dark</span>
    </button>
  </div>
  <script>
    const btn = document.getElementById('theme-toggle');
    const icon = document.getElementById('theme-toggle-icon');
    const label = document.getElementById('theme-toggle-label');
    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      if (theme === 'dark') {
        icon.textContent = '☀️';
        label.textContent = 'Light';
      } else {
        icon.textContent = '🌙';
        label.textContent = 'Dark';
      }
      localStorage.setItem('theme', theme);
    }
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
    const saved = localStorage.getItem('theme');
    if (saved) setTheme(saved);
  </script>
    '''

    head_path = os.path.join('static', 'templates', 'head.html')
    with open(head_path, 'r') as f:
        head_template = f.read()
    css_light = 'css/theme-light.css'
    css_dark = 'css/theme-dark.css'

    import nbformat
    import base64
    print(f"[DEBUG] build_html_for_files called with {len(files)} files:")
    for f in files:
        print(f"  - {f}")
    print("[DEBUG] Starting main file processing loop...")
    missing_files = []
    for file in files:
        print(f"[DEBUG] ---\n[DEBUG] Processing file: {file}")
        file_path = Path(file)
        if debug:
            print(f"[DEBUG] Starting processing for: {file}")
        if not file_path.exists():
            print(f"[ERROR] File not found: {file}")
            missing_files.append(file)
            continue
        ext = file_path.suffix.lower()
        print(f"[DEBUG] File extension: {ext}")
        try:
            if ext == '.md':
                print(f"[DEBUG] Reading markdown file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                print(f"[DEBUG] Rendering markdown to HTML...")
                body_html = markdown.markdown(md_content, extensions=['extra', 'toc', 'tables'])
            elif ext == '.ipynb':
                print(f"[DEBUG] Reading notebook file: {file_path}")
                try:
                    nb = nbformat.read(str(file_path), as_version=4)
                except Exception as e:
                    print(f"[ERROR] Could not read notebook: {file_path}: {e}")
                    continue
                print(f"[DEBUG] Notebook loaded. Keys: {list(nb.keys())}")
                if not nb.get('cells'):
                    print(f"[WARN] Notebook {file_path} has no cells.")
                    continue
                print(f"[DEBUG] Notebook {file_path} has {len(nb['cells'])} cells.")
                body_html = []
                for idx, cell in enumerate(nb.get('cells', [])):
                    print(f"[DEBUG] Processing cell {idx+1} of type {cell.get('cell_type')}")
                    cell_type = cell.get('cell_type')
                    lang = cell.get('metadata', {}).get('language', 'python' if cell_type == 'code' else 'markdown')
                    if debug:
                        print(f"[DEBUG] Cell {idx}: type={cell_type}, lang={lang}")
                    if cell_type == 'markdown':
                        import markdown as mdmod
                        try:
                            print(f"[DEBUG] Rendering markdown cell {idx+1}")
                            cell_html = mdmod.markdown(''.join(cell.get('source', [])), extensions=['extra', 'toc', 'tables'])
                            body_html.append(f'<div class="notebook-markdown-cell">{cell_html}</div>')
                        except Exception as e:
                            print(f"[ERROR] Failed to render markdown cell {idx+1} in {file_path}: {e}")
                    elif cell_type == 'code':
                        print(f"[DEBUG] Rendering code cell {idx+1}")
                        code = ''.join(cell.get('source', []))
                        code_html = f'<pre class="notebook-code-cell"><code>{code}</code></pre>'
                        outputs_html = []
                        for oidx, output in enumerate(cell.get('outputs', [])):
                            otype = output.get('output_type')
                            print(f"[DEBUG]   Output {oidx+1}: type={otype}")
                            try:
                                if otype == 'stream':
                                    text = ''.join(output.get('text', []))
                                    outputs_html.append(f'<div class="notebook-output-stream">{text}</div>')
                                elif otype == 'execute_result' or otype == 'display_data':
                                    data = output.get('data', {})
                                    if 'text/plain' in data:
                                        outputs_html.append(f'<div class="notebook-output-text">{data["text/plain"]}</div>')
                                    if 'image/png' in data:
                                        img_data = data['image/png']
                                        outputs_html.append(f'<img class="notebook-output-img" src="data:image/png;base64,{img_data}" />')
                                    if 'image/jpeg' in data:
                                        img_data = data['image/jpeg']
                                        outputs_html.append(f'<img class="notebook-output-img" src="data:image/jpeg;base64,{img_data}" />')
                                    if 'text/html' in data:
                                        outputs_html.append(f'<div class="notebook-output-html">{data["text/html"]}</div>')
                                elif otype == 'error':
                                    ename = output.get('ename', '')
                                    evalue = output.get('evalue', '')
                                    traceback = output.get('traceback', [])
                                    tb_html = '<br>'.join(traceback)
                                    outputs_html.append(f'<div class="notebook-output-error"><b>{ename}: {evalue}</b><br>{tb_html}</div>')
                            except Exception as e:
                                print(f"[ERROR] Failed to render output {oidx+1} in code cell {idx+1} in {file_path}: {e}")
                        cell_block = code_html + ''.join(outputs_html)
                        body_html.append(f'<div class="notebook-code-cell-block">{cell_block}</div>')
                body_html = '\n'.join(body_html)
            else:
                print(f"[SKIP] Unsupported file type: {file}")
                continue
            if not body_html:
                print(f"[WARN] No content generated for {file_path}, skipping HTML output.")
                continue
            page_title = title
            head_html = head_template.replace('{{ title }}', page_title).replace('{{ css_light }}', css_light).replace('{{ css_dark }}', css_dark)
            full_html = f'''<!DOCTYPE html>\n<html lang="{site.get('language', 'en')}">\n{head_html}\n<body>\n  {header_html}\n  <nav class="site-nav" id="site-nav" aria-label="Main navigation">{menu_html}</nav>\n  <main class="site-main container">\n    {theme_toggle_html}\n    {body_html}\n  </main>\n  <footer>\n    {footer_html}\n  </footer>\n</body>\n</html>\n'''
            out_dir = Path('docs')
            out_dir.mkdir(exist_ok=True)
            out_name = file_path.stem + '.html'
            out_path = out_dir / out_name
            try:
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                print(f"[OK] Built {out_path} from {file}")
            except Exception as e:
                print(f"[ERROR] Failed to write HTML file {out_path}: {e}")
        except Exception as e:
            print(f"[FATAL] Unexpected error processing {file}: {e}")
    if missing_files:
        print(f"[SUMMARY] {len(missing_files)} file(s) were missing and not processed:")
        for mf in missing_files:
            print(f"  - {mf}")
        # Always output a valid HTML page with .container for any fallback or summary
        # (This block is only for summary, not for outputting a page, so no fallback HTML is written here)

def main():
    print("[DEBUG] main() is running!")
    parser = argparse.ArgumentParser(description="Build site outputs from content.")
    parser.add_argument('--html', action='store_true', help='Build HTML output')
    parser.add_argument('--md', action='store_true', help='Build Markdown output')
    parser.add_argument('--docx', action='store_true', help='Build DOCX output')
    parser.add_argument('--tex', action='store_true', help='Build LaTeX output')
    parser.add_argument('--pdf', action='store_true', help='Build PDF output')
    parser.add_argument('--jupyter', action='store_true', help='Build Jupyter Notebook output')
    parser.add_argument('--ppt', action='store_true', help='Build PowerPoint output')
    parser.add_argument('--files', nargs='+', help='Only build the specified files')
    parser.add_argument('--debug', action='store_true', help='Print debug information about menu extraction')
    args = parser.parse_args()

    # Print parsed arguments for now
    print("[INFO] Build flags:")
    print(f"  HTML:    {args.html}")
    print(f"  Markdown:{args.md}")
    print(f"  DOCX:    {args.docx}")
    print(f"  LaTeX:   {args.tex}")
    print(f"  PDF:     {args.pdf}")
    print(f"  Jupyter: {args.jupyter}")
    print(f"  PPT:     {args.ppt}")
    print(f"  Files:   {args.files}")

    # HTML build skeleton
    if args.html:
        print("[INFO] HTML build selected.")
        if args.files:
            print(f"[INFO] Building HTML for specified files: {args.files}")
            build_html_for_files(args.files, debug=args.debug)
        else:
            print("[INFO] Building HTML for all content.")
            build_html_all(debug=args.debug)

    # Placeholders for other formats (to be implemented)
    if args.md:
        print("[TODO] Markdown build not yet implemented.")
    if args.docx:
        print("[TODO] DOCX build not yet implemented.")
    if args.tex:
        print("[TODO] LaTeX build not yet implemented.")
    if args.pdf:
        print("[TODO] PDF build not yet implemented.")
    if args.jupyter:
        print("[TODO] Jupyter build not yet implemented.")
    if args.ppt:
        print("[TODO] PowerPoint build not yet implemented.")

if __name__ == "__main__":
    main()



from pathlib import Path
import os
import sys
try:
    import markdown
except ImportError:
    print("[ERROR] The 'markdown' package is required. Install with: pip install markdown", file=sys.stderr)
    sys.exit(1)
from content_parser import load_and_validate_content_yml
from build_menu_html import build_menu_ul
from build_footer_html import render_footer
from menu_parser import get_menu_tree

def build_html_for_files(files, debug=False):
    print("[DEBUG] build_html_for_files() is running!")
    """
    Build HTML for specified markdown files using YAML-driven templates and navigation.
    debug: if True, print debug output for menu and notebook processing.
    """
    # Load site config and menu
    content = load_and_validate_content_yml('_content.yml')
    site = content['site']
    # Use only top-level menu items (no submenus) to match legacy output
    import sys
    try:
        menu = get_menu_tree('_content.yml')
        if isinstance(menu, dict) and 'toc' in menu:
            menu = menu['toc']
    except Exception as e:
        print(f"[ERROR] Could not load menu: {e}")
        menu = []

    # Debug print for menu structure
    if debug:
        import pprint
        print("[DEBUG] Raw menu structure from get_menu_tree:")
        pprint.pprint(menu)
    print("[DEBUG] Entered build_html_for_files main logic.")
    def file_to_html_link(file_path, title):
        base, ext = os.path.splitext(os.path.basename(file_path))
        return f'<a href="{base}.html">{title}</a>'

    def first_child_file(node):
        # Recursively find the first file in children
        if 'children' in node:
            for child in node['children']:
                if isinstance(child, dict):
                    if 'file' in child:
                        return child['file']
                    result = first_child_file(child)
                    if result:
                        return result
        return None

    def top_level_menu_items(menu):
        items = []
        if isinstance(menu, list):
            for node in menu:
                if not isinstance(node, dict):
                    continue
                title = node.get('title')
                file = node.get('file')
                # Accept any top-level menu item with a title and file or children
                if not file:
                    file = first_child_file(node)
                if title and (file or node.get('children')):
                    # Use file if present, else first child file
                    items.append((file, title))
        return items

    top_menu = top_level_menu_items(menu)

    if debug:
        print("[DEBUG] Top-level menu items extracted:")
        for file, title in top_menu:
            print(f"  - {title}: {file}")

    menu_html = ['<ul class="site-nav-menu" id="site-nav-menu">']
    for file, title in top_menu:
        menu_html.append('<li>')
        menu_html.append(file_to_html_link(file, title))
        menu_html.append('</li>')
    menu_html.append('</ul>')
    menu_html = ''.join(menu_html)

    # Build footer
    footer_text = content.get('footer', {}).get('text', '')
    footer_html = render_footer(footer_text)

    # Build site title/header
    logo = site['logo']
    title = site['title']
    description = site.get('description', '')
    logo_web = './' + logo[len('static/'):] if logo.startswith('static/') else logo
    header_html = f'''
  <header class="site-header" style="display: flex; flex-direction: column; align-items: center; gap: 0.7em;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 1.2em; width: 100%;">
      <img src="{logo_web}" alt="Site logo" class="site-logo" style="height: 80px; width: 80px; border-radius: 18px; object-fit: cover;" />
      <div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">
        <h1 class="site-title" style="margin: 0; text-align: center; font-size: 3em; font-weight: 800; letter-spacing: -1.5px;">{title}</h1>
        <div class="site-subtitle" style="margin: 0; text-align: center; font-size: 1.2em; font-weight: 400; color: #666; max-width: 32em;">{description}</div>
      </div>
    </div>
  </header>
    '''

    # Theme toggle button (inserted after header)
    theme_toggle_html = '''
  <div class="theme-toggle-container" style="display: flex; justify-content: flex-end; width: 100%; margin: 0.5em 0 0.5em 0;">
    <button id="theme-toggle" class="theme-toggle" aria-label="Toggle theme" style="padding: 0.4em 1.2em; font-size: 1em; border-radius: 1.2em; border: 1px solid #bbb; background: var(--theme-toggle-bg, #f8f8f8); cursor: pointer;">
      <span id="theme-toggle-icon" aria-hidden="true">🌙</span> <span id="theme-toggle-label">Dark</span>
    </button>
  </div>
  <script>
    // Simple theme toggle script
    const btn = document.getElementById('theme-toggle');
    const icon = document.getElementById('theme-toggle-icon');
    const label = document.getElementById('theme-toggle-label');
    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      if (theme === 'dark') {
        icon.textContent = '☀️';
        label.textContent = 'Light';
      } else {
        icon.textContent = '🌙';
        label.textContent = 'Dark';
      }
      localStorage.setItem('theme', theme);
    }
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
    // On load, set theme from localStorage
    const saved = localStorage.getItem('theme');
    if (saved) setTheme(saved);
  </script>
    '''

    # Load head template
    head_path = os.path.join('static', 'templates', 'head.html')
    with open(head_path, 'r') as f:
        head_template = f.read()
    css_light = 'css/theme-light.css'
    css_dark = 'css/theme-dark.css'

    import nbformat
    import base64
    print(f"[DEBUG] build_html_for_files called with {len(files)} files:")
    for f in files:
        print(f"  - {f}")
    print("[DEBUG] Starting main file processing loop...")
    missing_files = []
    for file in files:
        print(f"[DEBUG] ---\n[DEBUG] Processing file: {file}")
        file_path = Path(file)
        if debug:
            print(f"[DEBUG] Starting processing for: {file}")
        if not file_path.exists():
            print(f"[ERROR] File not found: {file}")
            missing_files.append(file)
            continue
        ext = file_path.suffix.lower()
        print(f"[DEBUG] File extension: {ext}")
        try:
            if ext == '.md':
                print(f"[DEBUG] Reading markdown file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                print(f"[DEBUG] Rendering markdown to HTML...")
                body_html = markdown.markdown(md_content, extensions=['extra', 'toc', 'tables'])
            elif ext == '.ipynb':
                print(f"[DEBUG] Reading notebook file: {file_path}")
                try:
                    nb = nbformat.read(str(file_path), as_version=4)
                except Exception as e:
                    print(f"[ERROR] Could not read notebook: {file_path}: {e}")
                    continue
                print(f"[DEBUG] Notebook loaded. Keys: {list(nb.keys())}")
                if not nb.get('cells'):
                    print(f"[WARN] Notebook {file_path} has no cells.")
                    continue
                print(f"[DEBUG] Notebook {file_path} has {len(nb['cells'])} cells.")
                body_html = []
                for idx, cell in enumerate(nb.get('cells', [])):
                    print(f"[DEBUG] Processing cell {idx+1} of type {cell.get('cell_type')}")
                    cell_type = cell.get('cell_type')
                    lang = cell.get('metadata', {}).get('language', 'python' if cell_type == 'code' else 'markdown')
                    if debug:
                        print(f"[DEBUG] Cell {idx}: type={cell_type}, lang={lang}")
                    if cell_type == 'markdown':
                        import markdown as mdmod
                        try:
                            print(f"[DEBUG] Rendering markdown cell {idx+1}")
                            cell_html = mdmod.markdown(''.join(cell.get('source', [])), extensions=['extra', 'toc', 'tables'])
                            body_html.append(f'<div class="notebook-markdown-cell">{cell_html}</div>')
                        except Exception as e:
                            print(f"[ERROR] Failed to render markdown cell {idx+1} in {file_path}: {e}")
                    elif cell_type == 'code':
                        print(f"[DEBUG] Rendering code cell {idx+1}")
                        code = ''.join(cell.get('source', []))
                        code_html = f'<pre class="notebook-code-cell"><code>{code}</code></pre>'
                        outputs_html = []
                        for oidx, output in enumerate(cell.get('outputs', [])):
                            otype = output.get('output_type')
                            print(f"[DEBUG]   Output {oidx+1}: type={otype}")
                            try:
                                if otype == 'stream':
                                    text = ''.join(output.get('text', []))
                                    outputs_html.append(f'<div class="notebook-output-stream">{text}</div>')
                                elif otype == 'execute_result' or otype == 'display_data':
                                    data = output.get('data', {})
                                    if 'text/plain' in data:
                                        outputs_html.append(f'<div class="notebook-output-text">{data["text/plain"]}</div>')
                                    if 'image/png' in data:
                                        img_data = data['image/png']
                                        outputs_html.append(f'<img class="notebook-output-img" src="data:image/png;base64,{img_data}" />')
                                    if 'image/jpeg' in data:
                                        img_data = data['image/jpeg']
                                        outputs_html.append(f'<img class="notebook-output-img" src="data:image/jpeg;base64,{img_data}" />')
                                    if 'text/html' in data:
                                        outputs_html.append(f'<div class="notebook-output-html">{data["text/html"]}</div>')
                                elif otype == 'error':
                                    ename = output.get('ename', '')
                                    evalue = output.get('evalue', '')
                                    traceback = output.get('traceback', [])
                                    tb_html = '<br>'.join(traceback)
                                    outputs_html.append(f'<div class="notebook-output-error"><b>{ename}: {evalue}</b><br>{tb_html}</div>')
                            except Exception as e:
                                print(f"[ERROR] Failed to render output {oidx+1} in code cell {idx+1} in {file_path}: {e}")
                        cell_block = code_html + ''.join(outputs_html)
                        body_html.append(f'<div class="notebook-code-cell-block">{cell_block}</div>')
                body_html = '\n'.join(body_html)
            else:
                print(f"[SKIP] Unsupported file type: {file}")
                continue
            if not body_html:
                print(f"[WARN] No content generated for {file_path}, skipping HTML output.")
                continue
            # Compose full HTML with semantic, accessible structure
            page_title = title
            head_html = head_template.replace('{{ title }}', page_title).replace('{{ css_light }}', css_light).replace('{{ css_dark }}', css_dark)
            full_html = f'''<!DOCTYPE html>\n<html lang="{site.get('language', 'en')}">\n{head_html}\n<body>\n  {header_html}\n  <nav class="site-nav" id="site-nav" aria-label="Main navigation">{menu_html}</nav>\n  <main class="site-main container">\n    {theme_toggle_html}\n    {body_html}\n  </main>\n  <footer>\n    {footer_html}\n  </footer>\n</body>\n</html>\n'''
            out_dir = Path('docs')
            out_dir.mkdir(exist_ok=True)
            out_name = file_path.stem + '.html'
            out_path = out_dir / out_name
            try:
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                print(f"[OK] Built {out_path} from {file}")
            except Exception as e:
                print(f"[ERROR] Failed to write HTML file {out_path}: {e}")
        except Exception as e:
            print(f"[FATAL] Unexpected error processing {file}: {e}")
    if missing_files:
        print(f"[SUMMARY] {len(missing_files)} file(s) were missing and not processed:")
        for mf in missing_files:
            print(f"  - {mf}")
        # Always output a valid HTML page with .container for any fallback or summary
        # (This block is only for summary, not for outputting a page, so no fallback HTML is written here)
