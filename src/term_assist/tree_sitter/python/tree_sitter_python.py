from tree_sitter_language_pack import get_language, get_parser

PY_LANGUAGE = get_language("python")
parser = get_parser("python")


def node_text(code_bytes, node):
    """
    Return the actual text of a node, decoded to string.
    """
    return code_bytes[node.start_byte : node.end_byte].decode("utf-8")


def chunk_name_for_node(node):

    if node.type == "import_statement" or node.type == "import_from_statement":
        return "Import"
    elif node.type == "function_definition":
        return "Function"
    elif node.type == "class_definition":
        return "Class"
    else:
        return "TopLevelCode"


def get_line_numbers(code, node):

    start_line = code[: node.start_byte].count("\n") + 1
    end_line = code[: node.end_byte].count("\n") + 1
    return start_line, end_line


def parse_and_chunk(filename: str):

    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()
    code_bytes = code.encode("utf-8")
    tree = parser.parse(code_bytes)
    root_node = tree.root_node

    chunks = []
    import_nodes = []

    for child in root_node.children:
        if child.is_missing or child.type == "comment":
            continue

        if child.type in {"import_statement", "import_from_statement"}:
            import_nodes.append(child)
        else:
            start, end = get_line_numbers(code, child)
            chunks.append(
                {
                    "type": chunk_name_for_node(child),
                    "start_line": start,
                    "end_line": end,
                    "snippet": node_text(code_bytes, child),
                }
            )

    if import_nodes:
        first, last = import_nodes[0], import_nodes[-1]
        start, end = get_line_numbers(code, first)
        _, end = get_line_numbers(code, last)

        snippet = "\n".join(node_text(code_bytes, n) for n in import_nodes)

        chunks.insert(
            0,
            {
                "type": "import",
                "start_line": start,
                "end_line": end,
                "snippet": snippet,
            },
        )

    return chunks
