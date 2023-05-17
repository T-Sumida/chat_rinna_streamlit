from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from chat import ChatData


class LLM:
    def __init__(self, cache_dir: str = "./") -> None:
        """Initialize

        Args:
            cache_dir (str, optional): モデルファイルの保存ディレクトリ. Defaults to "./".
        """
        self._tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", use_fast=False, cache_dir=cache_dir)
        self._model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-neox-3.6b-instruction-sft", device_map="auto", cache_dir=cache_dir)

    def generate_response(self, chat_history: List[ChatData]) -> str:
        """AIからの返答を生成する

        Args:
            chat_history (List[ChatData]): 最新の発話を含む会話履歴

        Returns:
            str: 返答
        """
        prompt = self._create_prompt(chat_history)

        token_ids = self._tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self._model.generate(
                token_ids.to(self._model.device),
                do_sample=True,
                max_new_tokens=128,
                temperature=0.7,
                pad_token_id=self._tokenizer.pad_token_id,
                bos_token_id=self._tokenizer.bos_token_id,
                eos_token_id=self._tokenizer.eos_token_id
            )
        output = self._tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
        return output.replace("<NL>", "\n")

    def _create_prompt(self, chat_history: List[ChatData]) -> str:
        """rinna/japanese-gpt-neox-3.6b-instruction-sftに入力するプロンプトを会話履歴から生成する

        Args:
            chat_history (List[ChatData]): 会話履歴

        Returns:
            str: プロンプト
        """
        messages = []
        for chat in chat_history:
            messages.append(f"{chat.type}: {chat.text}")
        
        prompt = "<NL>".join(messages)
        prompt = prompt + "<NL>"
        return prompt