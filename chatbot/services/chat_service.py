import logging

from django.db import transaction

from chatbot.models import ChatMessage, ChatSession
from chatbot.services.semantic_search import (
    SemanticSearchService,
    get_semantic_search_service,
)
from chatbot.services.storefront_search import (
    StorefrontSearchService,
    get_storefront_search_service,
)
from chatbot.utils import truncate_text

logger = logging.getLogger(__name__)


class ChatService:
    """Builds a simple answer from semantic search results."""

    def __init__(
        self,
        search_service: SemanticSearchService,
        storefront_search_service: StorefrontSearchService,
    ) -> None:
        self.search_service = search_service
        self.storefront_search_service = storefront_search_service

    @transaction.atomic
    def answer(self, session_key: str, question: str) -> dict:
        session, _ = ChatSession.objects.get_or_create(session_key=session_key)
        matches = self.search_service.search(question)
        storefront_result = None if matches else self.storefront_search_service.answer(question)
        answer = storefront_result["answer"] if storefront_result else self._build_answer(matches)
        response_matches = storefront_result["matches"] if storefront_result else matches

        ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.USER,
            content=question,
        )
        ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.ASSISTANT,
            content=answer,
        )

        return {
            "answer": answer,
            "matches": response_matches,
            "history": self._recent_history(session),
        }

    def _build_answer(self, matches: list[dict]) -> str:
        if not matches:
            return (
                "I could not find a matching answer in the stored website content. "
                "Please contact support or try asking with different words."
            )

        best_match = matches[0]
        source_type = best_match["metadata"].get("source_type", "content")
        title = best_match["metadata"].get("title", "Matched content")
        content = truncate_text(best_match["content"])

        if source_type == "faq":
            return f"{content}\n\nSource: {title}"
        return f"Here is the closest matching information I found:\n\n{content}\n\nSource: {title}"

    @staticmethod
    def _recent_history(session: ChatSession) -> list[dict]:
        messages = session.messages.order_by("-created_at")[:10]
        return [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }
            for message in reversed(messages)
        ]


def get_chat_service() -> ChatService:
    return ChatService(
        search_service=get_semantic_search_service(),
        storefront_search_service=get_storefront_search_service(),
    )
