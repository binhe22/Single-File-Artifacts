import os
from typing import List, Tuple
import anthropic
from e2b.api.v2.client.models import sandbox
import gradio as gr
from anthropic import Anthropic
from e2b import Sandbox, api
from gradio_agentchatbot import AgentChatbot, ChatMessage

# Constants
DEFAULT_PAGE = "https://e2b.dev/"
IFRAME_TEMPLATE = '<iframe src="{}" width="100%" height="800px"></iframe>'
DEFAULT_CONTENT = IFRAME_TEMPLATE.format(DEFAULT_PAGE)
MAX_TOKENS = 4096
MODEL_NAME = "claude-3-5-sonnet-20240620"
SANDBOX_TEMPLATE = "nextjs-developer"
FILE_PATH = "/home/user/app/page.tsx"
PORT = 3000
ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
# INPUT_ANTHROPIC_API_KEY = ""
# INPUT_E2B_API_KEY = ""
SAMPLE_CODE = """
import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div>
      <h1>Welcome to my Next.js page!</h1>
      <p>This is a simple page component.</p>
    </div>
  );
};

export default HomePage;
"""

PROMPT = """
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


def render_code(api_key: str, code: str) -> Tuple[str, Sandbox]:
    """
    Render the provided code in a sandbox environment.
    Args:
        code (str): The code to be rendered.
    Returns:
        Tuple[str, Sandbox]: The URL of the rendered page and the sandbox instance.
    """
    try:
        if not api_key:
            return DEFAULT_CONTENT, None
        sandbox = Sandbox(template=SANDBOX_TEMPLATE, api_key=api_key)
        sandbox.keep_alive(100)  # Consider making this configurable
        sandbox.filesystem.write(FILE_PATH, code)
        url = sandbox.get_hostname(PORT)
        return f"https://{url}", sandbox
    except Exception as e:
        print(f"Error in render_code: {e}")
        return DEFAULT_PAGE, None


def get_web_page_content(llm_key: str, request_desc: str) -> Tuple[str, str]:
    """
    Get web page content based on the provided description.
    Args:
        request_desc (str): The description of the requested content.
    Returns:
        Tuple[str, str]: The content and the code.
    """
    # api_key = os.environ.get(ANTHROPIC_API_KEY_ENV)
    # if not api_key:
    #     raise ValueError(
    #         f"Missing {ANTHROPIC_API_KEY_ENV} environment variable")
    # client = Anthropic(api_key=api_key)
    api_key = llm_key
    client = Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
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
                "content": PROMPT + request_desc
            }],
        )
        content = next((i.text for i in response.content if i.type == "text"),
                       "")
        code = next((i.input.get("code")
                     for i in response.content if i.type == "tool_use"), "")

        return content, code
    except Exception as e:
        print(f"Error in get_web_page_content: {e}")
        return "", ""


def interact_with_agent(prompt: str, messages: List[ChatMessage],
                        anthropic_api_key: str, e2b_api_key: str):
    """
    Interact with the agent based on the provided prompt and messages.
    Args:
        prompt (str): The user's prompt.
        messages (List[ChatMessage]): The list of chat messages.
    Yields:
        Tuple[List[ChatMessage], gr.update]: Updated messages and iframe content.
    """
    messages.append(ChatMessage(role="user", content=prompt))
    yield messages, gr.update()
    content, code = get_web_page_content(anthropic_api_key, prompt)
    if not content:
        print("error")
        messages.append(
            ChatMessage(
                role="assistant",
                content=
                "There is somenthing wrong,please verify your api key first."))
        yield messages, gr.update()
    iframe = gr.update()
    if code:
        url, _ = render_code(e2b_api_key, code)
        iframe = IFRAME_TEMPLATE.format(url)
    messages.append(ChatMessage(role="assistant", content=content))
    yield messages, iframe


def valid_and_set_api_key(anthropic_api_key: str, e2b_api_key: str):
    result_str = ""
    content, code = get_web_page_content(anthropic_api_key, "hi")
    url, sand = render_code(e2b_api_key, SAMPLE_CODE)
    print(anthropic_api_key, e2b_api_key)
    if content:
        result_str = result_str + "ANTHROPIC_API_KEY is valid"
    else:
        result_str = result_str + "ANTHROPIC_API_KEY is not valid"

    if sand:
        result_str = result_str + "\nE2B_API_KEY is valid"
    else:
        result_str = result_str + "\nE2B_API_KEY is not valid"
    return anthropic_api_key, e2b_api_key, result_str

    # print(anthropic_api_key, e2b_api_key)


# Gradio interface setup
with gr.Blocks(title="Artifacts in One File") as demo:
    anthropic_api_key = gr.State("")
    e2b_api_key = gr.State("")
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ### Please input the key, and it won't be saved.
            Welcome to star [Github Repo](https://github.com/binhe22/single-file-artifacts)
            Visit [E2B Website](https://e2b.dev/) to get the E2B_API_KEY.
            There is no multi-turn conversation for now.
            """)
            with gr.Row():
                anthropic_input = gr.Textbox(
                    label="ANTHROPIC_API_KEY",
                    placeholder="Input Anthropic API Key",
                    type="password")
                e2b_input = gr.Textbox(label="E2B_API_KEY",
                                       placeholder="Input E2B API Key",
                                       type="password")
            submit_button = gr.Button("Verify")
            output = gr.Textbox(label="Verification Result")
            chatbot = AgentChatbot(label="Agent")
            text_input = gr.Textbox(lines=1, label="Chat Message")
        with gr.Column(scale=2):
            iframe = gr.HTML(DEFAULT_CONTENT)

    text_input.submit(interact_with_agent,
                      [text_input, chatbot, anthropic_api_key, e2b_api_key],
                      [chatbot, iframe])
    submit_button.click(valid_and_set_api_key, [anthropic_input, e2b_input],
                        outputs=[anthropic_api_key, e2b_api_key, output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
