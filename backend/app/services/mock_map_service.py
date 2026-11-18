from datetime import datetime, timezone
from app.schemas.route import RouteQuery, RouteResult, RouteSegment
class MockMapService:
    def query(self, request: RouteQuery) -> RouteResult:
        segments = [RouteSegment(start_id=start, end_id=end, distance_meters=1200 + index * 350, estimated_minutes=18 + index * 5, traffic_info="模拟数据：道路通畅，建议步行前往。") for index, (start, end) in enumerate(zip(request.attraction_ids, request.attraction_ids[1:]))]
        return RouteResult(segments=segments, query_time=datetime.now(timezone.utc).isoformat())
