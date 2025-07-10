import yaml, sys
for fname in ['_toc.yml', '_config.yml']:
    try:
        with open(fname) as f: yaml.safe_load(f)
        print(f"[OK] {fname} is valid YAML.")
    except Exception as e:
        print(f"[ERROR] {fname} is invalid YAML: {e}")
        sys.exit(1)
