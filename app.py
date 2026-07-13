import streamlit as st
import google.generativeai as genai
import itertools
import re

# 페이지 설정
st.set_page_config(page_title="충남 지역화 학습 AI", page_icon="🗺️", initial_sidebar_state="collapsed")
st.sidebar.title("🛠️ 설정")

api_keys = [
    st.sidebar.text_input("Gemini API 키 1:", type="password").strip(),
    st.sidebar.text_input("Gemini API 키 2:", type="password").strip(),
    st.sidebar.text_input("Gemini API 키 3:", type="password").strip()
]
valid_keys = [k for k in api_keys if k]

if "key_cycle" not in st.session_state or st.session_state.get("last_keys") != valid_keys:
    st.session_state.key_cycle = itertools.cycle(valid_keys) if valid_keys else None
    st.session_state.last_keys = valid_keys

st.title("🗺️ 충남 지역화 학습 AI")

system_instruction = """
너는 초등학교 4학년 사회 지역화 학습을 돕는 가이드야. 아래 규칙을 절대적으로 지켜라.
1. 데이터 활용: 아래 [학습 지식 데이터]를 최우선으로 사용하여 답변해라. 부족한 정보는 실시간 검색을 활용해라.
2. 표 형식: 데이터 정리 시 마크다운 표(Table)를 사용해라. 이후 표를 간단히 텍스트로 설명해라.
3. 숫자 및 청결: 모든 수치는 아라비아 숫자로만 표기해라.
4. 발문 제한: 답변 끝에는 반드시 딱 1개의 발문(질문)만 던져라.
5. 구조: 설명은 핵심만 간결하게 하고, 질문과 관련된 시각 자료(링크)를 적절히 포함해.

[학습 지식 데이터]
1. 천안시: 위치(충남 북동), 면적(636.5㎢), 인구(691,000명), 지형(태조산, 광덕산, 곡교천), 기온(봄 11, 여름 24, 가을 13, 겨울 -1), 강수량(봄 200, 여름 750, 가을 210, 겨울 70), 산업(반도체, 배터리), 유산(독립기념관, 유관순사적지), 특산물(호두과자, 거봉포도, 신고배)
2. 아산시: 위치(충남 북), 면적(542.1㎢), 인구(384,000명), 지형(영인산, 광덕산, 아산평야), 기온(봄 12, 여름 25, 가을 14, 겨울 0), 강수량(봄 210, 여름 800, 가을 220, 겨울 70), 산업(자동차, 디스플레이), 유산(현충사, 민속박물관, 장영실관), 특산물(아산맑은쌀, 배, 쪽파)
3. 당진시: 위치(충남 북서 해안), 면적(705.4㎢), 인구(171,000명), 지형(아미산, 갯벌), 기온(봄 11, 여름 24, 가을 14, 겨울 1), 강수량(봄 180, 여름 720, 가을 190, 겨울 60), 산업(철강), 유산(솔뫼성지, 필경사), 특산물(해나루쌀, 꽈리고추, 실치)
4. 서산시: 위치(충남 북서 해안), 면적(741.2㎢), 인구(181,000명), 지형(가야산, 팔봉산, 간척지), 기온(봄 11, 여름 24, 가을 14, 겨울 0), 강수량(봄 190, 여름 740, 가을 200, 겨울 60), 산업(석유화학, 자동차), 유산(마애삼존불, 해미읍성), 특산물(육쪽마늘, 어리굴젓, 감태)
5. 공주시: 위치(충남 중앙), 면적(864.2㎢), 인구(102,000명), 지형(계룡산, 무성산, 금강), 기온(봄 12, 여름 25, 가을 14, 겨울 -1), 강수량(봄 210, 여름 810, 가을 220, 겨울 65), 산업(역사관광), 유산(무령왕릉, 공산성), 특산물(공주알밤, 인절미)
6. 논산시: 위치(충남 남), 면적(555.2㎢), 인구(111,000명), 지형(대둔산, 논산평야, 탑정호), 기온(봄 12, 여름 25, 가을 15, 겨울 1), 강수량(봄 200, 여름 780, 가을 210, 겨울 70), 산업(딸기, 젓갈, 국방), 유산(관촉사, 돈암서원), 특산물(논산딸기, 강경젓갈)
7. 보령시: 위치(충남 남서 해안), 면적(574.0㎢), 인구(96,000명), 지형(성주산, 대천해수욕장), 기온(봄 11, 여름 24, 가을 14, 겨울 1), 강수량(봄 190, 여름 750, 가을 200, 겨울 65), 산업(관광, 화력발전), 유산(충청수영성, 석탄박물관), 특산물(보령김, 머드)
8. 부여군: 위치(충남 남), 면적(624.5㎢), 인구(61,000명), 지형(부소산, 백마강 분지), 기온(봄 12, 여름 25, 가을 14, 겨울 0), 강수량(봄 210, 여름 800, 가을 220, 겨울 70), 산업(관광, 수박, 멜론), 유산(부여박물관, 백제금동대향로), 특산물(굿뜨래수박, 멜론, 부여밤)
9. 홍성군: 위치(충남 서 중앙), 면적(446.7㎢), 인구(100,000명), 지형(용봉산, 오서산, 홍성천), 기온(봄 11, 여름 24, 가을 14, 겨울 0), 강수량(봄 190, 여름 740, 가을 200, 겨울 65), 산업(한우, 행정), 유산(홍주읍성, 김좌진생가), 특산물(홍성한우, 광천김, 토굴새우젓)
10. 예산군: 위치(충남 북서 내륙), 면적(542.3㎢), 인구(80,000명), 지형(가야산, 예당호), 기온(봄 11, 여름 24, 가을 14, 겨울 0), 강수량(봄 200, 여름 780, 가을 210, 겨울 70), 산업(사과, 관광), 유산(수덕사, 윤봉길의사기념관), 특산물(예산사과, 삽다리더덕)
11. 서천군: 위치(충남 남서 끝), 면적(366.1㎢), 인구(50,000명), 지형(희리산, 금강 하구 갯벌), 기온(봄 11, 여름 24, 가을 15, 겨울 1), 강수량(봄 190, 여름 730, 가을 200, 겨울 60), 산업(수산업, 생태관광), 유산(국립생태원, 한산모시관), 특산물(한산모시, 소곡주, 서천김)
12. 태안군: 위치(충남 서 끝 반도), 면적(516.1㎢), 인구(61,000명), 지형(신두리 해안사구), 기온(봄 11, 여름 23, 가을 14, 겨울 1), 강수량(봄 180, 여름 700, 가을 190, 겨울 65), 산업(해양관광, 화력발전), 유산(국립해양유물관, 마애삼존불), 특산물(꽃게, 대하, 육쪽마늘)
13. 금산군: 위치(충남 남동 끝), 면적(577.1㎢), 인구(50,000명), 지형(서대산, 금강 상류), 기온(봄 11, 여름 24, 가을 13, 겨울 -2), 강수량(봄 200, 여름 760, 가을 200, 겨울 60), 산업(인삼, 깻잎), 유산(금산인삼관, 칠백의총), 특산물(금산인삼, 추어탕, 깻잎)
14. 청양군: 위치(충남 중앙 내륙), 면적(479.1㎢), 인구(30,000명), 지형(칠갑산), 기온(봄 11, 여름 24, 가을 13, 겨울 -2), 강수량(봄 200, 여름 780, 가을 210, 겨울 70), 산업(농업, 산악관광), 유산(장곡사, 칠갑산천문대), 특산물(청양고추, 구기자, 밤)
15. 계룡시: 위치(충남 남동 내륙), 면적(60.7㎢), 인구(45,000명), 지형(계룡산, 고원), 기온(봄 11, 여름 24, 가을 13, 겨울 -1), 강수량(봄 200, 여름 750, 가을 210, 겨울 70), 산업(국방), 유산(계룡대, 사계고택), 특산물(계룡물엿, 팥거리떡)
"""

if valid_keys:
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
            # 키 순환 및 모델 호출 로직
            success = False
            for _ in range(len(valid_keys)):
                try:
                    current_key = next(st.session_state.key_cycle)
                    genai.configure(api_key=current_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-3-flash-preview",
                        generation_config={"temperature": 1.0},
                        system_instruction=system_instruction,
                        tools=[{"google_search_retrieval": {}}]
                    )
                    response = model.generate_content(prompt)
                    
                    text = response.text
                    text = re.sub(r'\(|\)', '', text)
                    text = re.sub(r'^\d+\.\s', '', text, flags=re.MULTILINE)
                    
                    st.markdown(text)
                    st.session_state.messages.append({"role": "assistant", "content": text})
                    success = True
                    break
                except Exception as e:
                    if "429" in str(e):
                        continue
                    else:
                        st.error(f"오류: {e}")
                        break
            
            if not success:
                st.error("모든 API 키의 사용량이 초과되었습니다. 잠시 후 다시 시도해주세요.")

else:
    st.info("👈 왼쪽 사이드바에 API 키를 최소 1개 이상 입력하세요.")
