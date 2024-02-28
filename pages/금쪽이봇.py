import streamlit as st

from openai import OpenAI
from PIL import Image
import numpy as np

from dotenv import load_dotenv
load_dotenv()

import sys

sys.path.append("..")
from PIL import Image
favicon = Image.open("소영.png")
st.set_page_config("파닥몬사이트", page_icon=favicon)
from utils import authenticate, initialize_ui
initialize_ui()

authenticate()

imgs = {
    "소영":np.array(Image.open("소영.png")),
    "노성":np.array(Image.open("노성.png"))
}

client = OpenAI()

st.title("금쪽이봇")

if 'openai_model' not in st.session_state:
    st.session_state["openai_model"]="gpt-4-0125-preview"
# Initialize session state to store conversation history if it doesn't already exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

with st.chat_message("assistant", avatar=imgs["노성"]):
    st.write("파닥몬님, 궁금하신게 있다면 알려주세요.")

for chat in st.session_state['chat_history']:
    role = chat["role"]
    content = chat["content"]
    if role == 'user':
        with st.chat_message(role, avatar=imgs["소영"]):
            st.write(content)
    elif role == 'assistant':
        with st.chat_message(role, avatar=imgs["노성"]):
            st.write(content)

if prompt := st.chat_input():
    st.session_state["chat_history"].append({"role":"user", "content": prompt})
    with st.chat_message("user", avatar=imgs["소영"]):
        st.write(prompt)

    with st.chat_message("assistant", avatar=imgs["노성"]):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{
                "role": "system", 
                "content": '''
                    You are a helpful assistant named '금쪽이'. 
                    You generally communicate in Korean, but upon specific request you excel in communicating in 
                    other languages as well. The client you are helping is named '파닥몬님', and you will serve her by kindly calling her name followed by your
                    reaction to her request. As for the name you can call her anything among 4 names, '파닥몬님', '사랑둥이님', '바보둥이님', '귀염둥이님'.
                    No other names should be used to call the her. Here's an example: "안녕하세요, 금쪽이입니다. 어떻게 도와드릴까요?", or "알겠습니다 파닥몬님", or "이해했습니다 귀염둥이님 or 사랑둥이님 or 바보둥이님". 
                '''
            }] + [{"role":m["role"], "content":m["content"]} for m in st.session_state["chat_history"]],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state["chat_history"].append({"role":"assistant", "content":response})
