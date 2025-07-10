
import shutil

def copy_static_assets(debug=False):
    """Copy CSS and image assets from static/ to docs/."""
    # Copy CSS
    css_src = Path('static/css')
    css_dest = Path('docs/css')
    if css_src.exists():
        css_dest.mkdir(parents=True, exist_ok=True)
        for css_file in css_src.glob('*.css'):
            dest = css_dest / css_file.name
            shutil.copy2(css_file, dest)
            debug_print(f"[INFO] Copied {css_file} to {dest}", debug)
    else:
        debug_print(f"[WARN] Source CSS directory {css_src} does not exist.", debug)
    # Copy images
    img_src = Path('static/images')
    img_dest = Path('docs/images')
    if img_src.exists():
        img_dest.mkdir(parents=True, exist_ok=True)
        for img_file in img_src.glob('*'):
            if img_file.is_file():
                dest = img_dest / img_file.name
                shutil.copy2(img_file, dest)
                debug_print(f"[INFO] Copied {img_file} to {dest}", debug)
    else:
        debug_print(f"[WARN] Source images directory {img_src} does not exist.", debug)
def debug_print(msg, debug):
    if debug:
        print(msg)
#!/usr/bin/env python3

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
    copy_static_assets(debug=debug)
    """Build HTML for all files referenced in the menu/content tree (_content.yml)."""
    from content_parser import load_and_validate_content_yml, get_all_content_files
    content = load_and_validate_content_yml('_content.yml')
    files = get_all_content_files(content)
    if not files:
        if debug:
            print("[WARN] No files found in _content.yml toc.")
        return
    if debug:
        print(f"[INFO] Building HTML for {len(files)} files from menu/content tree.")
    build_html_for_files(files, debug=debug)

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
    copy_static_assets(debug=debug)
    debug_print("[DEBUG] build_html_for_files() is running!", debug)
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


    import re
    def slugify(title):
        # Lowercase, replace spaces with hyphens, remove non-alphanum except hyphens
        slug = title.lower().strip()
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        return slug

    def file_to_html_link(file_path, title, is_auto_index=False):
        if is_auto_index:
            base = slugify(title)
        else:
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
                is_auto_index = False
                if not file and node.get('children'):
                    # This is an auto-generated index
                    is_auto_index = True
                    file = slugify(title) + '.html'
                elif file:
                    # Use the file as normal
                    pass
                if title and (file or node.get('children')):
                    items.append((file, title, node, is_auto_index))
        return items

    top_menu = top_level_menu_items(menu)

    menu_html = ['<ul class="site-nav-menu" id="site-nav-menu">']
    for file, title, _, is_auto_index in top_menu:
        menu_html.append('<li>')
        menu_html.append(file_to_html_link(file, title, is_auto_index=is_auto_index))
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
      <span id="theme-toggle-icon" aria-hidden="true">☀️</span> <span id="theme-toggle-label">Light</span>
    </button>
  </div>
  <script>
    // Default to dark mode unless user has set a preference
    function getPreferredTheme() {
      const saved = localStorage.getItem('theme');
      if (saved) return saved;
      return 'dark';
    }
    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      const icon = document.getElementById('theme-toggle-icon');
      const label = document.getElementById('theme-toggle-label');
      if (theme === 'dark') {
        icon.textContent = '☀️';
        label.textContent = 'Light';
      } else {
        icon.textContent = '🌙';
        label.textContent = 'Dark';
      }
      localStorage.setItem('theme', theme);
    }
    document.addEventListener('DOMContentLoaded', function() {
      const btn = document.getElementById('theme-toggle');
      btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
        setTheme(current === 'dark' ? 'light' : 'dark');
      });
      setTheme(getPreferredTheme());
    });
  </script>
    '''

    head_path = os.path.join('static', 'templates', 'head.html')
    with open(head_path, 'r') as f:
        head_template = f.read()
    css_light = 'css/theme-light.css'
    css_dark = 'css/theme-dark.css'

    import nbformat
    import base64
    debug_print(f"[DEBUG] build_html_for_files called with {len(files)} files:", debug)
    for f in files:
        debug_print(f"  - {f}", debug)
    debug_print(f"[DEBUG] Current working directory: {os.getcwd()}", debug)
    debug_print(f"[DEBUG] Output directory absolute path: {str(Path('docs').resolve())}", debug)
    debug_print(f"[DEBUG] Output directory exists: {Path('docs').exists()}", debug)
    debug_print("[DEBUG] Listing files in output directory (docs/):", debug)
    try:
        for p in Path('docs').iterdir():
            debug_print(f"    - {p.name} (dir: {p.is_dir()}, file: {p.is_file()})", debug)
            if p.is_dir():
                for subp in p.iterdir():
                    debug_print(f"      - {subp.name} (dir: {subp.is_dir()}, file: {subp.is_file()})", debug)
    except Exception as e:
        debug_print(f"[ERROR] Could not list docs/: {e}", debug)
    debug_print("[DEBUG] Starting main file processing loop...", debug)
    missing_files = []

    # --- Auto-generate index pages for top-level menus with no file ---
    for file, title, node, is_auto_index in top_menu:
        if is_auto_index:
            # Always generate at slugified-title.html for auto-indexes
            slug = slugify(title)
            out_path = Path('docs') / f"{slug}.html"
            # Build a list of children (and grandchildren)
            def render_children(children, level=1):
                html = []
                for child in children:
                    if not isinstance(child, dict):
                        continue
                    child_title = child.get('title', '(untitled)')
                    child_file = child.get('file')
                    child_children = child.get('children')
                    # Use h2/h3/h4 for subgroups, and always list grandchildren if present
                    if child_file and child_children:
                        # Submenu/group with a file: link and heading, then list grandchildren
                        heading_tag = f'h{min(level+1, 4)}'
                        html.append(f'<{heading_tag}>{file_to_html_link(child_file, child_title)}</{heading_tag}>')
                        html.append(render_children(child_children, level+1))
                    elif child_file:
                        # Just a file
                        html.append(f'<li>{file_to_html_link(child_file, child_title)}</li>')
                    elif child_children:
                        # Submenu/group with no file: heading, then list grandchildren
                        heading_tag = f'h{min(level+1, 4)}'
                        html.append(f'<{heading_tag}>{child_title}</{heading_tag}>')
                        html.append(render_children(child_children, level+1))
                # Only wrap in <ul> if there are <li> children at this level
                if any(x.startswith('<li>') for x in html):
                    return '<ul class="menu-section">' + ''.join(html) + '</ul>'
                else:
                    return ''.join(html)
            section_html = f'<h2>{title}</h2>'
            if node.get('description'):
                section_html += f'<div class="menu-description">{node["description"]}</div>'
            section_html += render_children(node['children'])
            page_title = title
            head_html = head_template.replace('{{ title }}', page_title).replace('{{ css_light }}', css_light).replace('{{ css_dark }}', css_dark)
            full_html = f'''<!DOCTYPE html>\n<html lang="{site.get('language', 'en')}">\n{head_html}\n<body>\n  {header_html}\n  <nav class="site-nav" id="site-nav" aria-label="Main navigation">{menu_html}</nav>\n  <main class="site-main container">\n    {theme_toggle_html}\n    {section_html}\n  </main>\n  <footer>\n    {footer_html}\n  </footer>\n</body>\n</html>\n'''
            out_path.parent.mkdir(exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            debug_print(f"[OK] Auto-generated index page: {out_path}", debug)

    # --- Normal file build logic ---
    for file in files:
        debug_print(f"[DEBUG] ---\n[DEBUG] Processing file: {file}", debug)
        file_path = Path(file)
        debug_print(f"[DEBUG] Starting processing for: {file}", debug)
        if not file_path.exists():
            debug_print(f"[ERROR] File not found: {file}", debug)
            missing_files.append(file)
            continue
        ext = file_path.suffix.lower()
        debug_print(f"[DEBUG] File extension: {ext}", debug)
        try:
            if ext == '.md':
                debug_print(f"[DEBUG] Reading markdown file: {file_path}", debug)
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                debug_print(f"[DEBUG] Rendering markdown to HTML...", debug)
                body_html = markdown.markdown(md_content, extensions=['extra', 'toc', 'tables'])
            elif ext == '.ipynb':
                debug_print(f"[DEBUG] Reading notebook file: {file_path}", debug)
                try:
                    nb = nbformat.read(str(file_path), as_version=4)
                except Exception as e:
                    debug_print(f"[ERROR] Could not read notebook: {file_path}: {e}", debug)
                    continue
                debug_print(f"[DEBUG] Notebook loaded. Keys: {list(nb.keys())}", debug)
                if not nb.get('cells'):
                    debug_print(f"[WARN] Notebook {file_path} has no cells.", debug)
                    continue
                debug_print(f"[DEBUG] Notebook {file_path} has {len(nb['cells'])} cells.", debug)
                body_html = []
                for idx, cell in enumerate(nb.get('cells', [])):
                    debug_print(f"[DEBUG] Processing cell {idx+1} of type {cell.get('cell_type')}", debug)
                    cell_type = cell.get('cell_type')
                    lang = cell.get('metadata', {}).get('language', 'python' if cell_type == 'code' else 'markdown')
                    debug_print(f"[DEBUG] Cell {idx}: type={cell_type}, lang={lang}", debug)
                    if cell_type == 'markdown':
                        import markdown as mdmod
                        try:
                            debug_print(f"[DEBUG] Rendering markdown cell {idx+1}", debug)
                            cell_html = mdmod.markdown(''.join(cell.get('source', [])), extensions=['extra', 'toc', 'tables'])
                            body_html.append(f'<div class="notebook-markdown-cell">{cell_html}</div>')
                        except Exception as e:
                            debug_print(f"[ERROR] Failed to render markdown cell {idx+1} in {file_path}: {e}", debug)
                    elif cell_type == 'code':
                        debug_print(f"[DEBUG] Rendering code cell {idx+1}", debug)
                        code = ''.join(cell.get('source', []))
                        code_html = f'<pre class="notebook-code-cell"><code>{code}</code></pre>'
                        outputs_html = []
                        for oidx, output in enumerate(cell.get('outputs', [])):
                            otype = output.get('output_type')
                            debug_print(f"[DEBUG]   Output {oidx+1}: type={otype}", debug)
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
                                debug_print(f"[ERROR] Failed to render output {oidx+1} in code cell {idx+1} in {file_path}: {e}", debug)
                        cell_block = code_html + ''.join(outputs_html)
                        body_html.append(f'<div class="notebook-code-cell-block">{cell_block}</div>')
                body_html = '\n'.join(body_html)
            else:
                debug_print(f"[SKIP] Unsupported file type: {file}", debug)
                continue
            if not body_html:
                debug_print(f"[WARN] No content generated for {file_path}, skipping HTML output.", debug)
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
                debug_print(f"[OK] Built {out_path} from {file}", debug)
            except Exception as e:
                debug_print(f"[ERROR] Failed to write HTML file {out_path}: {e}", debug)
        except Exception as e:
            debug_print(f"[FATAL] Unexpected error processing {file}: {e}", debug)
    if missing_files:
        debug_print(f"[SUMMARY] {len(missing_files)} file(s) were missing and not processed:", debug)
        for mf in missing_files:
            debug_print(f"  - {mf}", debug)
        # Always output a valid HTML page with .container for any fallback or summary
        # (This block is only for summary, not for outputting a page, so no fallback HTML is written here)

def main():
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
    if args.debug:
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
        if args.debug:
            print("[INFO] HTML build selected.")
        if args.files:
            if args.debug:
                print(f"[INFO] Building HTML for specified files: {args.files}")
            build_html_for_files(args.files, debug=args.debug)
        else:
            if args.debug:
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
    debug_print(f"[DEBUG] build_html_for_files called with {len(files)} files:", debug)
    for f in files:
        debug_print(f"  - {f}", debug)
    debug_print("[DEBUG] Starting main file processing loop...", debug)
    missing_files = []
    for file in files:
        debug_print(f"[DEBUG] ---\n[DEBUG] Processing file: {file}", debug)
        file_path = Path(file)
        debug_print(f"[DEBUG] Starting processing for: {file}", debug)
        if not file_path.exists():
            debug_print(f"[ERROR] File not found: {file}", debug)
            missing_files.append(file)
            continue
        ext = file_path.suffix.lower()
        debug_print(f"[DEBUG] File extension: {ext}", debug)
        try:
            if ext == '.md':
                debug_print(f"[DEBUG] Reading markdown file: {file_path}", debug)
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                debug_print(f"[DEBUG] Rendering markdown to HTML...", debug)
                body_html = markdown.markdown(md_content, extensions=['extra', 'toc', 'tables'])
            elif ext == '.ipynb':
                debug_print(f"[DEBUG] Reading notebook file: {file_path}", debug)
                try:
                    nb = nbformat.read(str(file_path), as_version=4)
                except Exception as e:
                    debug_print(f"[ERROR] Could not read notebook: {file_path}: {e}", debug)
                    continue
                debug_print(f"[DEBUG] Notebook loaded. Keys: {list(nb.keys())}", debug)
                if not nb.get('cells'):
                    debug_print(f"[WARN] Notebook {file_path} has no cells.", debug)
                    continue
                debug_print(f"[DEBUG] Notebook {file_path} has {len(nb['cells'])} cells.", debug)
                body_html = []
                for idx, cell in enumerate(nb.get('cells', [])):
                    debug_print(f"[DEBUG] Processing cell {idx+1} of type {cell.get('cell_type')}", debug)
                    cell_type = cell.get('cell_type')
                    lang = cell.get('metadata', {}).get('language', 'python' if cell_type == 'code' else 'markdown')
                    debug_print(f"[DEBUG] Cell {idx}: type={cell_type}, lang={lang}", debug)
                    if cell_type == 'markdown':
                        import markdown as mdmod
                        try:
                            debug_print(f"[DEBUG] Rendering markdown cell {idx+1}", debug)
                            cell_html = mdmod.markdown(''.join(cell.get('source', [])), extensions=['extra', 'toc', 'tables'])
                            body_html.append(f'<div class="notebook-markdown-cell">{cell_html}</div>')
                        except Exception as e:
                            debug_print(f"[ERROR] Failed to render markdown cell {idx+1} in {file_path}: {e}", debug)
                    elif cell_type == 'code':
                        debug_print(f"[DEBUG] Rendering code cell {idx+1}", debug)
                        code = ''.join(cell.get('source', []))
                        code_html = f'<pre class="notebook-code-cell"><code>{code}</code></pre>'
                        outputs_html = []
                        for oidx, output in enumerate(cell.get('outputs', [])):
                            otype = output.get('output_type')
                            debug_print(f"[DEBUG]   Output {oidx+1}: type={otype}", debug)
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
                                debug_print(f"[ERROR] Failed to render output {oidx+1} in code cell {idx+1} in {file_path}: {e}", debug)
                        cell_block = code_html + ''.join(outputs_html)
                        body_html.append(f'<div class="notebook-code-cell-block">{cell_block}</div>')
                body_html = '\n'.join(body_html)
            else:
                debug_print(f"[SKIP] Unsupported file type: {file}", debug)
                continue
            if not body_html:
                debug_print(f"[WARN] No content generated for {file_path}, skipping HTML output.", debug)
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
                debug_print(f"[OK] Built {out_path} from {file}", debug)
            except Exception as e:
                debug_print(f"[ERROR] Failed to write HTML file {out_path}: {e}", debug)
        except Exception as e:
            debug_print(f"[FATAL] Unexpected error processing {file}: {e}", debug)
    if missing_files:
        debug_print(f"[SUMMARY] {len(missing_files)} file(s) were missing and not processed:", debug)
        for mf in missing_files:
            debug_print(f"  - {mf}", debug)
        # Always output a valid HTML page with .container for any fallback or summary
        # (This block is only for summary, not for outputting a page, so no fallback HTML is written here)
