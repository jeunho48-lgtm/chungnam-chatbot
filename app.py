import streamlit as st
import google.generativeai as genai
import random

# ==========================================
# 🔑 1. 선생님의 마스터 API 키 설정 
# ==========================================
# [중요] 여기에 선생님이 복사해두신 API 키들을 넣어주세요! 
# 예: ["키1", "키2", "키3"]
MASTER_KEYS = ["AIzaSyAiLq56Or8ByUqHEHp-BG3Wn_08BR7_dBc"]

# ==========================================
# 🖥️ 2. 사이드바 구성 (타인 공유용 입력창)
# ==========================================
st.sidebar.title("🛠️ 교사 설정 메뉴")
st.sidebar.markdown("---")

# 다른 선생님이 접속했을 때 본인의 키를 넣을 수 있는 창
user_api_key = st.sidebar.text_input(
    "다른 반 선생님이신가요? 본인의 API 키를 입력해 주세요:", 
    type="password"
)

# 최종 적용할 API 키 결정 (입력된 키가 있으면 우선 사용)
if user_api_key:
    final_api_key = user_api_key
    st.sidebar.success("🔑 공유받은 선생님의 API 키가 적용되었습니다!")
else:
    final_api_key = random.choice(MASTER_KEYS)

# Gemini API 인증 적용
genai.configure(api_key=final_api_key)

# ==========================================
# 🤖 3. 메인 챗봇 화면
# ==========================================
st.title("🗺️ 충청남도 지역화 학습 가이드 AI")
st.caption("초등학교 4학년을 위한 다정한 지역 탐구 대화방")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 질문 입력
if prompt := st.chat_input("천안이나 아산에 대해 궁금한 점을 물어보세요!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="""
너는 초등학교 4학년 학생들이 스스로 지리 데이터를 해석하고 탐구할 수 있도록 돕는 '충청남도 지역화 학습' 질문 가이드 AI야. 
정답을 바로 알려주기보다, 아이들이 생각할 수 있는 질문을 던져라. 
인구, 면적 등의 통계 수치는 반드시 최신 데이터를 검색하여 안내하고, 출력물에서 번호는 무조건 삭제해라.
"""
        )
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
