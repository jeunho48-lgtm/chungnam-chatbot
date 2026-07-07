import streamlit as st
import google.generativeai as genai

# 1. API 키 설정 (사이드바 입력 우선)
st.sidebar.title("🛠️ 교사 설정")
api_key = st.sidebar.text_input("Gemini API 키를 입력하세요:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    st.title("🗺️ 충청남도 지역화 학습 가이드")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("천안이나 아산에 대해 궁금한 점을 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 시스템 프롬프트 강화
            full_prompt = f"""
            너는 초등학교 4학년을 위한 충남 지역화 학습 가이드야.
            정답을 바로 말하지 말고, 아이가 생각할 질문을 던져라.
            번호나 항목명을 출력하지 말고 자연스러운 문장으로만 말해라.
            질문: {prompt}
            """
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("⚠️ 사이드바에 API 키를 입력해야 챗봇이 시작됩니다!")
