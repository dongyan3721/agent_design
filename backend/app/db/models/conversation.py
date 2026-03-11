"""Conversation and message models for AI chat persistence (MongoDB)."""

from datetime import UTC, datetime
from typing import Literal, Optional

from beanie import Document
from pydantic import Field


class ToolCall(Document):
    """ToolCall document model - record of a tool invocation."""

    message_id: str
    tool_call_id: str
    tool_name: str
    args: dict = Field(default_factory=dict)
    result: Optional[str] = None
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None

    class Settings:
        name = "tool_calls"
        indexes = ["message_id"]


class Message(Document):
    """Message document model - individual message in a conversation."""

    conversation_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    model_name: Optional[str] = None
    tokens_used: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "messages"
        indexes = ["conversation_id"]


class Conversation(Document):
    """Conversation document model - groups messages in a chat session."""

    user_id: Optional[str] = None
    title: Optional[str] = None
    is_archived: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "conversations"
        indexes = ["user_id"]
