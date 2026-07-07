import streamlit as st
import google.generativeai as genai

st.title("API 연결 테스트")

api_key = st.text_input("API 키 입력:", type="password").strip()

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 구글 서버에서 사용 가능한 모델 목록을 가져와봅니다.
        models = [m.name for m in genai.list_models()]
        st.success("API 키 연결 성공!")
        st.write("사용 가능한 모델 목록:", models)
    except Exception as e:
        st.error(f"연결 실패: {e}")
