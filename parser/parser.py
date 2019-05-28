import ast
import os
import collections
import nltk

from nltk import pos_tag

nltk.download('averaged_perceptron_tagger')


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def check_py_files(path, max_len):
    filenames = []
    flag = False
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py') and len(filenames) <= max_len:
                filenames.append(os.path.join(dirname, file))
                if len(filenames) >= max_len:
                    return filenames
    print('total %s files' % len(filenames))
    return filenames


def get_trees(with_filenames=False, with_file_content=False):
    filenames = check_py_files(path, max_len=100)
    trees = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    trees = [t for t in get_trees(path) if t]
    function_names = [
        f for f in flat([get_all_names(t) for t in trees])
        if not magic_method(f)
        ]

    def split_snake_case_name_to_words(name):
        return [n for n in name.split('_') if n]
    return flat([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_top_verbs_in_path(path, top_size=10):
    Path = path
    trees = [t for t in get_trees(None) if t]
    fncs = [
        f for f in flat(
            [[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees]
            )
        if not magic_method(f)
        ]

    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in fncs])
    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=10):
    t = get_trees(path)
    nms = [
        f for f in flat(
            [[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in t]
            )
        if not magic_method(f)
        ]

    return collections.Counter(nms).most_common(top_size)

def magic_method(f):
    if (f.startswith('__') and f.startswith('__')):
        return True


if __name__ == "__main__":
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]


    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)


    TOP_SIZE = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurence in collections.Counter(wds).most_common(TOP_SIZE):
        print(word, occurence)
