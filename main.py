import os
import openai
import gradio as gr
import config

#if you have OpenAI API key as an environment variable, enable the below
#openai.api_key = os.getenv("OPENAI_API_KEY")
#if you have OpenAI API key as a string, enable the below
openai.api_key = config.api_key

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt,messages,s):
    max_tokens = 4097
    response_content = ''
    remaining_tokens = max_tokens

    while remaining_tokens > 0:
        # Enviamos la cantidad de tokens que queden disponibles o el máximo permitido
        num_tokens = min(remaining_tokens, max_tokens)
        context = {"role": "system", "content": "Eres un asistente muy útil."}
        messages = [context]
        content = prompt[len(prompt)-remaining_tokens:len(prompt)-remaining_tokens+num_tokens]
        remaining_tokens -= num_tokens
        messages.append({"role": "user", "content": content})

        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response_content += completions.choices[0].message.content

        messages.pop()  # Elimina la respuesta del asistente agregada anteriormente

        messages.append({"role": "assistant", "content": completions.choices[0].message.content})

    return response_content.strip()

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp, history, s)
    history.append((input, output))
    # Abre el archivo txt en modo agregar
    with open("conversacion.txt", "a") as file:
        file.write("User: " + input + "\n" + "Assistant: " + output + "\n")
    return history, history

block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center>Build Yo'own ChatGPT with OpenAI API & Gradio</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])
    
block.launch(debug=True)