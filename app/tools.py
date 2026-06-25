from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool


@tool
def get_time(timezone: str = "Asia/Seoul") -> str:
    """Return the current time for an IANA timezone as an ISO-8601 string."""

    return datetime.now(ZoneInfo(timezone)).isoformat()


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression for practice purposes."""

    allowed_chars = set("0123456789+-*/(). %")
    if not expression or any(char not in allowed_chars for char in expression):
        return "계산할 수 없는 식입니다. 숫자와 기본 연산자만 입력하세요."

    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:  # pragma: no cover - agent 실습 중 직접 다듬을 영역
        return f"계산 실패: {exc}"


@tool
def fake_search(query: str) -> str:
    """Return a fake search result placeholder until a real search API is connected."""

    return f"'{query}'에 대한 검색 도구 자리입니다. 실제 검색 API 또는 MCP 도구로 교체하세요."
