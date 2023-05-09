import json

from channels.generic.websocket import WebsocketConsumer

from chats.services import chatbot, repository


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data: str):
        user = self.scope["user"]
        chat_id = self.scope["url_route"]["kwargs"]["room_name"]
        message_data = json.loads(text_data)
        question = message_data.get("message", "")
        if not question:
            raise ValueError("question must be defined")
        history_chatbot = chatbot.HistoryChatBot(user.username)
        answer = history_chatbot.ask(question)
        self.send(text_data=json.dumps({"message": answer}))
        messages = (
            (user.id, chat_id, question),
            (None, chat_id, answer),
        )
        repository.bulk_create_messages(messages)
