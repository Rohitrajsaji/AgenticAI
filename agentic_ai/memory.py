from typing import List, Dict, Any


class ShortTermMemory:
    def __init__(self, max_messages: int = 60):
        self.max_messages = max_messages
        self.messages: List[Dict[str, Any]] = []

    def add(self, message: Dict[str, Any]):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get(self) -> List[Dict[str, Any]]:
        return list(self.messages)
