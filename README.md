**AI Assistant**

### Short description
This is chatbot application created with
websocket, langchain and Chroma. Main functionality
of the AI is located in /apps/chats/services/chatbot.py.
Bot have common history for user from all chats saved in Chroma DB.
Also, there are some tests, permissions, signals etc. in the app.

# Installation

```sh
git clone https://github.com/ye11ow-banana/chatbot.git
```

Install dependencies to your virtual environment
```sh
poetry install
```

Set environment variables to .env file
```sh
OPENAI_API_KEY=
```
```sh
SECRET_KEY=
```

### Run Django
```sh
python3 manage.py migrate
```
```sh
python3 manage.py test chats
```
```sh
python3 manage.py loaddata data.json
```
```sh
python3 manage.py runserver
```

---

### Steps to check functionality

1. Login as admin (password - admin)
    ```sh
    http://127.0.0.1:8000/admin/
    ```
2. Check all chats
    ```sh
    http://127.0.0.1:8000/chats/
    ```
3. Check messages in chats (You can ask the bot something)
    ```sh
    http://127.0.0.1:8000/chats/1/
    ```
    ```sh
    http://127.0.0.1:8000/chats/2/
    ```
4. Login as john (password - john)
    ```sh
    http://127.0.0.1:8000/admin/
    ```
5. Check messages in chat (You can ask the bot something)
    ```sh
    http://127.0.0.1:8000/chats/3/
    ```

Have a good day :)
