import json
import logging

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from chatbot.services.chat_service import get_chat_service
from chatbot.services.ingestion_service import get_ingestion_service
from chatbot.services.vector_store import get_chroma_service
from chatbot.utils import clean_text, parse_json_body

logger = logging.getLogger(__name__)


@require_GET
def health(request: HttpRequest) -> JsonResponse:
    """Simple local readiness check for the chatbot backend."""
    try:
        chroma = get_chroma_service()
        return JsonResponse(
            {
                "status": "ok",
                "vector_store": "chromadb",
                "indexed_items": chroma.count(),
            }
        )
    except Exception as exc:
        logger.exception("Chatbot health check failed")
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)


@csrf_exempt
@require_POST
def chat(request: HttpRequest) -> JsonResponse:
    """JSON endpoint for semantic-search chatbot answers."""
    try:
        payload = parse_json_body(request)
        question = clean_text(payload.get("message", ""))
        if not question:
            return JsonResponse({"error": "Message is required."}, status=400)

        if not request.session.session_key:
            request.session.create()

        result = get_chat_service().answer(
            session_key=request.session.session_key,
            question=question,
        )
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)
    except Exception:
        logger.exception("Chatbot request failed")
        return JsonResponse(
            {"error": "Chatbot failed to process this message."},
            status=500,
        )


@csrf_exempt
@require_POST
def upload_knowledge(request: HttpRequest) -> JsonResponse:
    """Upload TXT/PDF files or pasted website text into the chatbot knowledge base."""
    try:
        service = get_ingestion_service()

        if "file" in request.FILES:
            result = service.ingest_uploaded_file(
                uploaded_file=request.FILES["file"],
                title=request.POST.get("title", ""),
                source_type=request.POST.get("source_type", "document"),
            )
        else:
            payload = parse_json_body(request)
            text = payload.get("text") or payload.get("content") or ""
            result = service.ingest_text(
                title=payload.get("title", "Website text"),
                text=text,
                source_type=payload.get("source_type", "page"),
                source_url=payload.get("source_url", ""),
            )

        source = result.source
        return JsonResponse(
            {
                "status": "ok",
                "duplicate": result.duplicate,
                "indexed_chunks": result.indexed_chunks,
                "source": {
                    "id": source.id,
                    "title": source.title,
                    "source_type": source.source_type,
                    "source_url": source.source_url,
                    "original_filename": source.original_filename,
                    "content_hash": source.content_hash,
                    "chunk_count": source.chunk_count,
                },
            },
            status=200 if result.duplicate else 201,
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except RuntimeError as exc:
        return JsonResponse({"error": str(exc)}, status=500)
    except Exception:
        logger.exception("Knowledge upload failed")
        return JsonResponse({"error": "Failed to ingest knowledge."}, status=500)
