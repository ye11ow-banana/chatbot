from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from . import services
from .models import Chat, Message


class ChatListView(LoginRequiredMixin, ListView):
    queryset = Chat.objects.all()
    context_object_name = "chats"
    template_name = "chats/chat_list.html"


class ChatMessagesView(LoginRequiredMixin, ListView):
    template_name = "chats/chat.html"
    context_object_name = "messages"

    def get_queryset(self) -> QuerySet[Message]:
        chat_pk = self.kwargs["pk"]
        return services.get_chat_messages(chat_pk)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        messages = context["messages"]
        context["chat"] = messages[0].chat
        return context


chat_list = ChatListView.as_view()
chat_messages = ChatMessagesView.as_view()
