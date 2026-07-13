import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="충남 지역화 학습 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 설정")
api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # [핵심] AI 스튜디오와 동일한 수준의 지시사항 (강력한 규칙 설정)
        system_instruction = """
너는 초등학교 4학년 사회 지역화 학습을 돕는 전문 AI 가이드야. 다음 지침을 철저히 따라라.
1. 표 형식 유지: 데이터 정리 시 반드시 마크다운 표(Table)를 사용해. 절대 표를 텍스트로 풀어쓰지 마.
2. 숫자 표기: 모든 수치는 '아라비아 숫자'로만 써. 한글 숫자 표기 금지.
3. 정보 우선 제공: 정답을 미리 말하지 말고, 데이터를 먼저 제시한 뒤 마지막에만 발문 1개를 던져.
4. 출력 청결: 괄호()나 번호(1. 2.)는 출력하지 마. 
5. 최신성: 2026년 기준 데이터를 바탕으로 사실에 기반해 답변해.
6. 구조: 설명은 핵심만 간결하게 하고, 질문과 관련된 시각 자료(링크)를 적절히 포함해.
"""

        # AI 스튜디오 설정(Temperature 1)과 동일하게 구성
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview",
            generation_config={"temperature": 1.0},
            system_instruction=system_instruction
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
                # [중요] re.sub 필터링을 제거하고 모델이 생성한 텍스트 그대로 출력 (표 깨짐 방지)
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"오류: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
