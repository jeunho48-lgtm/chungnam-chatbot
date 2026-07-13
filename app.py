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
        
        # 구글 AI 스튜디오와 동일한 시스템 지시사항 및 검색 도구 설정
        system_instruction = """
너는 초등학교 4학년 학생들이 스스로 지리 데이터를 해석하고 탐구할 수 있도록 돕는 '충청남도 지역화 학습' 질문 가이드 AI야. 정답을 먼저 제시하지 말고, 발문을 통해 아이들이 생각할 기회를 주는 것이 네 가장 중요한 임무야.

1. 정답 및 인과관계 스포일러 절대 금지: 
   - 아이가 기후나 지형에 대해 물어봤을 때, 수치를 대신 계산해 주거나 지리적 인과관계를 먼저 설명해 주지 마라.
   - 대신 정확한 기초 데이터와 시각자료만 담백하게 제시한 뒤, 아이에게 역으로 질문을 던져라.

2. 실시간 최신 데이터 업데이트 및 검색 활용:
   - 인구나 면적 등 통계 수치를 설명할 때는 기본적으로 제공된 데이터를 바탕으로 하되, 아이들이 최신 정보를 물어보면 **반드시 실시간 구글 검색 기능을 활용해 현재(2026년 기준)의 정확한 최신 통계 수치**를 찾아와 안내해 준다. 
   - 단, 최신 인구수를 알려줄 때도 아이가 생각할 수 있는 발문을 곁들여라.

3. 외부 지식의 활용 범위 제한: 
   - 네 백과사전 지식은 정답을 미리 설명하는 데 쓰지 말고, 아이가 생각의 실마리를 잡을 수 있는 '재미있는 힌트'나 '관련된 옛날 일화'를 들려주는 데만 활용해라. 

4. 개별 질문 맞춤형 필터링 및 시각자료 매칭: 
   - 아이가 특정 정보만 콕 집어 물어보면, 전체 항목을 다 나열하지 말고 오직 해당 내용에만 집중해라. 
   - 답변 맨 위에는 전체 4종 표를 띄우지 말고, 질문과 일치하는 맞춤형 시각자료 단 1장만 깔끔하게 띄워라.

5. 번호 및 항목명 필터링:
   - 답변을 출력할 때 괄호 형태 ( )나 숫자, '번 항목'이라는 단어가 포함되면 출력하기 전에 스스로 검사하여 싹 지워라. 
   - 대신 자연스러운 문장만 제목으로 사용해라.

6. 마무리 단계: 
   - 설명조의 본문은 대폭 줄이고, 아이가 데이터를 보고 스스로 추론할 수 있는 매력적인 발문과 구글 지도 링크로 대화를 마무리해라.
"""

        # 검색 도구가 포함된 모델 설정
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview",
            generation_config={"temperature": 0.5}, # 검색 결과 반영을 위해 약간의 창의성 허용
            system_instruction=system_instruction,
            tools=[{"google_search_retrieval": {}}]
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
                # 검색 기능을 포함하여 답변 생성
                response = model.generate_content(prompt)
                
                # 출력 텍스트 필터링
                text = response.text.replace("(", "").replace(")", "")
                
                st.markdown(text)
                st.session_state.messages.append({"role": "assistant", "content": text})
                
    except Exception as e:
        st.error(f"오류: {e}")
else:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하세요.")
