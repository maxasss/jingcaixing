"""High AMap Web Service adapter. The key is server-only configuration."""
from datetime import datetime, timezone

import httpx

from app.core.config import Settings
from app.core.exceptions import BusinessError
from app.models.attraction import Attraction
from app.schemas.route import RouteQuery, RouteResult, RouteSegment


class AMapMapService:
    # v3 responses include both distance and duration, which are required by
    # the route-text UI. The configured Web Service key works for this API.
    base_url = "https://restapi.amap.com/v3/direction"

    def __init__(self, settings: Settings):
        if not settings.amap_web_service_key:
            raise BusinessError("AMAP_NOT_CONFIGURED", "未配置高德 Web 服务 API Key", 503)
        self.key = settings.amap_web_service_key

    def query(self, request: RouteQuery, attractions: dict[int, Attraction]) -> RouteResult:
        missing = [item for item in request.attraction_ids if item not in attractions]
        if missing:
            raise BusinessError("ATTRACTION_NOT_FOUND", "路线中存在无效景点", 404)
        segments = [self._query_segment(attractions[start], attractions[end], request.travel_mode) for start, end in zip(request.attraction_ids, request.attraction_ids[1:])]
        return RouteResult(provider="amap", segments=segments, query_time=datetime.now(timezone.utc).isoformat())

    def _query_segment(self, start: Attraction, end: Attraction, mode: str) -> RouteSegment:
        params = {
            "key": self.key,
            "origin": f"{float(start.longitude):.6f},{float(start.latitude):.6f}",
            "destination": f"{float(end.longitude):.6f},{float(end.latitude):.6f}",
        }
        if mode == "driving":
            params["strategy"] = 4  # avoid congestion
        try:
            response = httpx.get(f"{self.base_url}/{mode}", params=params, timeout=10)
            response.raise_for_status()
            body = response.json()
            if str(body.get("status")) != "1" or not body.get("route", {}).get("paths"):
                raise ValueError(body.get("info", "高德未返回可用路线"))
            path = body["route"]["paths"][0]
            traffic_lights = path.get("traffic_lights")
            traffic = f"高德实时路线：已采用躲避拥堵策略，途经约 {traffic_lights} 个红绿灯。" if mode == "driving" else "步行路线：高德未提供实时拥堵状态。"
            return RouteSegment(start_id=start.attraction_id, end_id=end.attraction_id, distance_meters=int(float(path["distance"])), estimated_minutes=max(1, round(float(path["duration"]) / 60)), traffic_info=traffic)
        except (httpx.HTTPError, KeyError, TypeError, ValueError) as exc:
            raise BusinessError("AMAP_ROUTE_FAILED", "高德路线服务暂时不可用，请稍后重试", 502) from exc
