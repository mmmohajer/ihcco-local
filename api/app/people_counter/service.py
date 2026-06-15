from fastapi.responses import StreamingResponse

from app import state
from app.people_counter.utils.camera_service import generate_camera_frames

def get_people_count():
    return {
        "people_count": state.get_people_count()
    }

def reset_people_count(payload):
    new_count = state.set_people_count(payload.people_count)
    return {
        "people_count": new_count
    }

def live_camera_view():
    return StreamingResponse(
        generate_camera_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )