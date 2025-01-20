import gradio as gr

from config import CONFIG
from model_chat import add_user_message, respond_chat

with gr.Blocks(title="NoxtuaCompliance") as demo:
    chat_bot = gr.Chatbot(
        label="NoxtuaCompliance",
        type="messages",
        bubble_full_width=False,
        height="80vh",
        autoscroll=True,
        value=[{"role": "assistant", "content": CONFIG["assistant_response"]}],
    )
    with gr.Row():
        msg = gr.Textbox(label="Message", elem_id="chat-input")
    clear_btn = gr.Button("Clear chat", elem_id="clear-btn", variant="secondary")

    message_history = gr.State([])

    clear_btn.click(
        lambda: [[{"role": "assistant", "content": CONFIG["assistant_response"]}], []],
        [],
        [chat_bot, message_history],
    )

    msg.submit(
        add_user_message,
        [msg, chat_bot, message_history],
        [msg, chat_bot, message_history],
        queue=False,
    ).then(
        respond_chat,
        [chat_bot, message_history],
        [chat_bot, message_history],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8020)
