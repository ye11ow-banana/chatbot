from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import repository
from .models import Message


@receiver(post_save, sender=Message)
def set_chat_last_update(
    sender: Message, instance: Message, created: bool, **kwargs: Any
) -> None:
    if created:
        repository.set_chat_last_update(
            str(instance.chat_id), instance.created
        )
