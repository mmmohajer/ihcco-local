# app/people_counter/real_counter.py
# Final two-thread version:
# - camera_reader always reads RTSP and immediately updates raw live view
# - yolo_processor processes the latest raw frame and overwrites live view with annotated frame
# - reconnects RTSP automatically
# - keeps people count logic: entrance -> inside = +1, inside -> entrance = -1

import threading
import time

import cv2
import numpy as np
from ultralytics import YOLO

from app import state

# RTSP_URL = "rtsp://Application:ihcco58app@99.209.90.226:5541/streaming/channels/1"
RTSP_URL = "rtsp://Application:ihcco58app@192.168.0.16:5541/streaming/channels/1"
MODEL_PATH = "yolov8n.pt"

latest_raw_frame = None
raw_frame_lock = threading.Lock()


entrance_zone = np.array([
    [210, 100],
    [500, 50],
    [900, 0],
    [930, 450],
    [950, 600],
    [550, 600],
    [500, 760]
], np.int32)


inside_zone = np.array([
    [900, 0],
    [1920, 0],
    [1920, 1050],
    [0, 1250],
    [500, 760],
    [550, 600],
    [950, 600],
], np.int32)


def open_camera():
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


def camera_reader():
    global latest_raw_frame

    cap = open_camera()

    while not cap.isOpened():
        print("Could not open RTSP stream. Retrying...")
        time.sleep(5)
        cap = open_camera()

    print("Camera reader started")

    while True:
        success, frame = cap.read()

        if not success or frame is None:
            print("RTSP lost in camera reader. Reconnecting...")

            try:
                cap.release()
            except Exception:
                pass

            time.sleep(3)
            cap = open_camera()
            continue

        with raw_frame_lock:
            latest_raw_frame = frame.copy()

        # Important:
        # Always update live-view with raw frame.
        # If YOLO is slow or errors, the camera feed still stays alive.
        # state.set_latest_frame(frame)


def get_latest_raw_frame():
    with raw_frame_lock:
        if latest_raw_frame is None:
            return None

        return latest_raw_frame.copy()


def get_zone(point, previous_zone):
    if cv2.pointPolygonTest(entrance_zone, point, False) >= 0:
        return "entrance"

    if cv2.pointPolygonTest(inside_zone, point, False) >= 0:
        return "inside"

    return previous_zone


def draw_count_box(frame):
    people_count = state.get_people_count()
    text = f"PEOPLE COUNT: {people_count}"

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    x, y = 30, 50

    (text_width, text_height), _ = cv2.getTextSize(
        text,
        font,
        font_scale,
        thickness,
    )

    cv2.rectangle(
        frame,
        (x - 10, y - text_height - 10),
        (x + text_width + 10, y + 10),
        (0, 0, 0),
        -1,
    )

    cv2.putText(
        frame,
        text,
        (x, y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
    )


def draw_zones(frame):
    cv2.polylines(
        frame,
        [entrance_zone],
        isClosed=True,
        color=(255, 0, 0),
        thickness=2,
    )

    cv2.putText(
        frame,
        "ENTRANCE",
        tuple(entrance_zone[0]),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )

    cv2.polylines(
        frame,
        [inside_zone],
        isClosed=True,
        color=(0, 255, 0),
        thickness=2,
    )

    cv2.putText(
        frame,
        "INSIDE",
        tuple(inside_zone[0]),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2,
    )


def process_detection(frame, boxes, ids, tracking_status):
    for box, track_id in zip(boxes, ids):
        x1, y1, x2, y2 = box

        center_x = int((x1 + x2) / 2)
        # center_y = int((y1 + y2) / 2)
        center_y = int(y1)
        point = (center_x, center_y)

        previous_zone = tracking_status.get(track_id, "unknown")
        current_zone = get_zone(point, previous_zone)

        if previous_zone == "entrance" and current_zone == "inside":
            state.increment_people_count(1)
            print(
                f"ENTER: ID {track_id} | "
                f"{previous_zone} -> {current_zone} | "
                f"count={state.get_people_count()}"
            )

        elif previous_zone == "inside" and current_zone == "entrance":
            state.increment_people_count(-1)
            print(
                f"EXIT: ID {track_id} | "
                f"{previous_zone} -> {current_zone} | "
                f"count={state.get_people_count()}"
            )

        tracking_status[track_id] = current_zone

        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"ID:{track_id} {current_zone}",
            (int(x1), int(y1) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"{point}",
            (center_x + 8, center_y + 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 255, 255),
            1,
        )

        cv2.circle(
            frame,
            point,
            5,
            (0, 0, 255),
            -1,
        )


def yolo_processor():
    model = YOLO(MODEL_PATH)
    tracking_status = {}

    print("YOLO processor started")

    while True:
        frame = get_latest_raw_frame()

        if frame is None:
            time.sleep(0.05)
            continue

        try:
            results = model.track(
                frame,
                classes=[0],
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False,
                conf=0.4,
                imgsz=640,
            )

            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                ids = results[0].boxes.id.cpu().numpy().astype(int)

                process_detection(
                    frame=frame,
                    boxes=boxes,
                    ids=ids,
                    tracking_status=tracking_status,
                )

            draw_zones(frame)
            draw_count_box(frame)

            # Overwrite raw live-view with annotated frame when YOLO is ready.
            state.set_latest_frame(frame)

        except Exception as error:
            print(f"YOLO processor error: {error}")
            time.sleep(1)


def run_people_counter():
    threading.Thread(
        target=camera_reader,
        daemon=True,
    ).start()

    threading.Thread(
        target=yolo_processor,
        daemon=True,
    ).start()

    print("People counter service started")

    while True:
        time.sleep(60)
