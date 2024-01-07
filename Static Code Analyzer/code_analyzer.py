import os
import re
import sys
import ast

from validation import validation_funcs


class Analyzer:
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            self.content = file.read()
            self.lines = self.content.splitlines()
        self.filepath = path
        self.issues = []

    def validate(self):
        self.issues = []
        # print(ast.dump(ast.parse(self.content)))
        # Formatting checks
        for i, l in enumerate(self.lines):
            for key, func in validation_funcs.items():
                if not func(self.lines, i):
                    self.issues.append(f'{self.filepath}: Line {i + 1}: {key}')
        # Syntax check
        already_names = []
        for node in ast.walk(ast.parse(self.content)):
            if isinstance(node, ast.ClassDef) and not re.fullmatch('([A-Z][a-z]+)+', node.name):
                self.issues.append(f'{self.filepath}: Line {node.lineno}: S008')
            if isinstance(node, ast.FunctionDef):
                if not re.fullmatch('([a-z1-9]*_?)+', node.name):
                    self.issues.append(f'{self.filepath}: Line {node.lineno}: S009')
                if any([not re.fullmatch('([a-z1-9]*_?)+', arg.arg) for arg in node.args.args]):
                    self.issues.append(f'{self.filepath}: Line {node.lineno}: S010')
                if any([any([isinstance(d, tp) for tp in [ast.Dict, ast.Set, ast.List]]) for d in node.args.defaults]):
                    self.issues.append(f'{self.filepath}: Line {node.lineno}: S012')
            if (isinstance(node, ast.Name)
                    and not re.fullmatch('([a-z1-9]*_?)+', node.id)
                    and node.id not in already_names):
                already_names.append(node.id)
                self.issues.append(f'{self.filepath}: Line {node.lineno}: S011')

        return self.issues


if __name__ == "__main__":
    path = sys.argv[1]
    d = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                file_path = os.path.join(root, name)
                print('\n'.join(Analyzer(file_path).validate()))
    else:
        print('\n'.join(Analyzer(path).validate()))
