import time

import cv2
import numpy as np
from ultralytics import YOLO

from app import state


RTSP_URL = "rtsp://Application:ihcco58app@192.168.0.16:5541/streaming/channels/1"


entrance_zone = np.array([
    [300, 100],
    [500, 50],
    [650, 450],
    [400, 800]
], np.int32)


inside_zone = np.array([
    [650, 450],
    [500, 50],
    [1200, 50],
    [1200, 900],
    [400, 800]
], np.int32)


def open_camera():
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


def reconnect_camera(cap):
    print("RTSP lost. Reconnecting...")

    try:
        cap.release()
    except Exception:
        pass

    time.sleep(3)

    new_cap = open_camera()

    if not new_cap.isOpened():
        print("Reconnect failed. Retrying...")
        time.sleep(5)

    return new_cap


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
        thickness
    )

    cv2.rectangle(
        frame,
        (x - 10, y - text_height - 10),
        (x + text_width + 10, y + 10),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        text,
        (x, y),
        font,
        font_scale,
        (255, 255, 255),
        thickness
    )


def run_people_counter():
    model = YOLO("yolov8n.pt")

    cap = open_camera()

    while not cap.isOpened():
        print("Could not open RTSP stream. Retrying...")
        time.sleep(5)
        cap = open_camera()

    tracking_status = {}

    print("Real people counter started")

    while True:
        try:
            success, frame = cap.read()

            if not success or frame is None:
                cap = reconnect_camera(cap)
                continue

            results = model.track(
                frame,
                classes=[0],
                persist=True,
                tracker="botsort.yaml",
                verbose=False,
                conf=0.4,
                imgsz=640,
            )

            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                ids = results[0].boxes.id.cpu().numpy().astype(int)

                for box, track_id in zip(boxes, ids):
                    x1, y1, x2, y2 = box

                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)

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
                        2
                    )

                    cv2.putText(
                        frame,
                        f"ID:{track_id} {current_zone}",
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"{point}",
                        (center_x + 8, center_y + 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 255, 255),
                        1
                    )

                    cv2.circle(frame, point, 5, (0, 0, 255), -1)

            cv2.polylines(
                frame,
                [entrance_zone],
                isClosed=True,
                color=(255, 0, 0),
                thickness=2
            )

            cv2.putText(
                frame,
                "ENTRANCE",
                tuple(entrance_zone[0]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

            cv2.polylines(
                frame,
                [inside_zone],
                isClosed=True,
                color=(0, 255, 0),
                thickness=2
            )

            cv2.putText(
                frame,
                "INSIDE",
                tuple(inside_zone[0]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            draw_count_box(frame)

            state.set_latest_frame(frame)

        except Exception as error:
            print(f"People counter error: {error}")
            cap = reconnect_camera(cap)
            time.sleep(2)