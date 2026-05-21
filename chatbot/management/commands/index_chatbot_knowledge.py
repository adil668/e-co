import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from chatbot.models import KnowledgeSource
from chatbot.services.chunking import chunk_text
from chatbot.services.ingestion_service import IngestionService
from chatbot.services.vector_store import get_chroma_service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Index active chatbot knowledge sources into local ChromaDB."

    def handle(self, *args, **options):
        chroma = get_chroma_service()
        sources = KnowledgeSource.objects.filter(is_active=True)

        indexed_count = 0
        for source in sources.iterator():
            source.content_hash = IngestionService._hash_text(source.content)
            source.chunk_count = len(chunk_text(source.content))
            chroma.upsert_source(source)
            source.indexed_at = timezone.now()
            source.save(update_fields=["content_hash", "chunk_count", "indexed_at"])
            indexed_count += 1

        logger.info("Indexed %s chatbot knowledge sources", indexed_count)
        self.stdout.write(
            self.style.SUCCESS(f"Indexed {indexed_count} chatbot knowledge sources.")
        )
