import time
import cv2

from app import state

def generate_camera_frames():
    while True:
        frame = state.get_latest_frame()

        if frame is None:
            time.sleep(0.1)
            continue

        success, buffer = cv2.imencode(".jpg", frame)

        if not success:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )