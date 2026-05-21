import logging
from functools import lru_cache

import chromadb
from django.conf import settings

from chatbot.models import KnowledgeSource
from chatbot.services.embedding_service import EmbeddingService, get_embedding_service
from chatbot.services.chunking import chunk_text

logger = logging.getLogger(__name__)


class ChromaService:
    """Small wrapper around local persistent ChromaDB."""

    def __init__(self, embedding_service: EmbeddingService) -> None:
        self.embedding_service = embedding_service
        self.client = chromadb.PersistentClient(path=str(settings.CHATBOT_CHROMA_PATH))
        self.collection = self.client.get_or_create_collection(
            name=settings.CHATBOT_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("Chatbot Chroma collection ready: %s", settings.CHATBOT_COLLECTION_NAME)

    def upsert_source(self, source: KnowledgeSource) -> None:
        """Store one searchable content item in ChromaDB."""
        chunks = chunk_text(source.content)
        if not chunks:
            return

        # Remove older chunks for this source before writing the fresh version.
        self.collection.delete(where={"django_id": source.id})

        self.collection.upsert(
            ids=[self._source_id(source.id, index) for index, _ in enumerate(chunks)],
            documents=chunks,
            embeddings=self.embedding_service.embed_many(chunks),
            metadatas=[
                {
                    "django_id": source.id,
                    "title": source.title,
                    "source_type": source.source_type,
                    "source_url": source.source_url,
                    "chunk_index": index,
                    "content_hash": source.content_hash,
                    "original_filename": source.original_filename,
                }
                for index, _ in enumerate(chunks)
            ],
        )

    def search(self, query: str, top_k: int, min_score: float) -> list[dict]:
        """Return top semantic matches from locally stored embeddings."""
        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_embeddings=[self.embedding_service.embed(query)],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        matches = []
        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        for item_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            score = max(0.0, min(1.0, 1.0 - float(distance)))
            if score < min_score:
                continue
            matches.append(
                {
                    "id": item_id,
                    "content": document,
                    "metadata": metadata or {},
                    "score": round(score, 4),
                }
            )
        return matches

    def count(self) -> int:
        return self.collection.count()

    @staticmethod
    def _source_id(source_id: int, chunk_index: int) -> str:
        return f"knowledge-source-{source_id}-chunk-{chunk_index}"


@lru_cache(maxsize=1)
def get_chroma_service() -> ChromaService:
    return ChromaService(embedding_service=get_embedding_service())
