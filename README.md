# Code Explanation

This README file explains the functionality and implementation details of the Python script provided. The script compares two Python code snippets, normalizes their formatting, and identifies meaningful differences between them.

# Functions

## `normalize_code(code)`

```python
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
```

### Purpose: 
This function normalizes Python code by parsing it into an Abstract Syntax Tree (AST) and then converting it back to a string. This process removes unnecessary whitespace and standardizes the formatting.
### Parameters:
code (str): A string containing the Python code to be normalized.
### Returns:
normalized_code (str): The normalized version of the input code. If there is a syntax error, it returns the original code.

## is_comment(line)

``` python
   def is_comment(line):
    return line.strip().startswith('#')
```
### Purpose: 
This function checks if a given line of code is a comment.
Parameters:
### line (str):
A string containing a single line of code.
### Returns:
(bool): True if the line is a comment, False otherwise.

## is_whitespace_change(line)
```python
def is_whitespace_change(line):
    return line.strip() == ''
```
### Purpose: 
This function checks if a given line of code is only whitespace.
### Parameters:
line (str): A string containing a single line of code.
### Returns:
(bool): True if the line is only whitespace, False otherwise.

# i#s_meaningful_diff(line)

```python
  def is_meaningful_diff(line):
    # Ignore lines that are comments or whitespace
    stripped_line = line.strip()
    return not (stripped_line.startswith('#') or stripped_line == '')
```
### Purpose: 
This function determines if a given line of code represents a meaningful difference, excluding comments and whitespace.
### Parameters:
line (str): A string containing a single line of code.
### Returns:
(bool): True if the line represents a meaningful difference, False otherwise.

## resolve_diff(snippet_a, snippet_b)
```python
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
```
### Purpose: 
This function compares two code snippets, normalizes them, and identifies the meaningful differences.
### Parameters:
snippet_a (str): A string containing the first code snippet.
snippet_b (str): A string containing the second code snippet.
### Returns:
meaningful_diffs (list): A list of strings representing the meaningful differences between the two snippets.

## resolve_categorized_diff(snippet_a, snippet_b)

``` python
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
```
### Purpose: 
This function compares two code snippets, normalizes them, and categorizes the differences into comments, formatting changes, and interpreter-relevant changes.
### Parameters:
snippet_a (str): A string containing the first code snippet.
snippet_b (str): A string containing the second code snippet.
### Returns:
categorized_diffs (list): A list of dictionaries, each containing a type and the difference line.

## Main Execution

``` python
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
```
### Purpose: 
The main block of code runs comparisons between different code snippets and prints the meaningful differences.

### Code Snippets:

snippet_a: Contains a simple router definition.
snippet_b: Contains a router definition with an additional comment and a parameter for redirect_slashes.
snippet_c: Contains a router definition with the redirect_slashes parameter formatted differently.

# Output: 
<img width="770" alt="image" src="https://github.com/omkar806/CodeDiff/assets/77787482/1aab947e-6d92-4a81-900d-7ce83f7967d9">
