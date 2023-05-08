from django.db.models import QuerySet, F

from .models import Message


def get_chat_messages(chat_id: str) -> QuerySet[Message]:
    chat_messages = Message.objects.filter(chat_id=chat_id)
    chat_messages = chat_messages.annotate(
        chat_title=F("chat__title"), sender_username=F("sender__username")
    )
    return chat_messages.only("text", "created")
