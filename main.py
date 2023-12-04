import gradio as gr
# Importar el modelo, el tokenizador, y el dispositivo
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m")
tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")
import torch

# Definir la función bloom_create
def bloom_create(prompt, messages, input_history):
    max_tokens = 4096  # Limit of tokens to avoid exceeding the maximum allowed
    response_content = ''
    past_key_values = None  # Initialize the state of the model

    # Encode the messages and the prompt as input ids
    input_ids = tokenizer.encode('\n'.join([message['content'] for message in messages]), return_tensors='pt')
    
    # Generate output ids using the model
    output_ids = model.generate(input_ids, max_length=max_tokens, do_sample=True, top_p=0.95, use_cache=True)

    # Decode the output ids as text
    response_content = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Update the state of the model
    past_key_values = model.past_key_values

    return response_content.strip()

# Definir la función chatgpt_clone
def chatgpt_clone(input_text, history):
    history = history or []
    input_history = list(sum(history, ()))
    input_history.append(input_text)
    inp = ' '.join(input_history)
    output = bloom_create(inp, history, input_history)
    history.append((input_text, output))
    try:
        with open("conversacion.txt", "a") as file:
            file.write("User: " + input_text + "\n" + "Assistant: " + output + "\n")
    except Exception as e:
        print("Error writing to file:", str(e))
    return history, history


block = gr.Blocks(title="Chatgpt personal")

with block:
    gr.Markdown(description="Esta es una aplicación de chatbot basada en el modelo Chatgpt.")
    chatbot = gr.Chatbot(flagging_options=["Inapropiado", "Incorrecto"])
    message = gr.Textbox(label="Escribe tu mensaje aquí")
    state = gr.State(default={"history":[]})
    submit = gr.Button("SEND") # Botón para enviar mensaje
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state]) # Enviar mensaje al hacer clic en SEND
    submit.click(lambda x: gr.update(value=''), [], [message])  # Borrar el cuadro de texto de entrada al hacer clic en el botón
    message.submit(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state]) # Enviar mensaje al presionar Enter
    message.submit(lambda x: gr.update(value=''), [], [message])  # Borrar el cuadro de texto de entrada al enviar el mensaje

block.launch(debug=True, share=True)