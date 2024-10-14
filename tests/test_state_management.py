import pytest
from main import pdf_storage

def test_pdf_storage_initially_empty():
    assert len(pdf_storage) == 0, "PDF storage should be empty at the start."

def test_pdf_storage_insert():
    pdf_id = "12345"
    pdf_data = {"filename": "sample.pdf", "pdf_text_chunks": ["Chunk 1", "Chunk 2"]}
    pdf_storage[pdf_id] = pdf_data

    assert pdf_id in pdf_storage, "PDF ID was not added to storage."
    assert pdf_storage[pdf_id]["filename"] == "sample.pdf", "Filename mismatch in storage."
    assert len(pdf_storage[pdf_id]["pdf_text_chunks"]) == 2, "PDF chunks mismatch in storage."
