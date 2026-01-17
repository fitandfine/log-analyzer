#This file contains the entry point to the entire application.
from typing import Dict, Any, List
from fastapi import (
    FastAPI,
      HTTPException, 
      UploadFile,
        File,
        status,
        Request)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB, because computers use bytes not megabytes.
ALLOWED_EXTENSIONS = (".txt", ".log", ".logfile", ".data")

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



@app.post("/upload", tags=["Log Upload and Parsing"],status_code=status.HTTP_201_CREATED)
# use async def for better performance when handling file uploads, as it allows other requests to be processed while waiting for file I/O operations to complete.
async def upload_log(
   request: Request,
   file : UploadFile = File(...)
   
   ) -> Dict[str,Any]: # Even though File() also works, always use ... for mandatory fields.
   """
  Accepts, validates, and triages log files into Errors and Warnings.
    
    Logic Flow:
    1. Validation (Extension check)
    2. Size Verification (Request header and Seek method)
    3. Parsing (Streaming line-by-line....... to be implemented yet.........)
    4. Cleanup (Resource release, irrespective of success or failure)
   """
   # Step 1: Validate File and File Extension
   if not file.filename or not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST, 
           detail=f"Invalid file type. Please upload {ALLOWED_EXTENSIONS} files only."
           )
   # Step 2: Verify File Size put processing logic as well here to make sure we close the file is always properly closed
   actual_size = 0
   try:
        # Browsers usually send file size in request headers
        content_length = request.headers.get("content-length")

        if content_length is not None:
            if int(content_length) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File too large (max 20MB)"
                )
            
            #If content-length is not provided or is incorrect, we double-check using seek and tell methods.
            #This is important because relying solely on client-provided headers can be risky.
       
        #First  seek to the end of the file to get its size
       
        await file.file.seek(0,2)
       
        '''
        here, in file.seek(0,2) , the second argument '2' is used to indicate that the seek operation 
        should be performed relative to the end of the file. 1 in the second argument would indicate seeking 
        from the current position, and 0 would indicate seeking from the beginning of the file.
        The first argument '0' specifies the offset from that position, which means no additional offset is applied.
        '''
        
        actual_size = await file.file.tell() # tell() method returns the current position of the file pointer, which is equivalent to the size of the file after seeking to the end.

        await file.file.seek(0)
        '''
        BEST PRACTICE: Reset pointer to the beginning for subsequent operations. 
        In this case, we can do the file curser reset after verifying the size as well, just before parsing.
        This ensures that when we start reading the file for parsing, we begin from the start of the file. 
        We are doing this  before verifying if the file size is within limits to make sure if in future
        we need to send file to another service for processing, we don't miss any data. 
        '''
        if actual_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large (max 20MB)"
                )
    # Step 3: Parse the File for Errors and Warnings - Streaming Line-by-Line

   finally:
        await file.file.close() # Step 4: Cleanup - Ensure the file is closed after processing to free up resources.
    
   return{ 

        "filename":file.filename,
        "Size_in_Bytes": actual_size
        }