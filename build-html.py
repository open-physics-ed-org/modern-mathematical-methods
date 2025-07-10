#!/usr/bin/env python3
"""
build-html.py

Skeleton script for building site outputs with flexible CLI flags.
Supports: --html, --md, --docx, --tex, --pdf, --jupyter, --ppt, and --files FILE1 FILE2 ...

No build logic yet—just argument parsing and structure.
"""
import argparse
import sys

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
            build_html_for_files(args.files)
        else:
            print("[INFO] Building HTML for all content.")
            build_html_all()

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

def build_html_all():
    """Build HTML for all markdown files in content/ using top-level menu only."""
    from glob import glob
    md_files = glob('content/**/*.md', recursive=True)
    if not md_files:
        print("[WARN] No markdown files found in content/.")
        return
    build_html_for_files(md_files)

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

def build_html_for_files(files):
    """
    Build HTML for specified markdown files using YAML-driven templates and navigation.
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
    if '--debug' in sys.argv:
        import pprint
        print("[DEBUG] Raw menu structure from get_menu_tree:")
        pprint.pprint(menu)
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
                if not file:
                    file = first_child_file(node)
                if title and file:
                    items.append((file, title))
        return items

    top_menu = top_level_menu_items(menu)

    if '--debug' in sys.argv:
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

    # Load head template
    head_path = os.path.join('static', 'templates', 'head.html')
    with open(head_path, 'r') as f:
        head_template = f.read()
    css_light = 'css/theme-light.css'
    css_dark = 'css/theme-dark.css'

    for file in files:
        md_path = Path(file)
        if not md_path.exists():
            print(f"[ERROR] File not found: {file}")
            continue
        # Convert markdown to HTML (in-memory)
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        body_html = markdown.markdown(md_content, extensions=['extra', 'toc', 'tables'])

        # Compose full HTML
        page_title = title
        head_html = head_template.replace('{{ title }}', page_title).replace('{{ css_light }}', css_light).replace('{{ css_dark }}', css_dark)
        full_html = f'''<!DOCTYPE html>
<html lang="{site.get('language', 'en')}">
{head_html}
<body>
{header_html}
<nav class="site-nav" id="site-nav">{menu_html}</nav>
<main class="site-main">
{body_html}
</main>
{footer_html}
</body>
</html>
'''
        # Output path: docs/<basename>.html
        out_dir = Path('docs')
        out_dir.mkdir(exist_ok=True)
        out_name = md_path.stem + '.html'
        out_path = out_dir / out_name
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"[OK] Built {out_path} from {file}")

if __name__ == '__main__':
    main()
