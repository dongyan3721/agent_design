"""Conversation repository (MongoDB).

Contains database operations for Conversation, Message, and ToolCall entities.
"""

from datetime import UTC, datetime

from app.db.models.conversation import Conversation, Message, ToolCall


# =============================================================================
# Conversation Operations
# =============================================================================


async def get_conversation_by_id(
    conversation_id: str,
    *,
    include_messages: bool = False,
) -> Conversation | None:
    """Get conversation by ID."""
    conversation = await Conversation.get(conversation_id)
    # Note: MongoDB doesn't auto-load related documents; handle in service layer
    return conversation


async def get_conversations_by_user(
    user_id: str | None = None,
    *,
    skip: int = 0,
    limit: int = 50,
    include_archived: bool = False,
) -> list[Conversation]:
    """Get conversations for a user with pagination."""
    query_filter = {}
    if user_id:
        query_filter["user_id"] = user_id
    if not include_archived:
        query_filter["is_archived"] = False

    return await Conversation.find(query_filter).sort("-created_at").skip(skip).limit(limit).to_list()


async def count_conversations(
    user_id: str | None = None,
    *,
    include_archived: bool = False,
) -> int:
    """Count conversations for a user."""
    query_filter = {}
    if user_id:
        query_filter["user_id"] = user_id
    if not include_archived:
        query_filter["is_archived"] = False

    return await Conversation.find(query_filter).count()


async def create_conversation(
    *,
    user_id: str | None = None,
    title: str | None = None,
) -> Conversation:
    """Create a new conversation."""
    conversation = Conversation(
        user_id=user_id,
        title=title,
    )
    await conversation.insert()
    return conversation


async def update_conversation(
    *,
    db_conversation: Conversation,
    update_data: dict,
) -> Conversation:
    """Update a conversation."""
    for field, value in update_data.items():
        setattr(db_conversation, field, value)
    db_conversation.updated_at = datetime.now(UTC)
    await db_conversation.save()
    return db_conversation


async def archive_conversation(
    conversation_id: str,
) -> Conversation | None:
    """Archive a conversation."""
    conversation = await get_conversation_by_id(conversation_id)
    if conversation:
        conversation.is_archived = True
        conversation.updated_at = datetime.now(UTC)
        await conversation.save()
    return conversation


async def delete_conversation(conversation_id: str) -> bool:
    """Delete a conversation and all related messages/tool_calls."""
    conversation = await get_conversation_by_id(conversation_id)
    if conversation:
        # Delete related messages and tool calls
        messages = await get_messages_by_conversation(str(conversation.id))
        for message in messages:
            await ToolCall.find(ToolCall.message_id == str(message.id)).delete()
        await Message.find(Message.conversation_id == str(conversation.id)).delete()
        await conversation.delete()
        return True
    return False


# =============================================================================
# Message Operations
# =============================================================================


async def get_message_by_id(message_id: str) -> Message | None:
    """Get message by ID."""
    return await Message.get(message_id)


async def get_messages_by_conversation(
    conversation_id: str,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[Message]:
    """Get messages for a conversation with pagination."""
    return await (
        Message.find(Message.conversation_id == conversation_id)
        .sort("created_at")
        .skip(skip)
        .limit(limit)
        .to_list()
    )


async def count_messages(conversation_id: str) -> int:
    """Count messages in a conversation."""
    return await Message.find(Message.conversation_id == conversation_id).count()


async def create_message(
    *,
    conversation_id: str,
    role: str,
    content: str,
    model_name: str | None = None,
    tokens_used: int | None = None,
) -> Message:
    """Create a new message."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        model_name=model_name,
        tokens_used=tokens_used,
    )
    await message.insert()

    # Update conversation's updated_at timestamp
    conversation = await get_conversation_by_id(conversation_id)
    if conversation:
        conversation.updated_at = datetime.now(UTC)
        await conversation.save()

    return message


async def delete_message(message_id: str) -> bool:
    """Delete a message and its tool calls."""
    message = await get_message_by_id(message_id)
    if message:
        await ToolCall.find(ToolCall.message_id == str(message.id)).delete()
        await message.delete()
        return True
    return False


# =============================================================================
# ToolCall Operations
# =============================================================================


async def get_tool_call_by_id(tool_call_id: str) -> ToolCall | None:
    """Get tool call by ID."""
    return await ToolCall.get(tool_call_id)


async def get_tool_calls_by_message(
    message_id: str,
) -> list[ToolCall]:
    """Get tool calls for a message."""
    return await (
        ToolCall.find(ToolCall.message_id == message_id)
        .sort("started_at")
        .to_list()
    )


async def create_tool_call(
    *,
    message_id: str,
    tool_call_id: str,
    tool_name: str,
    args: dict,
    started_at: datetime,
) -> ToolCall:
    """Create a new tool call record."""
    tool_call = ToolCall(
        message_id=message_id,
        tool_call_id=tool_call_id,
        tool_name=tool_name,
        args=args,
        started_at=started_at,
        status="running",
    )
    await tool_call.insert()
    return tool_call


async def complete_tool_call(
    *,
    db_tool_call: ToolCall,
    result: str,
    completed_at: datetime,
    success: bool = True,
) -> ToolCall:
    """Mark a tool call as completed."""
    db_tool_call.result = result
    db_tool_call.completed_at = completed_at
    db_tool_call.status = "completed" if success else "failed"

    # Calculate duration
    if db_tool_call.started_at:
        delta = completed_at - db_tool_call.started_at
        db_tool_call.duration_ms = int(delta.total_seconds() * 1000)

    await db_tool_call.save()
    return db_tool_call
