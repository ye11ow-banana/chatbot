from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from .permissions import ChatOwnerRequired
from .services import repository
from .models import Chat, Message


class ChatListView(LoginRequiredMixin, ListView):
    context_object_name = "chats"
    template_name = "chats/chat_list.html"

    def get_queryset(self) -> QuerySet[Chat]:
        user_id = self.request.user.id
        return repository.get_user_chats(user_id)


class ChatMessagesView(LoginRequiredMixin, ChatOwnerRequired, ListView):
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
