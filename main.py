import gradio as gr
from gradio.themes import default
from gradio_agentchatbot import AgentChatbot, ChatMessage
from call_llm import get_web_page_content
from render_code import render_code

default_page = "https://e2b.dev/"
iframe_content = '<iframe src={} width="800px" height="800px"></iframe>'
default_content = iframe_content.format(default_page)

# def interact_with_agent(prompt, messages):
#     messages.append(ChatMessage(role="user", content=prompt))
#     yield messages
#     content, code = get_web_page_content(prompt)
#     if code:
#         url, sandbox = render_code(code)
#         iframe = iframe_content.format(url)
#     messages.append(ChatMessage(role="assistant", content=content))
#     yield messages, iframe


def interact_with_agent(prompt, messages):
    messages.append(ChatMessage(role="user", content=prompt))
    yield messages, gr.update()  # 第一次yield，更新messages但不更新iframe

    content, code = get_web_page_content(prompt)
    iframe = gr.update()  # 默认不更新iframe
    if code:
        url, sandbox = render_code(code)
        iframe = iframe_content.format(url)

    messages.append(ChatMessage(role="assistant", content=content))
    yield messages, iframe


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            chatbot = AgentChatbot(label="Agent")
            text_input = gr.Textbox(lines=1, label="Chat Message")

        with gr.Column(scale=2):
            iframe = gr.HTML(default_content)

    text_input.submit(interact_with_agent, [text_input, chatbot],
                      [chatbot, iframe])

# with gr.Blocks() as demo:
#     chatbot = AgentChatbot(label="Agent")
#     text_input = gr.Textbox(lines=1, label="Chat Message")
#     text_input.submit(interact_with_agent, [text_input, chatbot], [chatbot])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
