import logging
from functools import lru_cache

from django.conf import settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Creates local embeddings with all-MiniLM-L6-v2."""

    def __init__(self) -> None:
        model_name = getattr(
            settings,
            "CHATBOT_EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        )
        self.model = SentenceTransformer(model_name)
        logger.info("Loaded chatbot embedding model: %s", model_name)

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embedding.tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    # Lazy singleton keeps startup fast and avoids loading the model twice.
    return EmbeddingService()
