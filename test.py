from call_llm import get_web_page_content
from render_code import render_code


if __name__ == "__main__":
    request_desc = """
    创建一个网页，基于tailwind 
    内容是一封感谢信，感谢客户对我们茶叶的支持，引用诗词让内容有文采一些 让页面的内容足够好看，设计前卫，参考苹果的设计风格，添加更多的样式
    添加一个按钮，能让我输入客户的名称。
    
    """
    
    content,code = get_web_page_content(request_desc)
    
    print("Bot:", content)
    url,sandbox = render_code(code)
    print("URL",url)
    sandbox.close()





