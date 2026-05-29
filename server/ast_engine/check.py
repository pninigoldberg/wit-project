def check_code_issues(analysis_result):

    alerts = []

    # =========================
    # FILE LENGTH CHECK
    # =========================

    if analysis_result["file_length"] > 200:

        alerts.append({

            "type": "LONG_FILE",

            "message":
                "File is longer than 200 lines"
        })

    # =========================
    # FUNCTIONS CHECK
    # =========================

    for function in analysis_result["functions"]:

        # -------------------------
        # LONG FUNCTION
        # -------------------------

        if function["line_count"] > 20:

            alerts.append({

                "type": "LONG_FUNCTION",

                "message":
                    f'Function "{function["name"]}" '
                    f'is longer than 20 lines'
            })

        # -------------------------
        # MISSING DOCSTRING
        # -------------------------

        if not function["has_docstring"]:

            alerts.append({

                "type": "MISSING_DOCSTRING",

                "message":
                    f'Function "{function["name"]}" '
                    f'has no docstring'
            })

        # -------------------------
        # UNUSED VARIABLES
        # -------------------------

        for variable in function["unused_variables"]:

            alerts.append({

                "type": "UNUSED_VARIABLE",

                "message":
                    f'Unused variable "{variable}" '
                    f'in function "{function["name"]}"'
            })

        # -------------------------
        # NON ENGLISH VARIABLES
        # -------------------------

        for variable in function[
            "non_english_variables"
        ]:

            alerts.append({

                "type": "NON_ENGLISH_VARIABLE",

                "message":
                    f'Variable "{variable}" '
                    f'is not written in English'
            })

    return alerts