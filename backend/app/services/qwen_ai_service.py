"""Qwen OpenAI-compatible adapter for the itinerary-planning module."""
import json

import httpx
from pydantic import ValidationError

from app.core.config import Settings
from app.core.exceptions import BusinessError
from app.models.attraction import Attraction
from app.schemas.plan import DayPlan, Itinerary, PlanItem, PlanRequest


class QwenAIService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, request: PlanRequest, attractions: list[Attraction]) -> Itinerary:
        if not self.settings.qwen_api_key:
            raise BusinessError("QWEN_NOT_CONFIGURED", "未配置 Qwen API Key，已无法调用智能规划服务", 503)
        candidates = [item for item in attractions if item.category in request.interests] or attractions
        if not candidates:
            raise BusinessError("NO_ATTRACTIONS", "暂无可用于规划的景点资料", 422)
        payload = {
            "model": self.settings.qwen_model,
            "messages": [
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": self._user_prompt(request, candidates)},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }
        try:
            response = httpx.post(
                f"{self.settings.qwen_base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {self.settings.qwen_api_key}"},
                json=payload,
                timeout=90,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return self._validate_result(json.loads(content), request, {item.attraction_id for item in candidates})
        except (httpx.HTTPError, KeyError, json.JSONDecodeError, ValidationError, ValueError) as exc:
            raise BusinessError("QWEN_PLAN_FAILED", "智能规划服务暂时不可用，请稍后重试", 503) from exc

    @staticmethod
    def _system_prompt() -> str:
        return (
            "你是北京旅行行程规划助手。只能使用候选景点中的 attraction_id；"
            "必须输出 JSON 对象，格式为 {\"daily_plans\":[{\"day\":1,\"attraction_ids\":[1,2]}]}。"
            "不得输出 Markdown、解释或候选名单之外的景点。"
        )

    @staticmethod
    def _user_prompt(request: PlanRequest, attractions: list[Attraction]) -> str:
        candidates = [
            {"attraction_id": item.attraction_id, "name": item.name, "category": item.category,
             "duration": item.duration, "opening_hours": item.opening_hours,
             "latitude": float(item.latitude), "longitude": float(item.longitude)}
            for item in attractions
        ]
        return json.dumps({"days": request.days, "interests": request.interests, "pace": request.pace, "candidates": candidates}, ensure_ascii=False)

    @staticmethod
    def _validate_result(raw: dict, request: PlanRequest, valid_ids: set[int]) -> Itinerary:
        days = raw.get("daily_plans")
        if not isinstance(days, list) or len(days) != request.days:
            raise ValueError("invalid day count")
        seen: set[int] = set()
        result: list[DayPlan] = []
        for expected_day, value in enumerate(days, start=1):
            ids = value.get("attraction_ids", []) if isinstance(value, dict) else []
            if not isinstance(value, dict) or value.get("day") != expected_day or not isinstance(ids, list) or not ids:
                raise ValueError("invalid day plan")
            if any(not isinstance(item, int) or item not in valid_ids or item in seen for item in ids):
                raise ValueError("invalid attraction id")
            seen.update(ids)
            result.append(DayPlan(day=expected_day, attractions=[PlanItem(attraction_id=item, order=index + 1) for index, item in enumerate(ids)]))
        return Itinerary(days=request.days, interests=request.interests, pace=request.pace, daily_plans=result)
