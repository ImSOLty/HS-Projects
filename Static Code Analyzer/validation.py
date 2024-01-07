import re


def split_statement(line: str):
    try:
        edge = line.index('#')
        return line[:edge], line[edge:]
    except ValueError:
        return line, ""


def check_length(lines, k: int):
    return len(lines[k]) <= 79


def check_indentation(lines, k: int):
    return (len(lines[k]) - len(lines[k].lstrip())) % 4 == 0


def check_semicolon(lines, k: int):
    statement, comment = split_statement(lines[k])
    return not statement.strip().endswith(';')


def check_spaces_before_comment(lines, k: int):
    statement, comment = split_statement(lines[k])
    return (len(statement) - len(statement.rstrip()) >= 2
            or len(statement) == 0 or len(comment) == 0)


def check_todo(lines, k: int):
    statement, comment = split_statement(lines[k])
    return 'TODO'.lower() not in comment.lower()


def check_blanklines(lines, k: int):
    return k <= 2 or any([len(lines[k - t].strip()) > 0 for t in range(1, 4)])


def check_spaces_construction(lines, k: int):
    return re.search(r'(def|class)\s{2,}\S+', lines[k]) is None


validation_funcs = {
    "S001": check_length,
    "S002": check_indentation,
    "S003": check_semicolon,
    "S004": check_spaces_before_comment,
    "S005": check_todo,
    "S006": check_blanklines,
    "S007": check_spaces_construction,
}
