from io import BytesIO
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup

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

st.title("이미지다운로더")
st.info("링크 내 모든 이미지를 다운로드합니다")

link = st.text_input("원하는 이미지가 있는 페이지 링크를 입력하세요")
if link == None or link == "":
    st.stop()
else:

    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')

    with st.spinner("사이트에 접속중입니다..."):
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)

    with st.spinner("이미지를 추출하는 중입니다"):
        # Open the URL 
        driver.get(link)
        # Scroll to the bottom of the page to ensure all lazy-loaded images are loaded
        # This can be adjusted based on the page's loading behavior
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load
        time.sleep(5)  # Adjust timing as necessary
        images = driver.find_elements("css selector", "img")
        srcs = []
        for img in images:
            # Check for 'src' or 'data-src' or any other relevant attribute
            src = img.get_attribute('src') if img.get_attribute('src') else img.get_attribute('data-src')
            print(src)
            if src:  # Ensure src is not None
                srcs.append(src)

        # Close the browser
    driver.quit()

    with st.spinner("더 많은 이미지를 추출중입니다."):
        html = requests.get(link).content
        soup = BeautifulSoup(html, 'lxml')
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                print(src)
                srcs.append(src)

    if len(srcs) == 0:
        st.warning("이미지를 찾을 수 없습니다")
        st.stop()

    for src in srcs:
        correct_file = src != None and ".jpg" in src or ".png" in src or ".webp" in src or ".jpeg" in src
        if correct_file:
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown(f"<img src={src} width='100px'/>", unsafe_allow_html=True)
            with col2:

                if not src.startswith(('http:', 'https:')):
                    src = 'https:' + src
                                
                response = requests.get(src)

                # Check if the request was successful
                if response.status_code == 200:
                    # Open the image directly from the bytes in memory
                    image = Image.open(BytesIO(response.content))
                    
                    # Get the width and height of the image
                    width, height = image.size
                else:
                    width, height = "none", "none"
                st.write(f"넓이:{width}")
                st.write(f"높이:{height}")
            with col3:
                st.link_button("링크로가기", src)