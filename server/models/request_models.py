from pydantic import BaseModel


class FileData(BaseModel):
    filename: str
    code: str


class AnalyzeRequest(BaseModel):
    files: list[FileData]