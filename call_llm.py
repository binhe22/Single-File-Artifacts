
import os
from anthropic import Anthropic


def get_web_page_content(request_desc):
    client = Anthropic(
        # This is the default and can be omitted
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        tools=[
            {
                "name": "write_web_code",
                "description": "Writes TSX code to the page.tsx file. You can use tailwind classes.",
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
            }
        ],
        messages=[{"role": "user", "content": request_desc}],
    )
    content = ""
    code = ""
    for i in response.content:
        if i.type == "text":
            content = i.text
        if i.type == "tool_use":
            code = i.input["code"]
    return content,code
    
    
    return response
if __name__ == "__main__":
    request_desc = "write a simple website,title is hello xiaoxue"
    content,code = get_web_page_content(request_desc)
    print(code)
    