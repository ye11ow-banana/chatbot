from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from chats.models import Chat, Message

User = get_user_model()


class ChatListViewTest(TestCase):
    def setUp(self):
        self.url = reverse("chat_list")
        self.client = Client()
        self.user = User.objects.create_user(
            username="username1", password="password1"
        )
        self.chat1 = Chat.objects.create(
            owner=self.user, title="Conversation 1"
        )
        self.chat2 = Chat.objects.create(
            owner=self.user, title="Conversation 2"
        )

    def test_authentication_required(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=%2Fchats%2F", 302, 404
        )

    def test_POST(self):
        self.client.login(username=self.user.username, password="password1")
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 405)

    def test_GET(self):
        self.client.login(username=self.user.username, password="password1")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/chat_list.html")
        self.assertEquals(len(response.context["chats"]), 2)
        self.assertEquals(response.context["chats"][0], self.chat1)
        self.assertEquals(response.context["chats"][1], self.chat2)


class ChatMessagesViewTest(TestCase):
    def setUp(self):
        self.url = reverse("chat_messages", args=(1,))
        self.client = Client()
        self.user = User.objects.create_user(
            username="username1", password="password1"
        )
        self.chat = Chat.objects.create(
            owner=self.user, title="Conversation 1"
        )
        self.message1 = Message.objects.create(
            sender=self.user, chat=self.chat, text="Text 1"
        )
        self.message2 = Message.objects.create(chat=self.chat, text="Text 2")

    def test_authentication_required(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=%2Fchats%2F1%2F", 302, 404
        )

    def test_POST(self):
        self.client.login(username=self.user.username, password="password1")
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 405)

    def test_GET(self):
        chat = Chat.objects.create(owner=self.user, title="Conversation 1")
        Message.objects.create(chat=chat, text="Text 3")
        self.client.login(username=self.user.username, password="password1")
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "chats/chat.html")
        self.assertEquals(response.context["chat"], self.chat)
        self.assertEquals(len(response.context["messages"]), 2)
        self.assertEquals(response.context["messages"][0], self.message1)
        self.assertEquals(response.context["messages"][1], self.message2)
