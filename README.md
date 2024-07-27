# Artifacts in One File/Single File Artifacts

[English Version](#english-version) | [中文版本](#中文版本)

## English Version

This project is inspired by [ai-artifacts](https://github.com/e2b-dev/ai-artifacts/tree/main), aiming to implement a similar product in a simpler way to gain a deeper understanding of the technology.

With just 130 lines of code, we've created a product similar to Artifacts. This project is intended for quickly learning technical principles and has not considered many edge cases, so there may be numerous bugs.

The code relies on Gradio and E2B. Thanks to the open-source community for making technology exploration so simple.

### Installation and Usage

```
pip install -r requirements.txt

# Set environment variables E2B_API_KEY and ANTHROPIC_API_KEY before using
export E2B_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
# run the code
python3 main.py
```

### Implementation Method

#### Key Components

1. **Gradio Interface**: Provides a user-friendly chat interface and display area for generated web content.
2. **Anthropic's Claude AI**: Generates Next.js code based on user prompts.
3. **E2B Sandbox**: Creates a real-time Next.js environment to render the generated code.

#### Workflow

1. User inputs a description or request for a web component.
2. The input is sent to Claude AI through the Anthropic API.
3. Claude generates TSX code based on the prompt.
4. The code is sent to the E2B sandbox running a Next.js environment.
5. The sandbox renders the code and returns a URL.
6. The rendered content is displayed in an iframe within the Gradio interface.

### Recommendations

[E2B](https://e2b.dev/) is a very user-friendly Code Interpreter tool that also supports custom Docker image uploads, making it extremely powerful.

[Gradio](https://www.gradio.app) is very easy to get started with, allowing programmers who are not proficient in React or other front-end technology stacks to quickly develop a UI and validate products.

## 中文版本

这个项目是受[ai-artifacts ](https://github.com/e2b-dev/ai-artifacts/tree/main) 启发，想用一个更简单的方式实现一个类似的产品，以对类似技术有更深的理解。

最终 130 行代码， 就实现一个类似 Artifacts 的产品。此项目仅为快速学习技术原理使用，有非常多的边界条件没有考虑，会有很多 Bug。

上述代码依赖 Gradio 和 E2B ，感谢开源社区让探索技术如此简单。

### 安装使用

```
pip install -r requirements.txt

# Set environment variables E2B_API_KEY and ANTHROPIC_API_KEY before using
export E2B_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
# run the code
python3 main.py
```

### 实现方式

#### 关键组件

1. **Gradio界面** ：提供用户友好的聊天界面和生成的Web内容显示区域。
2. **Anthropic的Claude AI** ：基于用户提示生成Next.js代码。
3. **E2B沙箱** ：创建实时Next.js环境来渲染生成的代码。

#### 工作流程

1. 用户输入Web组件的描述或请求。
2. 输入通过Anthropic API发送给Claude AI。
3. Claude基于提示生成TSX代码。
4. 代码被发送到运行Next.js环境的E2B沙箱。
5. 沙箱渲染代码并返回URL。
6. 渲染的内容在Gradio界面的iframe中显示。

### 推荐

[E2B](https://e2b.dev/) 是一个非常好用的Code Interpretor 工具，还支持自定义 Docker 镜像上传，非常强大。

[Gradio](https://www.gradio.app) 非常容易上手，让不能熟练使用React 等前端技术栈的程序员也能快速开发一个 UI，验证产品。


