from django.db.models import QuerySet, F

from chats.models import Chat, Message


def get_chat_messages(chat_id: str) -> QuerySet[Message]:
    chat_messages = Message.objects.filter(chat_id=chat_id)
    chat_messages = chat_messages.annotate(
        chat_title=F("chat__title"), sender_username=F("sender__username")
    )
    return chat_messages.only("text", "created")


def get_chat_title(chat_id: str) -> str:
    return Chat.objects.filter(id=chat_id).only("title").get().title


def bulk_create_messages(messages: tuple[tuple, ...]) -> None:
    message_instances = []
    for message in messages:
        sender_id, chat_id, text = message
        message_instances.append(Message(
            sender_id=sender_id,
            chat_id=chat_id,
            text=text,
        ))
    Message.objects.bulk_create(message_instances)
