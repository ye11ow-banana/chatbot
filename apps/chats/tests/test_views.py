from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from chats.models import Chat

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
        self.assertEquals(response.context["chats"][0], self.chat1)
        self.assertEquals(response.context["chats"][1], self.chat2)
