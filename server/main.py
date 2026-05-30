"""from fastapi import FastAPI
from server.models.request_models import AnalyzeRequest

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Server works"}


@app.post("/analyze")
def analyze_code(data: AnalyzeRequest):

    return {
        "message": "Files received successfully",
        "files_count": len(data.files)
    }"""

from fastapi import FastAPI

from server.models.request_models import AnalyzeRequest

from server.ast_engine.parser import parse_code
from server.ast_engine.analyzer import analyze_tree
from server.ast_engine.check import check_code_issues

# בעתיד:
# from server.graphs.graphs import generate_graphs


app = FastAPI()


# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "Server works"
    }


# =========================================
# ANALYZE ENDPOINT
# =========================================

@app.post("/analyze")
def analyze_code(data: AnalyzeRequest):

    # כל התוצאות של כל הקבצים
    results = []

    # =====================================
    # LOOP OVER ALL FILES
    # =====================================

    for file in data.files:

        # =================================
        # PARSE
        # =================================

        parsed_data = parse_code(
            file.code
        )

        # אם יש syntax error
        if not parsed_data["success"]:

            results.append({

                "filename": file.filename,

                "success": False,

                "error": parsed_data["error"]
            })

            continue

        # =================================
        # ANALYZE
        # =================================

        analysis_result = analyze_tree(

            parsed_data["tree"],

            file.code
        )

        # =================================
        # CHECK
        # =================================

        alerts = check_code_issues(
            analysis_result
        )

        # =================================
        # GRAPHS
        # =================================

        # בעתיד החברה שלך תוסיף:
        #
        # graphs = generate_graphs(
        #     analysis_result,
        #     alerts
        # )

        # =================================
        # SAVE FILE RESULT
        # =================================

        file_result = {

            "filename": file.filename,

            "success": True,

            "analysis_result": analysis_result,

            "alerts": alerts

            # "graphs": graphs
        }

        # שמירת התוצאה של הקובץ
        results.append(file_result)

    # =====================================
    # FINAL RESPONSE
    # =====================================

    graph_paths = generate_graphs(results)
    print(graph_paths)
    return {

        "files_count": len(data.files),

        "results": results,

        "graphs": graph_paths
    }