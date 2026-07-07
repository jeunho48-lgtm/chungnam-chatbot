import streamlit as st
import google.generativeai as genai

# 1. 사이드바 설정
st.sidebar.title("🛠️ 교사 설정")
api_key = st.sidebar.text_input("Gemini API 키를 입력하세요:", type="password")

# 2. 메인 화면
st.title("🗺️ 충남 지역화 학습 AI")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 이전 대화 출력
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 사용자 입력 처리
        if prompt := st.chat_input("천안이나 아산에 대해 궁금한 점을 물어보세요!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # 프롬프트 구성
                full_prompt = f"""
                너는 초등학교 4학년을 위한 충남 지역화 학습 가이드야.
                정답을 바로 말하지 말고, 아이가 스스로 생각할 수 있도록 질문을 던져줘.
                번호나 항목명은 사용하지 말고 자연스러운 문장으로만 말해줘.
                질문: {prompt}
                """
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
else:
    st.warning("⚠️ 사이드바에 API 키를 입력하면 챗봇이 활성화됩니다.")
💡 수정 후 꼭 확인하세요!
코드 저장: 깃허브에서 기존 코드를 싹 지우고 위 코드를 붙여넣은 뒤, [Commit changes] 버튼을 꼭 누르세요.

스트림릿 새로고침: 스트림릿 페이지로 가서 새로고침(F5)을 하세요.

키 입력: 왼쪽 사이드바에 API 키를 다시 한번 정확히 붙여넣으세요.

결과 확인: 이제 챗봇이 API 키를 인식해서 정상적으로 답변을 시작할 겁니다.

이제 드디어 오류 없이 아이들과 수업할 수 있는 상태가 될 거예요! 바로 적용해 보시고 챗봇이 잘 대답하는지 확인해 주세요. 🚀
