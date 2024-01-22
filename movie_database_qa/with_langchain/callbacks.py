from typing import Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler

from movie_database_qa.log import verbose


class LLMStartHandler(BaseCallbackHandler):
    def __init__(self) -> None:
        super().__init__()
        self.prompt = None

    from langchain_core.messages import BaseMessage

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        verbose("on_llm_start", prompts)

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any
    ) -> Any:
        """Run when Chat Model starts running."""
        verbose("on_chat_model_start", messages)
