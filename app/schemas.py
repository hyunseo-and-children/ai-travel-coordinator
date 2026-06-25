from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response body for /healthz."""

    status: str = Field(default="ok")


class AgentPendingResponse(BaseModel):
    """Temporary response while the travel agents and request schema are implemented."""

    detail: str
    request_id: str | None = None


# 아래부터는 사용자가 직접 작성할 request/response 규격 메모입니다.
#
# 1) TravelPlanRequest 후보 필드
#    - home_address: 사용자의 집 주소
#    - destination: 여행지. 예: 서울, 대전, 부산 등
#    - nights: 몇 박인지 나타내는 정수
#    - travelers: 여행 인원. 필요하면 성인/아동 구분
#    - budget: 총 예산 또는 숙소/식비/교통 예산
#    - preferences: 선호 조건. 예: 조용한 숙소, 맛집 위주, 아이 동반, 대중교통 우선
#
# 2) AccommodationCandidate 후보 필드
#    - name: 숙소명
#    - address: 숙소 주소
#    - price_per_night: 1박 예상 가격
#    - reason: 추천 이유
#    - map_url 또는 coordinates: 동선 계산에 필요한 위치 정보
#
# 3) FoodAndPlaceCandidate 후보 필드
#    - restaurants: 맛집 후보 n개
#    - attractions: 가볼 만한 곳 후보 m개
#    - 각 후보에는 name, address, category, estimated_duration, reason, coordinates 등을 포함
#
# 4) RoutePlan 후보 필드
#    - accommodation: 기준 숙소
#    - ordered_stops: 최적 방문 순서
#    - total_travel_time: 총 이동 시간
#    - route_summary: 동선 요약
#
# 5) FinalSchedule 후보 필드
#    - title: 일정 이름
#    - days: 일자별 일정
#    - 각 일정 항목에는 place, start_time, end_time, move_from_previous, note 등을 포함
#
# 6) ChatResponse 또는 TravelPlanResponse 후보 필드
#    - answer: 사용자에게 보여줄 요약 답변
#    - schedules: 최종 일정 3가지
#    - used_agents: 사용된 agent 목록
#    - confidence 또는 assumptions: 모델 판단 근거와 가정
