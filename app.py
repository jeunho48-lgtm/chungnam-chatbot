import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="충남 지역화 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 설정")

api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 테스트 결과에서 확인된 사용 가능한 모델명으로 변경
        model = genai.GenerativeModel("gemini-2.0-flash-lite")

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
                instruction = "너는 충남 지역화 학습 가이드야. 정답을 바로 주지 말고 생각할 거리를 질문해줘. 한글로 대답해줘."
                response = model.generate_content(instruction + prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
