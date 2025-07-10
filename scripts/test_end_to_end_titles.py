"""
End-to-end test: Edit _content.yml, run preprocessor, check .autogen/_menu.yml, and report results.
"""
import yaml
import subprocess
from pathlib import Path
import sys
import shutil
import tempfile

def backup_file(path):
    backup = path.with_suffix(path.suffix + '.bak')
    shutil.copy2(path, backup)
    return backup

def restore_file(path, backup):
    shutil.move(str(backup), str(path))

def edit_content_yml(content_yml_path, test_title):
    with open(content_yml_path, 'r') as f:
        content = yaml.safe_load(f)
    # Edit the first notebook file title in mechanics
    for chapter in content.get('chapters', []):
        if chapter.get('id') == 'mechanics':
            for fobj in chapter.get('files', []):
                if isinstance(fobj, dict) and 'title' in fobj:
                    fobj['title'] = test_title
                    break
            break
    with open(content_yml_path, 'w') as f:
        yaml.dump(content, f, sort_keys=False, allow_unicode=True)

def run_preprocessor():
    result = subprocess.run([sys.executable, 'scripts/preprocess_content_yml.py'], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError('Preprocessor failed')

def get_first_mechanics_title_from_menu(menu_yml_path):
    with open(menu_yml_path, 'r') as f:
        menu = yaml.safe_load(f)
    menu_items = menu['menu']
    chapters = next((item for item in menu_items if item.get('title') == 'Chapters'), None)
    if not chapters:
        return None
    children = chapters.get('children', [])
    # Find the first mechanics notebook (by path)
    for item in children:
        if 'activity-duffing' in item['path']:
            return item['title']
    return None

def main():
    repo = Path(__file__).parent.parent
    content_yml = repo / '_content.yml'
    menu_yml = repo / '.autogen' / '_menu.yml'
    test_title = 'TEST_TITLE_12345'
    backup = backup_file(content_yml)
    try:
        edit_content_yml(content_yml, test_title)
        run_preprocessor()
        menu_title = get_first_mechanics_title_from_menu(menu_yml)
        if menu_title == test_title:
            print('[PASS] End-to-end: menu title updated from _content.yml')
        else:
            print(f'[FAIL] End-to-end: menu title="{menu_title}" != test title="{test_title}"')
    finally:
        restore_file(content_yml, backup)
        run_preprocessor()  # Restore menu to original

if __name__ == '__main__':
    main()
