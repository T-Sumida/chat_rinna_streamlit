from typing import Dict, List

import yaml
import streamlit as st
from streamlit_chat import message
from yaml.loader import SafeLoader

from agent import Agent
from chat import ChatData, CHAT_TYPE_AI


CONFIG_PATH = "./config/auth.yaml"
_CHAT_LATEST: str = "latest_chat"


def load_config() -> Dict:
    """認証情報を読み込む
    Returns:
        Dict: 認証情報
    """
    with open(CONFIG_PATH) as file:
        config = yaml.load(file, Loader=SafeLoader)


    for k in config["credentials"]["usernames"]:
        password = config["credentials"]["usernames"][k]["password"]
        config["credentials"]["usernames"][k]["password"] = stauth.Hasher([password]).generate()[0]
    return config


def chat_prompt():
    """Agentを起動する。
    """

    def get_text() -> str:
        input_text = st.text_input("You: ","", key="input")
        return input_text

    st.title("ChatBot")

    if "agent" not in st.session_state:
        st.session_state["agent"]: Agent = Agent()
    if _CHAT_LATEST not in st.session_state:
        st.session_state[_CHAT_LATEST] = "initialize"

    user_input = get_text()

    # テキスト入力がある かつ 前回と同じテキストでない場合
    if user_input and st.session_state[_CHAT_LATEST] != user_input:
        st.session_state[_CHAT_LATEST] = user_input #NOTE テキスト入力が連続で発生するのを防いでいる。
        st.session_state["agent"].run(user_input)

    conv_history = st.session_state["agent"].get_conv_history()
    show_conv(conv_history)


def show_conv(conv_history: List[ChatData]):
    """会話履歴をブラウザに描画する。
    Args:
        conv_history (List[ChatData]): 会話履歴のリスト
    """
    for i in range(len(conv_history)-1, -1, -1):
        if conv_history[i].type == CHAT_TYPE_AI:
            message(conv_history[i].text, key=str(i))
        else:
            message(conv_history[i].text, is_user=True, key=str(i) + '_user')


def main() -> None:
    """デモチャットを起動
    """
    chat_prompt()


if __name__ == "__main__":
    main()