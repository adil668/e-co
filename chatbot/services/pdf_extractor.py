from io import BytesIO


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract readable text from a PDF upload.

    The pypdf import stays inside this function so Django can still boot even
    before the optional PDF dependency is installed.
    """
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Install pypdf to ingest PDF files.") from exc

    reader = PdfReader(BytesIO(file_bytes))
    page_text = []
    for page in reader.pages:
        page_text.append(page.extract_text() or "")
    return "\n\n".join(page_text)
