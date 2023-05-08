from django.db.models import QuerySet

from .models import Message


def get_chat_messages(chat_id: str) -> QuerySet[Message]:
    chat_messages = Message.objects.filter(chat_id=chat_id)
    return chat_messages.select_related("chat").defer("created")
