import random
import re
from pathlib import Path
from typing import List

from fetcher import CodeDefinition, Problem, get_problem

CURRENT_FOLDER = Path(__file__).parent.resolve()


def main():
    print("Welcome to leetcode-python system.\n")
    initialized_ids = get_initialized_ids()

    while True:
        print(
            "Please enter a frontend problem id, \n"
            'or "random" to generate a random one, \n'
            'or "solve $i" to move problem to solution/, \n'
        )
        id_arg = input("Your choice: ").strip()

        random_pattern = re.compile(r"^random$")
        solving_pattern = re.compile(r"^solve (\d+)$")

        if random_pattern.match(id_arg):
            print("You selected random mode.")
            problem_id = generate_random_id(initialized_ids)
            print(f"Generated random problem: {problem_id}")
        elif match := solving_pattern.match(id_arg):
            # Solve a problem
            problem_id = int(match.group(1))
            deal_solving(problem_id)
            break
        else:
            try:
                problem_id = int(id_arg)
                if problem_id in initialized_ids:
                    print("The problem you chose has been initialized in problem/")
                    continue
            except ValueError:
                print(f"Invalid input: {id_arg}")
                continue

        problem = get_problem(problem_id)
        if not problem:
            print(
                f"Error: Failed to get problem #{problem_id} (it may be paid-only or not exist)."
            )
            continue

        code = next(
            (cd for cd in problem.code_definition if cd.value == "python"),
            None,
        )
        if not code:
            print(f"Problem {problem_id} has no Python version.")
            initialized_ids.append(problem.question_id)
            continue

        deal_problem(problem, code)
        break


def get_initialized_ids() -> List[int]:
    """Returns a list of initialized problem IDs."""
    id_pattern = re.compile(r"p(\d{4})_")
    problem_path = CURRENT_FOLDER / "src" / "problem"
    python_files = problem_path.glob("*.py")
    result = []

    for file in python_files:
        match = id_pattern.match(file.name)
        if match:
            result.append(int(match.group(1)))
    return result


def generate_random_id(except_ids: List[int]) -> int:
    """Generates a random ID that is not in the except_ids list."""
    while True:
        res = random.randint(1, 3298)  # Random number between 1 and 3298
        if res not in except_ids:
            return res
        print(
            f"Generated random ID ({res}), but it is invalid (the problem may have been solved "
            "or may have no Python version). Regenerating..."
        )


def deal_solving(problem_id: int):
    """Moves a problem file from the `problem/` directory to the `solution/` directory."""
    # Fetch the problem details
    problem = get_problem(problem_id)
    if not problem:
        raise ValueError(f"Problem {problem_id} does not exist.")

    file_name = f"p{problem.question_id:04}_{problem.title_slug.replace('-', '_')}"
    file_path = CURRENT_FOLDER / "src" / "problem" / f"{file_name}.py"

    # Check if the problem file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Problem file {file_path} does not exist.")

    solution_name = f"s{problem.question_id:04}_{problem.title_slug.replace('-', '_')}"
    solution_path = CURRENT_FOLDER / "src" / "solution" / f"{solution_name}.py"

    # Check if the solution file already exists
    if solution_path.exists():
        raise FileExistsError(f"Solution file {solution_path} already exists.")

    # Move the problem file to the solution directory
    file_path.rename(solution_path)


def deal_problem(problem: Problem, code: CodeDefinition):
    """
    Handles initializing a problem file using a template.
    """
    file_name = f"p{problem.question_id:04}_{problem.title_slug.replace('-', '_')}"
    file_path = CURRENT_FOLDER / "src" / "problem" / f"{file_name}.py"

    if file_path.exists():
        raise FileExistsError("Problem already initialized")

    # Read the template
    template_path = CURRENT_FOLDER / "template.txt"
    if not template_path.exists():
        raise FileNotFoundError("Template file not found")

    with template_path.open("r") as f:
        template = f.read()

    # Replace placeholders in the template
    source = (
        template.replace("__PROBLEM_TITLE__", problem.title)
        .replace("__PROBLEM_DESC__", build_desc(problem.content))
        .replace(
            "__PROBLEM_DEFAULT_CODE__",
            insert_return_in_code(problem.return_type, code.default_code),
        )
        .replace("__PROBLEM_ID__", str(problem.question_id))
        .replace("__EXTRA_IMPORT__", parse_extra_import(code.default_code))
        .replace("__PROBLEM_LINK__", parse_problem_link(problem))
        .replace("__DISCUSS_LINK__", parse_discuss_link(problem))
    )

    # Write the formatted template to the problem file
    with file_path.open("w") as f:
        f.write(source)


def build_desc(content: str) -> str:
    """Cleans up the problem description by removing or replacing HTML tags and entities."""
    return (
        content.replace("<strong>", "")
        .replace("</strong>", "")
        .replace("<em>", "")
        .replace("</em>", "")
        .replace("</p>", "")
        .replace("<p>", "")
        .replace("<b>", "")
        .replace("</b>", "")
        .replace("<pre>", "")
        .replace("</pre>", "")
        .replace("<ul>", "")
        .replace("</ul>", "")
        .replace("<li>", "")
        .replace("</li>", "")
        .replace("<code>", "")
        .replace("</code>", "")
        .replace("<i>", "")
        .replace("</i>", "")
        .replace("<sub>", "")
        .replace("</sub>", "")
        .replace("</sup>", "")
        .replace("<sup>", "^")
        .replace("&nbsp;", " ")
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("&quot;", '"')
        .replace("&minus;", "-")
        .replace("&#39;", "'")
        .replace("\n\n", "\n")
        .replace("\n", "\n * ")
    )


def insert_return_in_code(return_type: str, code: str) -> str:
    """
    Inserts a default return statement into the provided code based on the return type.
    """
    # Match an empty code block like `{}` or `{ <whitespace> }`
    re_pattern = re.compile(r"\{\s*\}")

    replacements = {
        "ListNode": "{\n    return ListNode(0)\n}",
        "ListNode[]": "{\n    return []\n}",
        "TreeNode": "{\n    return TreeNode(0)\n}",
        "boolean": "{\n    return False\n}",
        "character": "{\n    return '0'\n}",
        "character[][]": "{\n    return []\n}",
        "double": "{\n    return 0.0\n}",
        "double[]": "{\n    return []\n}",
        "int[]": "{\n    return []\n}",
        "integer": "{\n    return 0\n}",
        "integer[]": "{\n    return []\n}",
        "integer[][]": "{\n    return []\n}",
        "list<String>": "{\n    return []\n}",
        "list<TreeNode>": "{\n    return []\n}",
        "list<boolean>": "{\n    return []\n}",
        "list<double>": "{\n    return []\n}",
        "list<integer>": "{\n    return []\n}",
        "list<list<integer>>": "{\n    return []\n}",
        "list<list<string>>": "{\n    return []\n}",
        "list<string>": "{\n    return []\n}",
        "null": code,
        "string": '{\n    return ""\n}',
        "string[]": "{\n    return []\n}",
        "void": code,
        "NestedInteger": code,
        "Node": code,
    }

    # Get the replacement based on the return type
    replacement = replacements.get(return_type, code)

    # Apply the regex replacement if a new return statement is defined
    return re_pattern.sub(replacement, code)


def parse_extra_import(code: str) -> str:
    """
    Parses the code and generates appropriate import statements based on the structures used.
    """
    extra_imports = []

    # Check for linked-list usage
    if "class ListNode" in code:
        extra_imports.append("from utils.linked_list import ListNode, to_list")

    # Check for tree usage
    if "class TreeNode" in code:
        extra_imports.append("from utils.tree import TreeNode, to_tree")

    # Check for point usage
    if "class Point" in code:
        extra_imports.append("from utils.point import Point")

    return "\n".join(extra_imports)


def parse_problem_link(problem: "Problem") -> str:
    """
    Generates the LeetCode problem link based on the problem's title_slug.
    """
    return f"https://leetcode.com/problems/{problem.title_slug}/"


def parse_discuss_link(problem: "Problem") -> str:
    """
    Generates the LeetCode discussion link for the problem based on the problem's title_slug.
    """
    return f"https://leetcode.com/problems/{problem.title_slug}/discuss/?currentPage=1&orderBy=most_votes&query="


if __name__ == "__main__":
    main()
