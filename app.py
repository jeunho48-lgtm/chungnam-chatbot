import streamlit as st
import google.generativeai as genai

# 사이드바에서 API 키를 입력받도록 설정
st.sidebar.title("🛠️ Teacher Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    st.title("🗺️ Chungnam Regional Learning AI")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about Cheonan or Asan!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_prompt = f"""
            You are a guide for 4th-grade elementary students learning about Chungnam geography.
            Do not provide direct answers. Ask thought-provoking questions to help students explore.
            Do not include numbers, item names, or brackets in the output. Use natural sentences.
            Question: {prompt}
            """
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("⚠️ Please enter your API key in the sidebar to start!")
