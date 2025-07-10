"""
Test that scripts/preprocess_content_yml.py correctly propagates titles from _content.yml to .autogen/_menu.yml.
"""
import subprocess
from pathlib import Path
import yaml
import sys

def run_preprocessor():
    result = subprocess.run([sys.executable, 'scripts/preprocess_content_yml.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError('Preprocessor failed')

def get_titles_from_content_yml(content_yml_path):
    with open(content_yml_path, 'r') as f:
        content = yaml.safe_load(f)
    titles = {}
    for chapter in content.get('chapters', []):
        for fobj in chapter.get('files', []):
            if isinstance(fobj, dict):
                file_path = fobj.get('file')
                title = fobj.get('title')
                if file_path and title:
                    titles[Path(file_path).with_suffix('.html').name] = title
    return titles

def get_titles_from_menu_yml(menu_yml_path):
    with open(menu_yml_path, 'r') as f:
        menu = yaml.safe_load(f)
    menu_items = menu['menu']
    chapters = next((item for item in menu_items if item.get('title') == 'Chapters'), None)
    if not chapters:
        return {}
    children = chapters.get('children', [])
    menu_titles = {item['path']: item['title'] for item in children if 'path' in item and 'title' in item}
    return menu_titles

def main():
    repo = Path(__file__).parent.parent
    content_yml = repo / '_content.yml'
    menu_yml = repo / '.autogen' / '_menu.yml'
    run_preprocessor()
    content_titles = get_titles_from_content_yml(content_yml)
    menu_titles = get_titles_from_menu_yml(menu_yml)
    failed = False
    for html_name, expected_title in content_titles.items():
        actual_title = menu_titles.get(html_name)
        if actual_title != expected_title:
            print(f'[FAIL] {html_name}: menu title="{actual_title}" != content.yml title="{expected_title}"')
            failed = True
    if not failed:
        print('[PASS] Preprocessor correctly propagates all titles.')

if __name__ == '__main__':
    main()
