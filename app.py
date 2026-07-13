import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="충남 지역화 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 설정")

api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()
st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 답변의 일관성을 위해 온도를 0으로 설정
        generation_config = {"temperature": 0}
        
        # 모델 설정
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview",
            generation_config=generation_config,
            system_instruction="너는 초등학교 4학년 학생들이 스스로 지리 데이터를 해석하고 탐구할 수 있도록 돕는 '충청남도 지역화 학습' 질문 가이드 AI야. 정답을 먼저 제시하지 말고, 발문을 통해 아이들이 생각할 기회를 주는 것이 네 가장 중요한 임무야. 본문이나 제목에 괄호나 숫자가 포함되면 삭제해. 아이가 물어보면 맞춤형 데이터와 발문만 제시해."
        )

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
                # 실제 데이터 기반 답변 생성
                response = model.generate_content(prompt)
                
                # 출력 전 필터링 (괄호, 숫자 삭제)
                filtered_text = response.text.replace("(", "").replace(")", "")
                
                st.markdown(filtered_text)
                st.session_state.messages.append({"role": "assistant", "content": filtered_text})
                
    except Exception as e:
        st.error(f"오류: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
