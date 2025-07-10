import ast
import astor
import sys
import argparse

class RenameFunctionTransformer(ast.NodeTransformer):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def visit_FunctionDef(self, node):
        if node.name == self.old_name:
            node.name = self.new_name
        return self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.old_name:
            node.func.id = self.new_name
        return self.generic_visit(node)

class RemoveFunctionDefTransformer(ast.NodeTransformer):
    def __init__(self, func_name):
        self.func_name = func_name

    def visit_Module(self, node):
        node.body = [n for n in node.body if not (isinstance(n, ast.FunctionDef) and n.name == self.func_name)]
        return self.generic_visit(node)

class InsertRemoveRemoteImagesCall(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if node.name == "build_pdf_for_files":
            new_code = """
import subprocess
cmd = [sys.executable, 'remove_remote_images.py', str(file_path)]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print(f"[ERROR] remove_remote_images.py failed for {file_path}: {result.stderr}")
    continue
file_path = file_path.parent / (file_path.stem + '_no_remote' + file_path.suffix)
"""
            new_nodes = ast.parse(new_code).body
            # Insert at the start of the for-loop body inside build_pdf_for_files
            for stmt in node.body:
                if isinstance(stmt, ast.For):
                    stmt.body = new_nodes + stmt.body
            return node
        return self.generic_visit(node)
    
class FixFStringEscapes(ast.NodeTransformer):
    def visit_JoinedStr(self, node):
        # This will only fix f-strings with single-quoted escapes for ["description"]
        for idx, value in enumerate(node.values):
            if isinstance(value, ast.FormattedValue) and hasattr(value, 'value'):
                # Check if the formatted value is a Subscript with a Constant containing a single-quoted string
                if (isinstance(value.value, ast.Subscript) and
                    isinstance(value.value.slice, ast.Constant) and
                    isinstance(value.value.slice.value, str) and
                    value.value.slice.value.startswith("\\'") and value.value.slice.value.endswith("\\'")):
                    # Replace with double quotes
                    value.value.slice.value = value.value.slice.value.replace("\\'", '"')
        return self.generic_visit(node)

def main():
    parser = argparse.ArgumentParser(description="Generic AST-based Python code refactoring tool.")
    parser.add_argument("filename", help="Python file to edit")
    parser.add_argument("--rename-func", nargs=2, metavar=("OLD", "NEW"), help="Rename function OLD to NEW everywhere")
    parser.add_argument("--remove-func", metavar="NAME", help="Remove function definition with NAME")
    parser.add_argument("--insert-remove-remote", action="store_true", help="Insert remove_remote_images.py call in build_pdf_for_files")
    parser.add_argument("--fix-fstring-escapes", action="store_true", help="Fix f-string single-quote escapes")
    args = parser.parse_args()

    with open(args.filename, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)

    if args.rename_func:
        old, new = args.rename_func
        tree = RenameFunctionTransformer(old, new).visit(tree)
    if args.remove_func:
        tree = RemoveFunctionDefTransformer(args.remove_func).visit(tree)
    if args.insert_remove_remote:
        tree = InsertRemoveRemoteImagesCall().visit(tree)
    if args.fix_fstring_escapes:
        tree = FixFStringEscapes().visit(tree)

    new_source = astor.to_source(tree)
    with open(args.filename, "w", encoding="utf-8") as f:
        f.write(new_source)

if __name__ == "__main__":
    main()