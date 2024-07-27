from e2b_code_interpreter import CodeInterpreter
from e2b import Sandbox
import time
from call_llm import get_web_page_content


sandbox = Sandbox(template="nextjs-developer")
                 # cpu_count = 4,
                 # memory_size = 4_096)

# sandbox = Sandbox(template="elpfdrwoo5f9dvt2l5bo")
                  
                 # cwd = "/home/user/app/",
                 # start_cmd = "cd /home/user && npx next")
sandbox.keep_alive(60)

# proc1 = sandbox.process.start("cd /home/user && npx next")
# proc1.wait()
# print(proc1.output.stderr)

# code = """
# import type { NextPage } from 'next'

# const Home: NextPage = () => {
#   return (
#     <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100">
#       <main className="text-center">
#         <h1 className="text-4xl font-bold text-blue-600 mb-4">
#           Welcome to Next.js with Tailwind CSS
#         </h1>
#         <p className="text-xl text-gray-700">
#           Get started by editing{' '}
#           <code className="bg-gray-200 rounded-md p-1">pages/index.tsx</code>
#         </p>
#       </main>
#     </div>
#   )
# }

# export default Home

# """
request_desc = """
创建一个网页，基于tailwind 
内容是一封感谢信，感谢客户对我们茶叶的支持，引用诗词让内容有文采一些 让页面的内容足够好看，设计前卫，参考苹果的设计风格，添加更多的样式
添加一个按钮，能让我输入客户的名称。
添加一个按钮，能把生成的内容下载成JPG

你使用的任何将组件请转换为客户端组件，在输出代码的顶部添加 'use client' 指令
"""

content,code = get_web_page_content(request_desc)

print("Bot:", content)

sandbox.filesystem.write("/home/user/app/page.tsx", code)  

proc = sandbox.process.start("ps aux | grep node")
proc.wait()
print(proc.output.stdout)

open_port = 3000
url = sandbox.get_hostname(open_port)  

url = "https://"+url
print(url)

# proc = sandbox.process.start("echo 1")
# proc.wait()
# print(proc.output.stdout)


    
try:
    time.sleep(120)
    sandbox.close()
    print("quit")
except Exception as e:
    sandbox.close()
    print("quit",e)



sandbox.close()
    

