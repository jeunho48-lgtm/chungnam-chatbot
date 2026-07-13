import streamlit as st
import google.generativeai as genai
import re

st.set_page_config(page_title="충남 지역화 학습 AI", page_icon="🗺️")
api_key = st.sidebar.text_input("Gemini API 키 입력:", type="password").strip()

if api_key:
    genai.configure(api_key=api_key)
    
    # 6가지 규칙이 완벽하게 반영된 시스템 지시사항
    system_instruction = """
너는 충청남도 지역화 학습 가이드야. 다음 규칙을 철저히 따라라.
1. 질문에 집중: 질문과 관련된 데이터만 제시하고, 전체 개괄 설명은 하지 마.
2. 정보 우선 제공: 질문에 대한 핵심 데이터를 먼저 제시한 후, 마지막에만 생각할 발문 1개를 던져.
3. 숫자 표기: 모든 수치는 반드시 아라비아 숫자(예: 384,000)로 표기해. 한글 숫자는 금지.
4. 정답 스포일러 금지: 인과관계나 정답을 미리 말하지 말고, 데이터를 보고 아이가 추론하게 해.
5. 출력 필터링: 괄호(), 불필요한 숫자나 번호, '번 항목'은 모두 삭제해.
6. 데이터 일치: 질문과 직접 관련된 시각 자료 1장만 제시하고 나머지는 생략해.
"""

    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config={"temperature": 0.2},
        system_instruction=system_instruction
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("질문을 입력하세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 질문에 따른 최신 정보 반영 요청
            cmd = f"질문: {prompt}\n\n[지시: 질문 관련 핵심 정보만 아라비아 숫자로 제시하고, 마지막에 발문 1개만 해.]"
            response = model.generate_content(cmd)
            
            # 필터링: 괄호 속 내용 및 숫자 삭제
            text = re.sub(r'\([0-9,.\s]+\)', '', response.text)
            text = re.sub(r'\d+\.\s', '', text)
            
            st.markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})
