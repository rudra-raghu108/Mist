"""Compatibility endpoints for the simplified frontend integration.

These handlers provide lightweight versions of the original prototype
endpoints (e.g. ``/api/chat``) so the React UI can operate against the
production-ready ``main.py`` FastAPI application.  They rely on the seeded
SQL FAQ knowledge base and keep in-memory history so chats feel stateful
without requiring authentication.
"""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, DefaultDict, Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.ai_service import ai_service
from app.services.faq_service import faq_service

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory store so the UI can render history without persisting to Mongo.
_chat_history: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
_chat_history_lock = asyncio.Lock()
_MAX_HISTORY_ITEMS = 200

_scraping_state: Dict[str, Any] = {
    "status": "idle",
    "last_started": None,
    "last_completed": None,
    "sources": [],
}

_registered_users: Dict[str, Dict[str, Any]] = {}

_DEFAULT_FALLBACK_RESPONSE = (
    "I'm here to help with SRM Institute of Science & Technology. Try asking"
    " about admissions, courses, campus life, placements, scholarships, or"
    " facilities for more specific guidance."
)


def _utc_timestamp() -> float:
    return datetime.utcnow().timestamp()


def _utc_iso() -> str:
    return datetime.utcnow().isoformat()


async def _record_history(user_id: str, entry: Dict[str, Any]) -> None:
    async with _chat_history_lock:
        history = _chat_history[user_id]
        history.append(entry)
        if len(history) > _MAX_HISTORY_ITEMS:
            # Retain only the most recent N items to keep memory bounded.
            del history[:-_MAX_HISTORY_ITEMS]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: Optional[str] = Field(None, min_length=1)


@router.post("/chat")
async def chat_endpoint(payload: ChatRequest) -> Dict[str, Any]:
    """Return an FAQ-grounded response compatible with the legacy endpoint."""

    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    user_id = (payload.user_id or "anonymous").strip() or "anonymous"
    user_timestamp = _utc_timestamp()

    await _record_history(
        user_id,
        {
            "id": f"{user_timestamp:.6f}",
            "type": "user",
            "message": message,
            "timestamp": user_timestamp,
        },
    )

    match = await faq_service.find_best_match(message)

    ai_result: Optional[Dict[str, Any]] = None
    try:
        ai_result = await ai_service.generate_response(user_message=message)
    except Exception:  # pragma: no cover - runtime safeguard
        logger.exception("AI service failed to generate response")

    response_text = _DEFAULT_FALLBACK_RESPONSE
    metadata: Optional[Dict[str, Any]] = None

    if ai_result and ai_result.get("content"):
        response_text = ai_result["content"].strip()

    if match:
        entry = match.entry
        metadata = {
            "faq_id": entry.id,
            "question": entry.question,
            "category": entry.category.value if entry.category else None,
            "tags": entry.tags or [],
            "score": round(match.score, 3),
        }
        if entry.source_name or entry.source_url:
            metadata["source"] = {
                "name": entry.source_name,
                "url": entry.source_url,
            }
        # Prefer the structured FAQ answer when OpenAI is unavailable
        if not ai_result or ai_result.get("model_used") == "knowledge-base":
            response_text = entry.answer.strip()
    elif ai_result and ai_result.get("knowledge_base"):
        kb = ai_result["knowledge_base"]
        metadata = {
            "question": kb.get("question"),
            "category": kb.get("category"),
            "tags": kb.get("tags", []),
            "score": kb.get("score"),
        }
        source_name = kb.get("source_name")
        source_url = kb.get("source_url")
        if source_name or source_url:
            metadata["source"] = {
                "name": source_name,
                "url": source_url,
            }

    ai_timestamp = _utc_timestamp()
    await _record_history(
        user_id,
        {
            "id": f"{ai_timestamp:.6f}",
            "type": "assistant",
            "message": response_text,
            "timestamp": ai_timestamp,
            "metadata": metadata,
        },
    )

    response: Dict[str, Any] = {
        "success": True,
        "response": response_text,
        "message": message,
        "user_id": user_id,
        "timestamp": ai_timestamp,
    }
    if metadata:
        response["source"] = metadata
    if ai_result:
        if "category" in ai_result and ai_result["category"]:
            response["category"] = ai_result["category"]
        if "model_used" in ai_result and ai_result["model_used"]:
            response["model"] = ai_result["model_used"]
        if "tokens_used" in ai_result and ai_result["tokens_used"]:
            response["tokens_used"] = ai_result["tokens_used"]
    return response


@router.get("/chat/history")
async def chat_history_endpoint(
    user_id: str = Query("anonymous"),
    limit: int = Query(50, ge=1, le=_MAX_HISTORY_ITEMS),
) -> Dict[str, Any]:
    """Return recent chat interactions for the provided user."""

    normalized_user_id = user_id.strip() or "anonymous"
    async with _chat_history_lock:
        history = list(_chat_history.get(normalized_user_id, []))

    return {
        "success": True,
        "history": history[-limit:],
        "total_messages": len(history),
    }


class UserCreateRequest(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    campus: Optional[str] = None


@router.post("/users")
async def create_user(payload: UserCreateRequest) -> Dict[str, Any]:
    """Register a lightweight user profile for analytics purposes."""

    user_id = payload.user_id or str(uuid4())
    profile = {
        "user_id": user_id,
        "name": payload.name,
        "email": payload.email,
        "campus": payload.campus,
        "created_at": _utc_iso(),
    }
    _registered_users[user_id] = profile
    return {"success": True, "user": profile}


@router.get("/analytics")
async def analytics_endpoint() -> Dict[str, Any]:
    """Expose basic engagement analytics for the dashboard widgets."""

    async with _chat_history_lock:
        total_messages = sum(len(history) for history in _chat_history.values())
        active_users = len(_chat_history)

    return {
        "success": True,
        "summary": {
            "active_users": active_users,
            "registered_users": len(_registered_users),
            "messages": total_messages,
        },
        "last_updated": _utc_iso(),
    }


@router.post("/ai/enhance")
async def ai_enhance_endpoint() -> Dict[str, Any]:
    """Simulate an AI knowledge refresh, mirroring the prototype behaviour."""

    completion_time = _utc_iso()
    return {
        "success": True,
        "message": "Knowledge base already synced with latest FAQ entries.",
        "completed_at": completion_time,
    }


@router.post("/ai-training")
async def ai_training_endpoint() -> Dict[str, Any]:
    """Stub endpoint to acknowledge custom training payloads."""

    return {
        "success": True,
        "message": "Training request received. FAQ knowledge base is ready.",
        "processed_at": _utc_iso(),
    }


@router.post("/scraping/start")
async def scraping_start_endpoint() -> Dict[str, Any]:
    """Pretend to kick off scraping so the UI can progress through onboarding."""

    started_at = _utc_iso()
    _scraping_state.update(
        {
            "status": "completed",
            "last_started": started_at,
            "last_completed": started_at,
            "sources": [
                {
                    "id": "faq_seed",
                    "name": "Seeded FAQ knowledge base",
                    "items": len(_registered_users) + 5,
                }
            ],
        }
    )
    return {"success": True, "started_at": started_at, "status": _scraping_state["status"]}


@router.get("/scraping/status")
async def scraping_status_endpoint() -> Dict[str, Any]:
    """Return the most recent scraping run metadata."""

    return {"success": True, **_scraping_state}


@router.get("/scraping/data/{source_id}")
async def scraping_data_endpoint(source_id: str) -> Dict[str, Any]:
    """Provide placeholder scraped content for dashboards."""

    return {
        "success": True,
        "source_id": source_id,
        "data": [
            {
                "title": "SRMIST Overview",
                "summary": (
                    "SRM Institute of Science & Technology is a leading private university with"
                    " multi-campus presence and strong placement records."
                ),
                "url": "https://www.srmist.edu.in/about/",
            }
        ],
        "fetched_at": _utc_iso(),
    }


@router.post("/scraping/source/{source_id}")
async def scraping_source_endpoint(source_id: str) -> Dict[str, Any]:
    """Acknowledge targeted scraping requests."""

    requested_at = _utc_iso()
    _scraping_state.update({"status": "completed", "last_completed": requested_at})
    return {
        "success": True,
        "source_id": source_id,
        "requested_at": requested_at,
        "status": _scraping_state["status"],
    }
