from fastapi.responses import StreamingResponse

from app import state
from app.people_counter.utils.camera_service import generate_camera_frames


def get_people_count():
    return {
        "people_count": state.get_people_count(),
        "max_people_count": state.get_max_people_count(),
        "total_entries_today": state.get_total_entries_today(),
    }


def reset_people_count(payload):
    new_count = state.set_people_count(payload.people_count)

    return {
        "people_count": new_count,
        "max_people_count": state.get_max_people_count(),
        "total_entries_today": state.get_total_entries_today(),
    }


def live_camera_view():
    return StreamingResponse(
        generate_camera_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )

def reset_max_people_count(payload):
    new_max_count = state.set_max_people_count(payload.max_people_count)

    return {
        "people_count": state.get_people_count(),
        "max_people_count": new_max_count,
        "total_entries_today": state.get_total_entries_today(),
    }