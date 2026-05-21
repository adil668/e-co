from chatbot.utils import clean_text


def chunk_text(text: str, chunk_words: int = 180, overlap_words: int = 30) -> list[str]:
    """Split text into overlapping chunks for semantic search.

    180 words keeps each vector focused. 30 words overlap preserves context when
    an answer sits near a chunk boundary.
    """
    words = clean_text(text).split()
    if not words:
        return []
    if len(words) <= chunk_words:
        return [" ".join(words)]

    chunks = []
    step = chunk_words - overlap_words
    for start in range(0, len(words), step):
        chunk = words[start : start + chunk_words]
        if chunk:
            chunks.append(" ".join(chunk))
        if start + chunk_words >= len(words):
            break
    return chunks
