import yaml, sys

toc = yaml.safe_load(open('_toc.yml'))
def check_toc(toc):
    files = set()
    def walk(node):
        if isinstance(node, dict):
            if 'file' in node:
                if node['file'] in files:
                    print(f"[ERROR] Duplicate file: {node['file']}")
                    sys.exit(1)
                files.add(node['file'])
            for k in ('chapters', 'sections'):
                if k in node:
                    for c in node[k]: walk(c)
        elif isinstance(node, list):
            for c in node: walk(c)
    walk(toc.get('chapters', []))
    print("[OK] No duplicate files in TOC.")
check_toc(toc)
