# openai-devassistant

Esto es un chatbot que usa las bibliotecas de gradio para tener una interfaz grafica y no tener la necesidad de ejecutar todo a traves de terminal, este surge para tener un acceso a modelos mas avanzadas de chatgpt a nivel de respuesta solo conectando la api y sabiendo como programar el contexto y la coherencia de la conversacion de la IA, ademas te permite regular como seran las respuestas a traves de codigo. 

start_sequence y restart_sequence son variables que se usan para mantener el hilo completo de la conversación. La idea es que cada mensaje del usuario (Human) comienza con restart_sequence y cada respuesta del asistente (AI) comienza con start_sequence.

prompt es el mensaje de introducción que aparece en la ventana del chat.

context es el primer mensaje que aparece una vez que el usuario ha iniciado la conversación. En este caso, es una respuesta del asistente al mensaje inicial del usuario, que se muestra en prompt.

messages es una lista que contiene todos los mensajes intercambiados entre el usuario y el asistente durante la conversación.

openai_create(prompt) es una función que utiliza la API de OpenAI para generar una respuesta del asistente en función de todo el historial de la conversación. La función usa el modelo gpt-3.5-turbo de OpenAI para generar estas respuestas.

chatgpt_clone(input, history) es una función que maneja el flujo completo de la conversación. Esta función toma el último mensaje del usuario (que se muestra en la entrada input) y lo utiliza junto con el historial completo de la conversación (history) para generar una respuesta del asistente. Luego, la función agrega tanto el mensaje del usuario como la respuesta del asistente al historial completo de la conversación y devuelve el historial actualizado.

block es un “bloque” de Gradio que define la interfaz de usuario del chatbot. Este bloque está formado por:

Un encabezado en Markdown que muestra el título de la aplicación.
Un componente chatbot, que muestra la conversación con el asistente.
Un componente message, que es una caja de texto que permite al usuario escribir un nuevo mensaje.
Un componente state, que se utiliza para almacenar el historial completo de la conversación.
Un botón submit que envía el nuevo mensaje del usuario a la función chatgpt_clone(input, history).
Resumiendo, la aplicación del chatbot utiliza la API de OpenAI para responder a las entradas del usuario, y Gradio proporciona una interfaz de usuario fácil de usar que permite al usuario interactuar con el chatbot.