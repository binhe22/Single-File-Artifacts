import gradio as gr
from gradio_agentchatbot import AgentChatbot, ChatMessage
import os
from anthropic import Anthropic
from e2b import Sandbox

default_page = "https://e2b.dev/"
iframe_content = '<iframe src={} width="100%" height="800px"></iframe>'
default_content = iframe_content.format(default_page)


def render_code(code):
    sandbox = Sandbox(template="nextjs-developer")
    # sandbox = Sandbox(template="elpfdrwoo5f9dvt2l5bo")
    sandbox.keep_alive(100)
    # set a default time,to make avoid waste of e2b service
    sandbox.filesystem.write("/home/user/app/page.tsx", code)
    open_port = 3000
    url = sandbox.get_hostname(open_port)
    url = "https://" + url
    return url, sandbox


prompt = """
You are a skilled Next.js developer. You do not make mistakes.
You have a running nextjs app and can edit the main page.tsx file. It reloads automatically.
You are using nextjs version 14. So make sure to include 'use client' if needed at the top.
Your job is to follow user's instruction by writing the TSX code to the page.tsx file.
Use tailwindcss classes to style the components.
Preinstalled packages:
- nextjs (14.2.5)
- recharts (2.12.7)
Please convert any components you use to client components, and add the 'use client' directive at the top of the output code.
Specific requirements are as follows:
"""


def get_web_page_content(request_desc):
    client = Anthropic(
        # This is the default and can be omitted
        api_key=os.environ.get("ANTHROPIC_API_KEY"), )
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        tools=[{
            "name": "write_web_code",
            "description":
            "Writes TSX code to the page.tsx file. You can use tailwind classes.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The TSX code to write",
                    }
                },
                "required": ["code"],
            },
        }],
        messages=[{
            "role": "user",
            "content": prompt + request_desc
        }],
    )
    content = ""
    code = ""
    for i in response.content:
        if i.type == "text":
            content = i.text
        if i.type == "tool_use":
            code = i.input.get("code")
    return content, code


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
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
