import itertools
from typing import List, Tuple, Dict, AsyncGenerator

from config import CONFIG, MODEL_CLIENT


def remove_gradio_metadata(chat_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove the metadata key and value from each message.

    Args:
        chat_history (List[Dict[str, str]]): The chat history to get rid of metadata.

    Returns:
        List[Dict[str, str]]: The chat history without metadata.
    """
    return [
        {"role": message["role"], "content": message["content"]}
        for message in chat_history
    ]


def add_user_message(
    query: str, chat_history: List[Dict[str, str]], message_history: List[str]
) -> Tuple[str, List[Dict[str, str]], List[str]]:
    """Adds the user message to the chat and message history.

    Args:
        query (str): The user query to be added to chat and message history.
        chat_history (List[Dict[str, str]]): The chat history the query should be added to.
        message_history (List[str]): The message history the query should be added to.

    Returns:
        Tuple[str, List[Dict[str, str]], List[str]]: The empty output to the message field and the final chat and message history.
    """
    chat_history = chat_history + [
        {"role": "user", "content": query},
        {"role": "assistant", "content": ""},
    ]
    message_history.append(query)
    return "", chat_history, message_history


async def respond_chat(
    chat_history: List[Dict[str, str]], message_history: List[str]
) -> AsyncGenerator[List[Dict[str, str]], List[str]]:
    """Creates a response from the LLM and hands it over to the chat.

    Args:
        chat_history (List[Dict[str, str]]): The chat history the LLM answer should be added to.
        message_history (List[str]): The message history used to build the messages serving as input for the LLM.

    Yields:
        AsyncGenerator[List[Dict[str, str]], List[str]]: The resulting chat and message history containing the LLM answer.
    """
    messages = [
        {"role": "user", "content": CONFIG["system_prompt"]},
        {"role": "assistant", "content": CONFIG["assistant_response"]},
    ] + [
        {"role": role, "content": content}
        for role, content in zip(
            itertools.cycle(["user", "assistant"]), message_history
        )
    ]
    chat_history = remove_gradio_metadata(chat_history)

    chat_history[-1]["content"] = ""
    message_history.append("")

    stream = await MODEL_CLIENT.chat.completions.create(
        model=CONFIG["model_name"], messages=messages, stream=True, temperature=0.0
    )

    async for event in stream:
        chunk_stream = event.choices[0].delta.content
        chat_history[-1]["content"] += chunk_stream
        # replace newlines with <br>
        chat_history[-1]["content"] = chat_history[-1]["content"].replace("\n", "<br>")
        message_history[-1] += chunk_stream
        if chat_history[-1]["content"].strip() != "":
            yield chat_history, message_history
