# import gradio as gr
#
# def greet(name, intensity):
#     return "Hello, " + name + "!" * int(intensity)
#
# demo = gr.Interface(
#     fn=greet,
#     inputs=["text", "slider"],
#     outputs=["text"],
# )
#
# demo.launch()

# import time
# import gradio as gr
#
# def slow_echo(message, history):
#     for i in range(len(message)):
#         time.sleep(0.3)
#         yield "You typed: " + message[: i+1]
#
# gr.ChatInterface(slow_echo, type="messages").launch()
#
# import gradio as gr
# import time
#
# def echo(message, history, system_prompt, tokens):
#     response = f"System prompt: {system_prompt}\n Message: {message}."
#     for i in range(min(len(response), int(tokens))):
#         time.sleep(0.05)
#         yield response[: i+1]
#
# with gr.Blocks() as demo:
#     system_prompt = gr.Textbox("You are helpful AI.", label="System Prompt")
#     slider = gr.Slider(10, 100, render=False)
#
#     gr.ChatInterface(
#         echo, additional_inputs=[system_prompt, slider], type="messages"
#     )
#
# demo.launch()
#
from openai import OpenAI
import gradio as gr

client = OpenAI(
  organization='org-vx1tULpxxjqPCz8D7yeRiTX8',
  api_key='sk-pp-dev-service-account-7SoSiwFgu5fRS1fAmbbxT3BlbkFJ5emMxsvjUsvSiiKCvBNr'
)


def predict(message, history, request: gr.Request):
    history_openai_format = []
    for msg in history:
        history_openai_format.append(msg)
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(model='gpt-3.5-turbo',
                                              messages=history_openai_format,
                                              temperature=1.0,
                                              stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message


gr.ChatInterface(predict, type="messages").launch(share=True, auth=("admin", "pass1234"))