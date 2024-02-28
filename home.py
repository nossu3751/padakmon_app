import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PIL import Image
from dotenv import load_dotenv
load_dotenv()


favicon = Image.open("소영.png")
st.set_page_config("파닥몬사이트", page_icon=favicon)
from utils import authenticate

authenticate()

st.title("파닥몬사이트")
add_vertical_space()
st.header("귀염둥이 파닥몬을 위한 사이트입니다")
add_vertical_space()
padakmon_image = Image.open("파닥몬.jpeg")
st.image(padakmon_image)




