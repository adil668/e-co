import json
import re

from django.http import HttpRequest


def clean_text(value: str) -> str:
    """Normalize whitespace before embedding or returning text."""
    return re.sub(r"\s+", " ", value or "").strip()


def parse_json_body(request: HttpRequest) -> dict:
    """Read JSON safely from a Django request body."""
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def truncate_text(value: str, max_chars: int = 1200) -> str:
    """Keep responses compact for a lightweight chatbot."""
    value = clean_text(value)
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def split_text_chunks(text: str, chunk_words: int = 180, overlap_words: int = 30) -> list[str]:
    """Split long content into overlapping chunks for better semantic retrieval."""
    from chatbot.services.chunking import chunk_text

    return chunk_text(text, chunk_words=chunk_words, overlap_words=overlap_words)
