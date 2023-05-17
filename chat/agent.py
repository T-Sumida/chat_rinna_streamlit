from typing import List

from chat import ChatData, CHAT_TYPE_USER, CHAT_TYPE_AI
from llm import LLM


_CHAT_CONVERSATION_LIMIT: int = 100


class Agent:
    def __init__(self) -> None:
        self._conv_history: List[ChatData] = []
        self._llm = LLM()

    def run(self, user_input: str) -> List:
        self._conv_history.append(ChatData.from_data(CHAT_TYPE_USER, user_input))

        response = self._llm.generate_response(self._conv_history)

        self._conv_history.append(ChatData.from_data(CHAT_TYPE_AI, response))

        if len(self._conv_history) > _CHAT_CONVERSATION_LIMIT:
            self._conv_history.pop(0)

        return self._conv_history

    def get_conv_history(self) -> List[ChatData]:
        return self._conv_history