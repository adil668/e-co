from django.conf import settings

from chatbot.services.vector_store import ChromaService, get_chroma_service
from chatbot.utils import clean_text


class SemanticSearchService:
    """Finds the most relevant stored website/project content."""

    def __init__(self, chroma: ChromaService) -> None:
        self.chroma = chroma

    def search(self, question: str) -> list[dict]:
        question = clean_text(question)
        if not question:
            return []
        return self.chroma.search(
            query=question,
            top_k=settings.CHATBOT_TOP_K,
            min_score=settings.CHATBOT_MIN_SCORE,
        )


def get_semantic_search_service() -> SemanticSearchService:
    return SemanticSearchService(chroma=get_chroma_service())
