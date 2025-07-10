import yaml

def print_tree(node, indent=0):
    if isinstance(node, dict):
        if 'file' in node: print('  '*indent + f"- {node['file']}")
        if 'part' in node: print('  '*indent + f"* {node['part']}")
        for k in ('chapters', 'sections'):
            if k in node:
                for c in node[k]: print_tree(c, indent+1)
    elif isinstance(node, list):
        for c in node: print_tree(c, indent)

toc = yaml.safe_load(open('_toc.yml'))
print_tree(toc.get('chapters', []))
