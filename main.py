import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from src.useful_functions import get_pdf_text, get_text_chunks, call_gemini
from src.models import ChatResponse, ChatRequest
from src.error_handling_middleware import CustomErrorHandlingMiddleware

from typing import Dict
from PyPDF2 import PdfReader
from loguru import logger


# Logger configuration
logger.add("logs/app.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB", compression="zip", serialize=True)

app = FastAPI()

# Add the custom error handling middleware
app.add_middleware(CustomErrorHandlingMiddleware)

# PDF storage
pdf_storage: Dict[str, Dict] = {}

MAX_FILE_SIZE = 10 * 1024 * 1024

@app.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Description:
    Handles PDF file uploads. Validates the file type and size, extracts text from the PDF, and stores the extracted content in memory.

    Parameters:
    file (UploadFile): The uploaded PDF file, provided as a multipart form-data file.
    
    Returns:
    JSONResponse: A response containing the unique identifier (pdf_id) of the uploaded PDF.
    
    Raises:
    HTTPException:
    400 if the uploaded file is not a PDF.
    400 if the file size exceeds the maximum limit of 10 MB.
    500 if an error occurs during PDF processing.
    """

    logger.info(f"Received file upload request for file: {file.filename}")
    # File type validation
    if not file.filename.endswith(".pdf"):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    
    file_size = await file.read()
    if len(file_size) > MAX_FILE_SIZE:
        logger.warning(f"File size too large: {len(file_size)} bytes")
        raise HTTPException(status_code=400, detail="File size is too large. Only 10 MB or less files are accepted.")

    pdf_id = str(uuid.uuid4())[:8]

    try:
        logger.debug(f"Processing PDF with ID: {pdf_id}")
        pdf_reader = PdfReader(file.file)
        pdf_text = get_pdf_text(pdf_reader)
        pdf_pages = len(pdf_reader.pages)
        text_chunks = get_text_chunks(pdf_text)

        pdf_storage[pdf_id] = {
            "filename": file.filename,
            "pdf_pages": pdf_pages,
            "pdf_text_chunks": text_chunks,
        }
        logger.info(f"PDF processed successfully. PDF ID: {pdf_id}")
        return JSONResponse(content={"pdf_id": pdf_id})
    
    except Exception as e:
        logger.error(f"Error during PDF processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during processing file: {str(e)}")


@app.post("/v1/chat/{pdf_id}", response_model=ChatResponse)
async def chat_with_pdf(pdf_id: str, request: ChatRequest):
    """
    Description:
    Processes a chat request associated with a previously uploaded PDF. Retrieves the stored content and interacts with the Gemini API to generate a response based on the user's message.

    Parameters:
    pdf_id (str): The unique identifier of the PDF to interact with.
    request (ChatRequest): An object containing the user's message.
    
    Returns:
    ChatResponse: A response containing the generated chat response from the Gemini API.
    
    Raises:
    HTTPException:
    400 if the PDF with the provided ID is not found.
    400 if the PDF content could not be extracted.
    500 if an error occurs during the chat processing.
    """
    logger.info(f"Received chat request for PDF ID: {pdf_id} with message: {request.message}")

    pdf_data = pdf_storage.get(pdf_id)
    if not pdf_data:
        logger.warning(f"PDF with ID {pdf_id} not found")
        raise HTTPException(status_code=400, detail="PDF is not found")
    
    pdf_chunks = pdf_data.get("pdf_text_chunks", "")
    if not pdf_chunks:
        logger.warning(f"Failed to extract PDF content for ID: {pdf_id}")
        raise HTTPException(status_code=400, detail="Failed to extract PDF content")
    
    try:
        response = call_gemini(chunks=pdf_chunks, user_message=request.message)
        logger.info(f"Chat response generated for PDF ID: {pdf_id}")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error during chat with PDF ID {pdf_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")
