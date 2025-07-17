#!/usr/bin/env python
# coding: utf-8

# In[1]:


# In[2]:


import google.generativeai as genai
import os

# 여기에 본인의 API 키를 입력하세요.
# 더 안전한 방법은 os.environ을 사용하여 환경 변수에서 키를 불러오는 것입니다.
# os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY"

genai.configure(api_key="AIzaSyDL02u2DTdd3tKg4KtgDzWFSKr8EDg8PyE")

# 사용할 제미나이 모델을 선택합니다. 'gemini-1.5-flash'는 빠르고 효율적입니다.
model = genai.GenerativeModel('gemini-2.5-flash')


# In[3]:


# 챗봇의 역할을 정의하는 시스템 프롬프트를 설정합니다.
# 이 프롬프트를 어떻게 작성하느냐에 따라 가사의 퀄리티가 달라집니다.
system_prompt = """
당신은 감성적인 노래 가사를 쓰는 작곡가입니다.
사용자가 원하는 주제, 장르, 분위기를 입력하면, 그에 맞는 창의적이고 아름다운 노래 가사를 만들어주세요.
가사는 다음과 같은 구조를 포함하면 좋습니다.

- 1절 (Verse 1)
- 프리코러스 (PreChorus)
- 후렴 (Chorus)
- 2절 (Verse 2)
- 브릿지 (Bridge)
- 후렴 (Chorus)
- 아웃트로 (Outro)

슬프고 애절한 발라드, 신나는 댄스 팝, 따뜻한 어쿠스틱 등 다양한 장르의 가사를 쓸 수 있습니다.
사용자의 요청에 깊이 공감하며, 독창적인 표현과 시적인 비유를 사용해주세요.
"""

# 시스템 프롬프트를 적용하여 채팅 세션을 시작합니다.
chat = model.start_chat(history=[
    {'role': 'user', 'parts': [system_prompt]},
    {'role': 'model', 'parts': ["안녕하세요! 저는 당신의 감성을 노래로 만들어드릴 작곡가입니다. 어떤 이야기를 노래로 만들고 싶으신가요? 주제, 장르, 분위기를 자유롭게 말씀해주세요."]}
])


# In[4]:




# In[5]:




# In[ ]:
import streamlit as st
import google.generativeai as genai
import os

# --- 페이지 설정 및 제목 ---
st.set_page_config(page_title="나만의 챗봇", page_icon="")
st.title("시은이와 민이의 노래 챗봇")

# --- API 키 설정 ---
# Streamlit의 secrets 관리 기능을 사용하는 것이 가장 안전합니다.
# 직접 입력하려면 아래 코드 사용
# api_key = "YOUR_GOOGLE_API_KEY"
# genai.configure(api_key=api_key)

# secrets.toml을 이용한 API 키 설정 (권장)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("API 키를 설정해주세요! Streamlit의 secrets.toml 파일을 확인하세요.")
    st.stop()


# --- 모델 초기화 ---
# 사용할 모델을 선택합니다.
model = genai.GenerativeModel('gemini-1.5-flash')


# --- 채팅 기록 관리 (가장 중요!) ---
# Streamlit은 스크립트를 위에서 아래로 재실행하므로, 채팅 기록을 세션에 저장해야 합니다.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 채팅 세션 시작 (대화 기록 포함)
chat = model.start_chat(history=st.session_state.chat_history)


# --- UI 화면 구성 ---
# 저장된 채팅 기록을 순서대로 화면에 표시
for message in chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 사용자 입력을 받기 위한 채팅 입력창
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자가 입력한 메시지를 화면에 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini 모델에게 응답 요청 및 화면에 표시
    with st.spinner("생각 중... 🤔"):
        response = chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)

    # 응답 후 채팅 기록을 세션에 업데이트
    st.session_state.chat_history = chat.history




