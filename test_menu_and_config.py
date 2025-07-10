from content_parser import load_and_validate_content_yml
from menu_parser import get_menu_tree

content = load_and_validate_content_yml('_content.yml')
print("Site config keys:", list(content['site'].keys()))
menu = get_menu_tree('_content.yml')
print("Menu loaded:", menu)
