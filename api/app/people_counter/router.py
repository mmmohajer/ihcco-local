from fastapi import APIRouter

from app.people_counter.schemas import CountResetRequest
from app.people_counter import service


router = APIRouter(
    prefix="/people-counter",
    tags=["People Counter"]
)

@router.get("/count")
def get_people_count():
    return service.get_people_count()

@router.post("/count/reset")
def reset_people_count(payload: CountResetRequest):
    return service.reset_people_count(payload)

@router.get("/live-view")
def live_camera_view():
    return service.live_camera_view()