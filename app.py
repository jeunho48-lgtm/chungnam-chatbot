import streamlit as st
import google.generativeai as genai

# 사이드바에서 API 키를 입력받도록 설정
st.sidebar.title("🛠️ 교사 설정")
api_key = st.sidebar.text_input("Gemini API 키를 입력하세요:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    st.title("🗺️ 충남 지역화 학습 AI")
    
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
            full_prompt = f"""
            너는 초등학교 4학년을 위한 충남 지역화 학습 가이드야.
            정답을 바로 말하지 말고, 아이가 스스로 생각할 수 있도록 질문을 던져줘.
            번호나 항목명, 괄호 등은 제외하고 자연스러운 문장으로만 대답해줘.
            질문: {prompt}
            """
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("⚠️ 챗봇을 시작하려면 사이드바에 API 키를 입력해 주세요!")
