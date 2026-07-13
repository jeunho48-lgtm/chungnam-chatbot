import streamlit as st
import google.generativeai as genai
import re

# 페이지 설정
st.set_page_config(page_title="충남 지역화 학습 AI", page_icon="🗺️")
st.sidebar.title("🛠️ 설정")
api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()

st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 기존 규칙에 숫자/간결체 규칙을 추가 반영함
        system_instruction = """
너는 초등학교 4학년 사회 지역화 학습 가이드야. 다음 규칙을 철저히 따라라.
1. 정보 우선 제공: 질문을 받으면 관련된 지리 정보(인구, 기온, 지형, 산업 등)를 먼저 충분히 설명하고 시각 자료(링크 등)를 제시해.
2. 답변 구조: 답변의 80%는 상세한 정보 전달과 데이터 해석으로 채우고, 마지막에만 아이가 생각할 수 있는 발문 1개를 던져.
3. 데이터 표기 규칙(추가): 모든 수치는 반드시 아라비아 숫자(예: 384,000)로 표기해. 한글로 숫자를 적지 마라.
4. 문장 스타일(추가): 문장은 핵심 위주로 짧게 끊어서 써. 장황한 설명은 피하고 깔끔하게 요약해.
5. 출력 규칙: 괄호()나 '번 항목' 같은 숫자는 출력하기 전에 모두 제거하고 자연스러운 문장으로만 구성해.
"""

        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview",
            generation_config={"temperature": 0.3},
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
                # 검색 도구 제외(429 방지) + 시스템 지시사항 준수 강화
                response = model.generate_content(f"{prompt} (아라비아 숫자를 쓰고 간결하게 요약해줘)")
                
                # 출력 필터링: 괄호 및 번호 제거
                text = re.sub(r'\([0-9,.\s]+\)', '', response.text)
                text = re.sub(r'\d+\.\s', '', text)
                
                st.markdown(text)
                st.session_state.messages.append({"role": "assistant", "content": text})
                
    except Exception as e:
        st.error(f"오류: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
