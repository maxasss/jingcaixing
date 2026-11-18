from pydantic import BaseModel, Field
class RouteQuery(BaseModel): attraction_ids: list[int] = Field(min_length=2); travel_mode: str = "walking"
class RouteSegment(BaseModel): start_id: int; end_id: int; distance_meters: int; estimated_minutes: int; traffic_info: str
class RouteResult(BaseModel): provider: str = "mock"; segments: list[RouteSegment]; query_time: str
