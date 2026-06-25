from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    """Base model for API schemas."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class HealthResponse(ApiModel):
    """Response body for /healthz."""

    status: str = Field(default="ok")


class AgentPendingResponse(ApiModel):
    """Temporary response while the travel agents are implemented."""

    detail: str
    request_id: str | None = None


class Coordinates(ApiModel):
    """Latitude/longitude pair used by route-related agents."""

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class TravelPlanRequest(ApiModel):
    """User input for creating travel-plan candidates."""

    home_address: str = Field(min_length=1, description="사용자의 집 주소")
    destination: str = Field(min_length=1, description="서울, 대전, 부산 등 가고 싶은 여행지")
    nights: int = Field(ge=1, description="몇 박으로 갈지 나타내는 값")
    travelers: int = Field(default=1, ge=1, description="여행 인원")
    budget: int | None = Field(default=None, ge=0, description="총 예산 또는 참고 예산")
    preferences: list[str] = Field(
        default_factory=list,
        description="숙소, 맛집, 이동 방식, 일정 강도 등 사용자 선호 조건",
    )


class AccommodationCandidate(ApiModel):
    """Accommodation candidate produced by the accommodation agent."""

    name: str = Field(min_length=1, description="숙소명")
    address: str = Field(min_length=1, description="숙소 주소")
    price_per_night: int | None = Field(default=None, ge=0, description="1박 예상 가격")
    reason: str = Field(min_length=1, description="추천 이유")
    map_url: str | None = Field(default=None, description="지도 URL 또는 예약/상세 페이지 URL")
    coordinates: Coordinates | None = Field(default=None, description="동선 계산용 위치 정보")


class PlaceCandidate(ApiModel):
    """Restaurant or attraction candidate produced by the food/itinerary agent."""

    name: str = Field(min_length=1, description="장소명")
    address: str = Field(min_length=1, description="장소 주소")
    category: str = Field(min_length=1, description="restaurant, attraction 등 장소 분류")
    estimated_duration_minutes: int | None = Field(
        default=None,
        ge=1,
        description="예상 체류 시간(분)",
    )
    reason: str = Field(min_length=1, description="추천 이유")
    map_url: str | None = Field(default=None, description="지도 URL 또는 상세 페이지 URL")
    coordinates: Coordinates | None = Field(default=None, description="동선 계산용 위치 정보")


class FoodAndPlaceCandidates(ApiModel):
    """Grouped candidates from the food/itinerary discovery agent."""

    restaurants: list[PlaceCandidate] = Field(min_length=1, description="맛집 후보 n개")
    attractions: list[PlaceCandidate] = Field(min_length=1, description="가볼 만한 곳 후보 m개")


class RouteStop(ApiModel):
    """One stop in an optimized route."""

    name: str = Field(min_length=1, description="방문 장소명")
    address: str = Field(min_length=1, description="방문 장소 주소")
    category: str = Field(min_length=1, description="숙소, 맛집, 관광지 등 분류")
    move_from_previous: str | None = Field(default=None, description="이전 장소에서 오는 방법")
    travel_time_minutes_from_previous: int | None = Field(
        default=None,
        ge=0,
        description="이전 장소에서 오는 데 걸리는 시간(분)",
    )
    coordinates: Coordinates | None = Field(default=None, description="동선 계산용 위치 정보")


class RoutePlan(ApiModel):
    """Optimized route candidate for one accommodation option."""

    accommodation: AccommodationCandidate = Field(description="기준 숙소")
    ordered_stops: list[RouteStop] = Field(min_length=1, description="최적 방문 순서")
    total_travel_time_minutes: int | None = Field(default=None, ge=0, description="총 이동 시간(분)")
    route_summary: str = Field(min_length=1, description="동선 요약")


class ScheduleItem(ApiModel):
    """One scheduled activity in a final itinerary."""

    place: str = Field(min_length=1, description="방문 장소")
    start_time: str = Field(min_length=1, description="시작 시간. 예: 14:00")
    end_time: str = Field(min_length=1, description="종료 시간. 예: 15:30")
    move_from_previous: str | None = Field(default=None, description="이전 장소에서 오는 동선")
    note: str | None = Field(default=None, description="일정 참고 메모")


class DaySchedule(ApiModel):
    """A day-level schedule containing ordered schedule items."""

    day: int = Field(ge=1, description="여행 n일차")
    items: list[ScheduleItem] = Field(min_length=1, description="해당 일자의 일정 항목")


class FinalSchedule(ApiModel):
    """Final schedule candidate produced from one optimized route plan."""

    title: str = Field(min_length=1, description="일정 이름")
    route_plan: RoutePlan = Field(description="이 일정의 기반이 된 동선")
    days: list[DaySchedule] = Field(min_length=1, description="일자별 일정")


class TravelPlanResponse(ApiModel):
    """Final API response containing three travel schedule options."""

    answer: str = Field(min_length=1, description="사용자에게 보여줄 요약 답변")
    schedules: list[FinalSchedule] = Field(
        min_length=3,
        max_length=3,
        description="장소, 시간, 동선을 포함한 최종 일정 3가지",
    )
    used_agents: list[str] = Field(default_factory=list, description="응답 생성에 사용된 agent 목록")
    confidence: float | None = Field(default=None, ge=0, le=1, description="모델 판단 신뢰도")
    assumptions: list[str] = Field(default_factory=list, description="모델이 둔 가정 또는 사용자 확인 필요 사항")


# Agent 구현 시 연결할 권장 흐름:
# 1) TravelPlanRequest를 /chat 요청 본문으로 받습니다.
# 2) accommodation agent는 AccommodationCandidate 3개를 생성합니다.
# 3) food_itinerary agent는 FoodAndPlaceCandidates를 생성합니다.
# 4) route agent는 숙소별 후보와 장소 후보를 받아 RoutePlan 3개를 생성합니다.
# 5) final_schedule agent는 RoutePlan을 받아 FinalSchedule 3개를 생성합니다.
# 6) /chat은 TravelPlanResponse로 최종 응답합니다.
