from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .services import repository
from .models import Chat, Message


class ChatListView(LoginRequiredMixin, ListView):
    queryset = Chat.objects.all()
    context_object_name = "chats"
    template_name = "chats/chat_list.html"


class ChatMessagesView(LoginRequiredMixin, ListView):
    template_name = "chats/chat.html"
    context_object_name = "messages"

    def get_queryset(self) -> list[Message]:
        chat_pk = self.kwargs["pk"]
        return list(repository.get_chat_messages(chat_pk))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        chat_pk = self.kwargs["pk"]
        messages = context["messages"]
        try:
            chat_title = messages[0].chat_title
        except IndexError:
            chat_title = repository.get_chat_title(chat_pk)
        context["chat_title"] = chat_title
        context["chat_pk"] = chat_pk
        return context


chat_list = ChatListView.as_view()
chat_messages = ChatMessagesView.as_view()
