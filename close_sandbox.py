from e2b_code_interpreter import CodeInterpreter
from e2b import Sandbox
import time
# sandbox = Sandbox(template="elpfdrwoo5f9dvt2l5bo",
#                  cwd = "/home/user/app/")

running_sandboxes = Sandbox.list()
print(running_sandboxes,len(running_sandboxes))
for i in running_sandboxes:
    s = Sandbox.reconnect(i.sandbox_id)
    print(s.get_hostname())
    s.close()
    print("close",i.sandbox_id)


