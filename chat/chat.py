from dataclasses import dataclass

CHAT_TYPE_AI: str = "システム"
CHAT_TYPE_USER: str = "ユーザー"


@dataclass
class ChatData:
    type: str
    text: str

    @classmethod
    def from_data(cls, type: str, text: str) -> "ChatData":
        if type not in [CHAT_TYPE_AI, CHAT_TYPE_USER]:
            raise TypeError("ChatDataのtypeは、ai or userを指定すること。")
        return cls(
            type=type, text=text
        )