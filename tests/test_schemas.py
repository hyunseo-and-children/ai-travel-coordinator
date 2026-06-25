import unittest

from pydantic import ValidationError

from app.schemas import (
    AccommodationCandidate,
    Coordinates,
    DaySchedule,
    FinalSchedule,
    FoodAndPlaceCandidates,
    PlaceCandidate,
    RoutePlan,
    RouteStop,
    ScheduleItem,
    TravelPlanRequest,
    TravelPlanResponse,
)


class TravelSchemaTest(unittest.TestCase):
    def test_travel_plan_request_accepts_required_trip_inputs(self):
        request = TravelPlanRequest(
            home_address="서울시 강남구 테헤란로 1",
            destination="부산",
            nights=2,
            travelers=3,
            budget=700000,
            preferences=["바다 근처 숙소", "대중교통 우선"],
        )

        self.assertEqual(request.destination, "부산")
        self.assertEqual(request.nights, 2)
        self.assertEqual(request.travelers, 3)
        self.assertEqual(request.preferences, ["바다 근처 숙소", "대중교통 우선"])

    def test_travel_plan_request_rejects_zero_nights(self):
        with self.assertRaises(ValidationError):
            TravelPlanRequest(
                home_address="서울시 강남구 테헤란로 1",
                destination="부산",
                nights=0,
            )

    def test_food_and_place_candidates_groups_restaurants_and_attractions(self):
        candidates = FoodAndPlaceCandidates(
            restaurants=[
                PlaceCandidate(
                    name="돼지국밥집",
                    address="부산 중구",
                    category="restaurant",
                    estimated_duration_minutes=60,
                    reason="부산 대표 음식",
                    coordinates=Coordinates(latitude=35.1796, longitude=129.0756),
                )
            ],
            attractions=[
                PlaceCandidate(
                    name="광안리해수욕장",
                    address="부산 수영구",
                    category="attraction",
                    estimated_duration_minutes=90,
                    reason="야경과 바다 동선이 좋음",
                )
            ],
        )

        self.assertEqual(candidates.restaurants[0].category, "restaurant")
        self.assertEqual(candidates.attractions[0].name, "광안리해수욕장")

    def test_travel_plan_response_requires_three_final_schedules(self):
        accommodation = AccommodationCandidate(
            name="해운대 호텔",
            address="부산 해운대구",
            price_per_night=120000,
            reason="주요 관광지 접근성이 좋음",
        )
        stop = RouteStop(
            name="광안리해수욕장",
            address="부산 수영구",
            category="attraction",
            move_from_previous="지하철 20분",
            travel_time_minutes_from_previous=20,
        )
        route = RoutePlan(
            accommodation=accommodation,
            ordered_stops=[stop],
            total_travel_time_minutes=90,
            route_summary="숙소에서 해변 중심으로 이동",
        )
        item = ScheduleItem(
            place="광안리해수욕장",
            start_time="14:00",
            end_time="15:30",
            move_from_previous="숙소에서 지하철 20분",
            note="도착 후 산책",
        )
        schedule = FinalSchedule(
            title="해운대 숙소 기반 일정",
            route_plan=route,
            days=[DaySchedule(day=1, items=[item])],
        )

        response = TravelPlanResponse(
            answer="숙소별 최적 일정 3가지를 정리했습니다.",
            schedules=[schedule, schedule, schedule],
            used_agents=["accommodation", "food_itinerary", "route", "final_schedule"],
            confidence=0.85,
            assumptions=["실시간 예약 가능 여부는 별도 확인 필요"],
        )

        self.assertEqual(len(response.schedules), 3)
        self.assertEqual(response.confidence, 0.85)

        with self.assertRaises(ValidationError):
            TravelPlanResponse(
                answer="일정이 부족합니다.",
                schedules=[schedule, schedule],
                used_agents=[],
                confidence=0.5,
            )


if __name__ == "__main__":
    unittest.main()
