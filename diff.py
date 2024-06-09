import difflib
import ast

def normalize_code(code):
    """
    Normalize the Python code by parsing it into an AST and then converting it back to a string.
    This removes unnecessary whitespace and standardizes the formatting.
    """
    try:
        tree = ast.parse(code)
        normalized_code = ast.unparse(tree)
        return normalized_code
    except SyntaxError:
        return code  # Return the original code if there's a syntax error

def is_comment(line):
    return line.strip().startswith('#')

def is_whitespace_change(line):
    return line.strip() == ''

def is_meaningful_diff(line):
    # Ignore lines that are comments or whitespace
    stripped_line = line.strip()
    return not (stripped_line.startswith('#') or stripped_line == '')

def resolve_diff(snippet_a, snippet_b):
    normalized_a = normalize_code(snippet_a)
    normalized_b = normalize_code(snippet_b)

    diff = difflib.ndiff(normalized_a.splitlines(), normalized_b.splitlines())
    meaningful_diffs = []

    for line in diff:
        # Only keep lines that are changed and meaningful
        if line.startswith('- ') or line.startswith('+ '):
            if is_meaningful_diff(line[2:]):
                meaningful_diffs.append(line)

    return meaningful_diffs

def resolve_categorized_diff(snippet_a, snippet_b):
    normalized_a = normalize_code(snippet_a)
    normalized_b = normalize_code(snippet_b)

    diff = difflib.ndiff(normalized_a.splitlines(), normalized_b.splitlines())
    categorized_diffs = []

    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            diff_type = "interpreter"
            content = line[2:]

            if is_comment(content):
                diff_type = "comment"
            elif is_whitespace_change(content):
                diff_type = "formatting"
            else:
                diff_type = "interpreter"

            categorized_diffs.append({"type": diff_type, "diff": line})

    return categorized_diffs

if __name__ == "__main__":
    snippet_a = (
        "# Router definition\n"
        "api_router = APIRouter()"
    )
    snippet_b = (
        "# Make sure endpoint are immune to missing trailing slashes\n"
        "api_router = APIRouter(redirect_slashes=True)"
    )
    snippet_c = (
        "# Router definition\n"
        "api_router = APIRouter(\n"
        "\tredirect_slashes=True\n"
        ")"
    )

    print("Meaningful diffs between snippet_a and snippet_b:")
    print(resolve_diff(snippet_a, snippet_b))
    print("\nMeaningful diffs between snippet_b and snippet_c:")
    print(resolve_diff(snippet_b, snippet_c))