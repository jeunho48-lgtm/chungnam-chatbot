import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="충남 지역화 학습 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 교사 설정")

# API 키 입력 (공백 제거)
api_key = st.sidebar.text_input("Gemini API 키를 입력하세요:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 질문 입력창 (한글)
        if prompt := st.chat_input("천안이나 아산에 대해 궁금한 점을 물어보세요!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # AI에게 내리는 지시사항 (영어)
                full_prompt = f"You are a guide for 4th-grade students learning about Chungnam geography. Answer in Korean. Do not give direct answers, but ask guiding questions. Question: {prompt}"
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류가 발생했습니다. API 키를 확인해주세요: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하면 챗봇이 시작됩니다.")
