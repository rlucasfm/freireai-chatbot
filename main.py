import streamlit as st
from openai import OpenAI
import time
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
assistant_id = "asst_gVWsPVMdh1MbgwR2K7Y3Gs9C"

st.title("FreireAI - Eu vou te ajudar a entender o Project Thinking! ")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": """Bem-vindo! Eu sou o FreireAI, um cérebro artificial pronto pra te ajudar a entender um pouco mais sobre o Project Thinking.
                                     \nSou uma criação da FWK Labs. Caso queira saber mais, acesse: https://fwk.global."""}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state['thread_id'] = thread.id

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client.beta.threads.messages.create(
        thread_id=st.session_state['thread_id'],
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=st.session_state['thread_id'],
        assistant_id=assistant_id
    )

    while run.status != 'completed':
        time.sleep(0.3)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state['thread_id'],
            run_id=run.id
        )

    # Retrieve messages added by the assistant
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state['thread_id']
    )

    response = messages.to_dict()

    msg = response.get('data')[0]['content'][0]['text']['value']
    msg = msg.split('【')[0]

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)