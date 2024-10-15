# Gemini PDF Query

## Project Overview

The PDF Chat Service is a FastAPI application that allows users to upload PDF files and interact with their contents through a conversational interface. Utilizing natural language processing, the service extracts text from uploaded PDFs, processes it, and provides responses to user queries based on the extracted content.

## Detailed Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Virtual Environment (optional but recommended)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone git@github.com:MuratShadol/Gemini-PDF-Query.git
   cd Gemini-PDF-Query

2. **Set up a virtual environment (optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt

4. **Configure environment variables: Create a .env file in the root directory and add your API key**:
   ```plaintext
   API_KEY=your_api_key_here

5. **Start the application**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000

## Environment Configuration
Make sure to set up your environment correctly. The following environment variables should be configured:
- `API_KEY`: Your API key for the Gemini model.

## API Endpoints

### Upload PDF
- **Endpoint**: `/v1/pdf`
- **Method**: `POST`

#### Request:
- **File**: Upload a PDF file.

#### Response:
- **Success**: Returns a JSON object with the PDF ID.
    ```json
    {
        "pdf_id": "12345678"
    }
    ```
- **Error**: Returns an error message for invalid files or sizes.
    ```json
    {
        "detail": "Invalid file type. Only PDF files are accepted."
    }
    ```

### Chat with PDF
- **Endpoint**: `/v1/chat/{pdf_id}`
- **Method**: `POST`

#### Request:
- **Body**:
    ```json
    {
        "message": "Your question here"
    }
    ```

#### Response:
- **Success**: Returns a JSON object with the chat response.
    ```json
    {
        "response": "This is the answer based on the PDF content."
    }
    ```
- **Error**: Returns an error message if the PDF is not found.
    ```json
    {
        "detail": "PDF is not found"
    }
    ```

## Testing Procedures

### Running the Test Suite
To run the test suite, ensure you have all dependencies installed, then execute the following command:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000
  ```

## Test Coverage

The project includes unit tests for core functions such as PDF text extraction, chunking, and Gemini API interaction. Ensure that you have a test PDF file available in the tests directory for the tests to execute successfully.

## Example Tests

The test suite includes tests for:
- PDF text extraction
- Text chunking functionality
- API interactions with mocked responses

