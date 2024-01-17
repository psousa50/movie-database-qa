import sys

# import gradio as gr


class ChatBot:
    def __init__(self):
        self.conversation = []

    def chatbot_response(self, user_input):
        response = f"You said: {user_input}"
        self.conversation.append(f"YOU: {user_input}\n")
        self.conversation.append(f"BOT: {response}\n")
        return "".join(self.conversation)


chat_bot = ChatBot()


def start(input):
    response = chat_bot.chatbot_response(input)
    print(response)


# def start_ui():
#     iface = gr.Interface(
#         fn=chat_bot.chatbot_response,
#         inputs=gr.Textbox(lines=2, placeholder="Type something..."),
#         outputs="text",
#         title="Simple Chatbot",
#         description="Type a message and get a response.",
#         layout="vertical",
#     )

#     iface.launch()


if __name__ == "__main__":
    input = sys.argv[1]
    start(input)
