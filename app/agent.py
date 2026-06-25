# 여행 코디네이터 Agent의 최상위 오케스트레이션을 직접 작성하는 파일입니다.
#
# 목표 흐름:
# 1) 사용자가 home_address, destination, nights 등을 입력합니다.
# 2) 숙소 agent가 destination 기준 숙소 후보 3가지를 찾습니다.
# 3) 맛집/일정 agent가 해당 지역 맛집 n가지와 가볼 만한 곳 m가지를 찾습니다.
# 4) 동선 agent가 집 주소, 숙소 후보, 맛집/관광지 후보를 받아 숙소별 최적 경로를 탐색합니다.
# 5) 일정 agent가 최적 동선 3가지를 바탕으로 장소, 시간, 이동 정보를 포함한 최종 일정 3가지를 산출합니다.
#
# 이 파일에 작성할 것:
# - create_agent 또는 LangGraph 그래프를 사용한 coordinator 생성 함수
# - accommodation, food_itinerary, route, final_schedule agent 호출 순서
# - 각 agent 사이에서 주고받을 중간 데이터 구조
# - 실패 시 재시도/부분 결과 처리 규칙
# - 최종 response_format 또는 structured_response 처리 방식
#
# 추천 함수 뼈대:
# - get_travel_coordinator_agent()
# - run_travel_coordinator(request)
# - stream_travel_coordinator(request)
#
# app/main.py의 /chat, /chat/stream에서 위 함수들을 import해서 연결하면 됩니다.
