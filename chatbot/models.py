from django.db import models


class KnowledgeSource(models.Model):
    """Website, FAQ, or project content that can be searched semantically."""

    class SourceType(models.TextChoices):
        FAQ = "faq", "FAQ"
        PAGE = "page", "Website Page"
        DOCUMENT = "document", "Document"

    title = models.CharField(max_length=200)
    content = models.TextField()
    content_hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        blank=True,
        editable=False,
    )
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        default=SourceType.FAQ,
    )
    source_url = models.CharField(max_length=500, blank=True)
    original_filename = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    chunk_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    indexed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class ChatSession(models.Model):
    """A lightweight record linked to Django's browser session key."""

    session_key = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.session_key


class ChatMessage(models.Model):
    """Stores current-session chat history in SQLite."""

    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    session = models.ForeignKey(
        ChatSession,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:40]}"
