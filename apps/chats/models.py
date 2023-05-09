from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class Chat(models.Model):
    """
    Represents a chat with messages.
    """

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chats",
        verbose_name="Owner of a chat",
    )
    title = models.CharField("Chat title", max_length=255)
    created = models.DateTimeField(
        "Chat creation date and time", auto_now_add=True
    )
    updated = models.DateTimeField(
        "Chat last update date and time", auto_now=True
    )

    class Meta:
        db_table = "chat"

    def __str__(self) -> str:
        return f"Chat: {self.title}"


class Message(models.Model):
    """
    Message in a chat.
    """

    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="User that sent this message. Null if sent by chatbot",
        null=True,
        blank=True,
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Chat a message belongs to",
    )
    text = models.CharField("Message text", max_length=4096)
    created = models.DateTimeField(
        "Message creation date and time", auto_now_add=True
    )

    class Meta:
        db_table = "message"

    def __str__(self) -> str:
        return f"Message: {self.pk}"
