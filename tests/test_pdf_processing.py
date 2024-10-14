import pytest
from PyPDF2 import PdfReader
from src.useful_functions import get_pdf_text, get_text_chunks


@pytest.fixture
def sample_pdf():
    reader = PdfReader("C:\\Users\\gghho\\Downloads\\Shadol_CV.pdf") 
    return reader

def test_get_pdf_text(sample_pdf):
    text = get_pdf_text(sample_pdf)
    assert text != "", "PDF text extraction failed. Text is empty."
    assert "Murat" in text, "Expected content not found in PDF."

def test_get_text_chunks():
    text = "This is a test document. " * 100  # Mock large text
    chunks = get_text_chunks(text)
    assert len(chunks) > 1, "Text splitting did not work as expected."
    assert all(len(chunk) <= 1000 for chunk in chunks), "Chunk size exceeded limit."
