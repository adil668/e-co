import hashlib
import logging
from dataclasses import dataclass

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.utils import timezone

from chatbot.models import KnowledgeSource
from chatbot.services.chunking import chunk_text
from chatbot.services.pdf_extractor import extract_pdf_text
from chatbot.services.vector_store import get_chroma_service
from chatbot.utils import clean_text

logger = logging.getLogger(__name__)


@dataclass
class IngestionResult:
    source: KnowledgeSource
    duplicate: bool
    indexed_chunks: int


class IngestionService:
    """Turns uploaded or pasted content into searchable chatbot knowledge."""

    def ingest_uploaded_file(
        self,
        uploaded_file: UploadedFile,
        title: str = "",
        source_type: str = KnowledgeSource.SourceType.DOCUMENT,
    ) -> IngestionResult:
        file_bytes = b"".join(uploaded_file.chunks())
        filename = uploaded_file.name or "uploaded-file"
        text = self._extract_file_text(filename, file_bytes)
        return self.ingest_text(
            title=title or filename,
            text=text,
            source_type=source_type,
            original_filename=filename,
            file_size=uploaded_file.size,
        )

    @transaction.atomic
    def ingest_text(
        self,
        title: str,
        text: str,
        source_type: str = KnowledgeSource.SourceType.PAGE,
        source_url: str = "",
        original_filename: str = "",
        file_size: int = 0,
    ) -> IngestionResult:
        content = clean_text(text)
        if not content:
            raise ValueError("No readable text was found.")

        content_hash = self._hash_text(content)
        existing = KnowledgeSource.objects.filter(content_hash=content_hash).first()
        if existing:
            return IngestionResult(source=existing, duplicate=True, indexed_chunks=existing.chunk_count)

        chunks = chunk_text(content)
        source = KnowledgeSource.objects.create(
            title=clean_text(title) or "Untitled knowledge source",
            content=content,
            content_hash=content_hash,
            source_type=source_type,
            source_url=source_url,
            original_filename=original_filename,
            file_size=file_size,
            chunk_count=len(chunks),
            indexed_at=timezone.now(),
        )

        get_chroma_service().upsert_source(source)
        logger.info("Ingested knowledge source %s with %s chunks", source.id, len(chunks))
        return IngestionResult(source=source, duplicate=False, indexed_chunks=len(chunks))

    @staticmethod
    def _hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def _extract_file_text(filename: str, file_bytes: bytes) -> str:
        lowered = filename.lower()
        if lowered.endswith(".txt") or lowered.endswith(".md"):
            return file_bytes.decode("utf-8", errors="ignore")
        if lowered.endswith(".pdf"):
            return extract_pdf_text(file_bytes)
        raise ValueError("Only TXT, Markdown, and PDF files are supported.")


def get_ingestion_service() -> IngestionService:
    return IngestionService()
