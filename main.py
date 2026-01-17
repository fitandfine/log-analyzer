#This file contains the entry point to the entire application.
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, UploadFile, File

app = FastAPI(
    title ="Log Analyzer API",
    description=" An API to upload and parse log files to extract errors and warnings",
    version="0.1.0"
)
@app.get("/", tags=["Health Check"]) # tags is used for grouping endpoints in the documentation used by Swagger UI
def health_check() -> Dict[str, str]: #The Return Type Hint. It promises that the function will output a Dictionary with String keys and values of string type.
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
# use async def for better performance when handling file uploads, as it allows other requests to be processed while waiting for file I/O operations to complete.
async def upload_log(file : UploadFile = File(...)) -> Dict[str,Any]: # Even though File() also works, always use ... for required fields.
   if not file.filename.endswith((".txt",".log",".logfile",".pdf")):
       raise HTTPException(status_code=400, detail="Invalid file type. Only plain text files are allowed.")
   else:
       return {"filename": file.filename, "content_type": file.content_type}