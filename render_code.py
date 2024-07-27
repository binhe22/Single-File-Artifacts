from e2b_code_interpreter import CodeInterpreter
from e2b import Sandbox
from call_llm import get_web_page_content

def render_code(code):
    sandbox = Sandbox(template="nextjs-developer")
    # sandbox = Sandbox(template="elpfdrwoo5f9dvt2l5bo")
    sandbox.keep_alive(100)
    # set a default time,to make avoid waste of e2b service
    sandbox.filesystem.write("/home/user/app/page.tsx", code)      
    open_port = 3000
    url = sandbox.get_hostname(open_port)  
    url = "https://"+url
    return url, sandbox

