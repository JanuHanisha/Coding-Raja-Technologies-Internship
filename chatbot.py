import os
import time
import openai
from openai import OpenAI
import gradio as gr

api_key = "sk-proj-kyNe8ys5ivjrvMKM81nxT3BlbkFJkfuNwSqen7J8WoSFNlbJ"
client = openai.Client(api_key=api_key)

prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n Human: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "hello how are you\n" 
            }
            ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response.choices[0].text 
    except openai.error.RateLimitError as e:
        print("Rate limit exceeded. Waiting to retry...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        return openai_create()

def conversation_history(input,history):
    history = history or []
    s=list(sum(history,()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input,output))
    return history, history

blocks = gr.Blocks()

with blocks:
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("Click")
    submit.click(conversation_history, inputs=[message,state],outputs=[chatbot,state])
    
 
blocks.launch(debug=True)   
    