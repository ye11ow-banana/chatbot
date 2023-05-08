from django.urls import path

from .views import chat_list, chat_messages

urlpatterns = [
    path("", chat_list, name="chat_list"),
    path("<int:pk>/", chat_messages, name="chat_messages"),
]
