from fastapi import FastAPI
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
    }