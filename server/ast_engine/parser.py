import ast


def parse_code(code: str):
    try:
        tree = ast.parse(code)

        return {
            "success": True,
            "tree": tree,
            "error": None
        }

    except SyntaxError as error:

        return {
            "success": False,
            "tree": None,
            "error": f"Syntax Error: {error}"
        }
