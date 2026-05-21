from django.contrib import admin
from django.utils import timezone

from chatbot.models import ChatMessage, ChatSession, KnowledgeSource
from chatbot.services.chunking import chunk_text
from chatbot.services.ingestion_service import IngestionService
from chatbot.services.vector_store import get_chroma_service


@admin.register(KnowledgeSource)
class KnowledgeSourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "source_type",
        "chunk_count",
        "is_active",
        "indexed_at",
        "updated_at",
    )
    list_filter = ("source_type", "is_active")
    search_fields = ("title", "content")
    readonly_fields = (
        "content_hash",
        "original_filename",
        "file_size",
        "chunk_count",
        "indexed_at",
    )
    actions = ("index_selected_sources",)

    def save_model(self, request, obj, form, change):
        """Keep manually entered admin content searchable after save."""
        obj.content_hash = IngestionService._hash_text(obj.content)
        obj.chunk_count = len(chunk_text(obj.content))
        obj.indexed_at = timezone.now()
        super().save_model(request, obj, form, change)
        if obj.is_active:
            get_chroma_service().upsert_source(obj)

    @admin.action(description="Index selected chatbot knowledge in ChromaDB")
    def index_selected_sources(self, request, queryset):
        indexed = 0
        for source in queryset.filter(is_active=True):
            source.content_hash = IngestionService._hash_text(source.content)
            source.chunk_count = len(chunk_text(source.content))
            source.indexed_at = timezone.now()
            source.save(update_fields=["content_hash", "chunk_count", "indexed_at"])
            get_chroma_service().upsert_source(source)
            indexed += 1
        self.message_user(request, f"Indexed {indexed} knowledge source(s).")


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "created_at", "updated_at")
    search_fields = ("session_key",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("content",)
