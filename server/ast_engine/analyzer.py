import ast


def analyze_tree(tree, code):

    functions = []

    assigned_variables_global = []
    used_variables_global = []

    # מספר שורות בקובץ
    file_length = len(code.splitlines())

    # מעבר על כל ה nodes בעץ
    for node in ast.walk(tree):

        # =========================
        # FUNCTION ANALYSIS
        # =========================
        if isinstance(node, ast.FunctionDef):

            assigned_variables = []
            used_variables = []

            # בדיקה האם יש docstring
            has_docstring = ast.get_docstring(node) is not None

            # מעבר פנימי בתוך הפונקציה
            for inner_node in ast.walk(node):

                # =========================
                # ASSIGNED VARIABLES
                # =========================
                if isinstance(inner_node, ast.Assign):

                    for target in inner_node.targets:

                        if isinstance(target, ast.Name):

                            assigned_variables.append(target.id)
                            assigned_variables_global.append(target.id)

                # =========================
                # USED VARIABLES
                # =========================
                elif isinstance(inner_node, ast.Name):

                    if isinstance(inner_node.ctx, ast.Load):

                        used_variables.append(inner_node.id)
                        used_variables_global.append(inner_node.id)

            # חישוב unused variables
            unused_variables = list(
                set(assigned_variables) - set(used_variables)
            )

            # בדיקת משתנים לא באנגלית
            non_english_variables = []

            for variable in assigned_variables:

                if not variable.isascii():

                    non_english_variables.append(variable)

            # מידע על הפונקציה
            function_data = {

                "name": node.name,

                "start_line": node.lineno,

                "end_line": node.end_lineno,

                "line_count": (
                    node.end_lineno - node.lineno + 1
                ),

                "has_docstring": has_docstring,

                "assigned_variables": assigned_variables,

                "used_variables": used_variables,

                "unused_variables": unused_variables,

                "non_english_variables": non_english_variables
            }

            functions.append(function_data)

    # =========================
    # GLOBAL UNUSED VARIABLES
    # =========================
    unused_variables_global = list(
        set(assigned_variables_global) -
        set(used_variables_global)
    )

    # =========================
    # FINAL RESULT
    # =========================
    analysis_result = {

        "file_length": file_length,

        "functions_count": len(functions),

        "functions": functions,

        "global_unused_variables": unused_variables_global
    }

    return analysis_result