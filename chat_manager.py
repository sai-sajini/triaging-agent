import uuid

class ChatManager:
    def __init__(self):
        self.chats = {}  # chat_id: list of messages
        self.active_chat_id = None

    def new_chat(self):
        chat_id = str(uuid.uuid4())
        self.chats[chat_id] = []
        self.active_chat_id = chat_id
        return chat_id

    def get_active_chat_id(self):
        return self.active_chat_id

    def set_active_chat(self, chat_id):
        if chat_id in self.chats:
            self.active_chat_id = chat_id

    def add_message(self, role, content):
        if self.active_chat_id:
            self.chats[self.active_chat_id].append({"role": role, "content": content})

    def get_chat_history(self, chat_id=None):
        chat_id = chat_id or self.active_chat_id
        return self.chats.get(chat_id, [])

    def get_all_chats(self):
        return list(self.chats.keys())

    def get_chat_title(self, chat_id):
        # Use first user message as title, or chat_id if empty
        history = self.chats.get(chat_id, [])
        for msg in history:
            if msg["role"] == "user":
                return msg["content"][:30] + ("..." if len(msg["content"]) > 30 else "")
        return chat_id[:8]
