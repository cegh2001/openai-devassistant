import os
import sys
import openai
import gradio as gr
import config

openai.api_key = config.api_key

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt, messages, input_history):
    max_tokens = 4096  # Limit of tokens to avoid exceeding the maximum allowed
    response_content = ''
    remaining_tokens = max_tokens

    while remaining_tokens > 0:
        # Send the remaining or maximum available tokens
        num_tokens = min(remaining_tokens, max_tokens)
        context = {"role": "system", "content": "Eres un asistente muy útil, sobre todo en programación."}
        messages = [context]
        content = prompt[len(prompt) - remaining_tokens: len(prompt) - remaining_tokens + num_tokens]
        remaining_tokens -= num_tokens
        messages.append({"role": "user", "content": content})

        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response_content += completions.choices[0].message.content

        messages.pop()  # Remove the previously added assistant response

        messages.append({"role": "assistant", "content": completions.choices[0].message.content})

    return response_content.strip()

def chatgpt_clone(input_text, history):
    history = history or []
    input_history = list(sum(history, ()))
    input_history.append(input_text)
    inp = ' '.join(input_history)
    output = openai_create(inp, history, input_history)
    history.append((input_text, output))
    try:
        with open("conversacion.txt", "a") as file:
            file.write("User: " + input_text + "\n" + "Assistant: " + output + "\n")
    except Exception as e:
        print("Error writing to file:", str(e))
    return history, history

block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center>Chatgpt personal</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND") # Button to send message
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state]) # Send message on button click SEND
    submit.click(lambda x: gr.update(value=''), [], [message])  # Clear input textbox on button click
    message.submit(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state]) # Send message on input pressing Enter
    message.submit(lambda x: gr.update(value=''), [], [message])  # Clear input textbox on input submit

block.launch(debug=True, share=True)
