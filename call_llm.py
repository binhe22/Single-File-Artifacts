import os
from anthropic import Anthropic


prompt ="""
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
        messages=[{"role": "user", "content": prompt+request_desc}],
    )
    content = ""
    code = ""
    for i in response.content:
        if i.type == "text":
            content = i.text
        if i.type == "tool_use":
            code = i.input["code"]
    return content,code



if __name__ == "__main__":
    request_desc = "write a simple website,title is hello xiaoxue"
    content,code = get_web_page_content(request_desc)
    print(code)
    