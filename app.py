import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="충남 지역화 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 설정")

# API 키 입력
api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        # 선생님 계정에서 확인된 모델명으로 정확히 수정
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3-flash-preview")

        # 세션 상태 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 기존 대화 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 사용자 입력 처리
        if prompt := st.chat_input("궁금한 점을 물어보세요!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                instruction = "너는 초등학교 4학년 사회 지역화 학습 가이드야. 정답을 바로 주지 말고 아이들이 스스로 생각할 수 있도록 관련 지리 정보(인구, 기온, 지형, 산업 등)를 활용한 질문을 먼저 던져줘. 항상 친절한 한글로 대답해줘."
                
                # 모델 응답 생성
                response = model.generate_content(instruction + prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
