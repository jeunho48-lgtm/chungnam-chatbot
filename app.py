import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="충남 지역화 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 설정")

api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 가장 범용적인 모델 사용
        model = genai.GenerativeModel("gemini-1.5-flash")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("궁금한 점을 물어보세요!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # 한글 답변을 강제하는 프롬프트
                instruction = "You are a guide for 4th-grade students in Chungnam. Answer in Korean. Ask guiding questions to encourage thinking."
                response = model.generate_content(instruction + prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
