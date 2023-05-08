from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Chat


class ChatListView(LoginRequiredMixin, ListView):
    queryset = Chat.objects.all()
    context_object_name = "chats"
    template_name = "chats/chat_list.html"


chat_list = ChatListView.as_view()
