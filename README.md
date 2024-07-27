# Artifacts in One File/Single File Artifacts


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
