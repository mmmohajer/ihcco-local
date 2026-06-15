import threading

people_count = 0
latest_frame = None

_lock = threading.Lock()


def get_people_count():
    with _lock:
        return people_count


def set_people_count(value: int):
    global people_count

    with _lock:
        people_count = max(value, 0)
        return people_count


def increment_people_count(amount: int):
    global people_count

    with _lock:
        people_count += amount
        people_count = max(people_count, 0)
        return people_count


def set_latest_frame(frame):
    global latest_frame

    with _lock:
        latest_frame = frame.copy()


def get_latest_frame():
    with _lock:
        if latest_frame is None:
            return None

        return latest_frame.copy()