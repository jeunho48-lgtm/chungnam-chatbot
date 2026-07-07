import streamlit as st
import google.generativeai as genai

# 웹 페이지 설정
st.set_page_config(page_title="충남 학습 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 교사 설정")

# API 키 입력 (공백 제거)
api_key = st.sidebar.text_input("Gemini API 키를 입력하세요:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 채팅 입력창
        if prompt := st.chat_input("천안이나 아산에 대해 궁금한 점을 물어보세요!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # AI 내부 명령어는 영어, 답변은 한글
                instruction = "You are a guide for 4th-grade students in Chungnam. Answer in Korean. Do not give direct answers; ask guiding questions to encourage thinking."
                response = model.generate_content(instruction + prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하면 대화가 시작됩니다.")
