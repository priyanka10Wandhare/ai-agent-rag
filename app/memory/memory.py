class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})

    def add_ai_message(self, message: str):
        self.history.append({"role": "assistant", "content": message})

    def get_context(self, limit: int = 4) -> str:
        recent = self.history[-limit:]
        context = ""

        for msg in recent:
            role = msg["role"].capitalize()
            context += f"{role}: {msg['content']}\n"

        return context.strip()
