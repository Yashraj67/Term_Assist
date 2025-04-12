import os
import re
import sys

from intervaltree import IntervalTree

sys.path.append("/home/yashraj/term_assist/term_assist/src")

from term_assist.constants import LINE_REGEX_PATTERNS
from term_assist.tree_sitter.python.tree_sitter_python import parse_and_chunk


def find_line_numbers(stderr_output: str):
    all_line_numbers = []
    for pattern in LINE_REGEX_PATTERNS:
        matches = re.findall(pattern, stderr_output)
        all_line_numbers.extend(matches)

    print(all_line_numbers)
    return list(set(all_line_numbers))


def get_file_len(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


def get_file_context(stderr_output, filepath, extention):
    error_lines = find_line_numbers(stderr_output)

    if extention in tuple([".py", ".cpp", ".java"]):
        file_len = get_file_len(filepath)
        context = ""
        if file_len > 100:
            chunks = parse_and_chunk(filepath)
            map = {}
            intervals = []
            for chunk in chunks:
                map[f"{chunk['start_line']} - {chunk["end_line"]+1}"] = chunk["snippet"]
                intervals.append((chunk["start_line"], chunk["end_line"] + 1))
            print(intervals)
            tree = IntervalTree.from_tuples(intervals)
            hits = {(iv.begin, iv.end) for p in error_lines for iv in tree.at(int(p))}
            for hit in hits:
                context += map[f"{hit[0]} - {hit[1]}"] + "/n"
            print(context)

        return context
    else:
        return
