#This file contains the entry point to the entire application.
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, UploadFile, File

app = FastAPI(
    title ="Log Analyzer API",
    description=" An API to upload and parse log files to extract errors and warnings",
    version="0.1.0"
)
@app.get("/", tags=["Health Check"]) # tags is used for grouping endpoints in the documentation used by Swagger UI
def health_check() -> Dict[str, str]:
    """
    root path to check if the API is running.
    Purpose:
    - Provides a simple health check endpoint.
    - Does NOT require any parameters.
    - Does NOT return any data.
    - Does NOT perform any business logic.
    """
    return {
        "status": "online",
        "message": "Log Analyzer API is running."
        }


@app.post("/upload", tags=["Log Upload"])
async def upload_log(file : UploadFile = File(...)) -> Dict[str,Any]:
    return {"filename": file.filename, "content_type": file.content_type}