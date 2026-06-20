import threading
from datetime import date

people_count = 0
max_people_count = 0
total_entries_today = 0

latest_frame = None

current_day = date.today()

_lock = threading.Lock()


def _check_new_day():
    global current_day
    global max_people_count
    global total_entries_today

    today = date.today()

    if today != current_day:
        current_day = today
        max_people_count = people_count
        total_entries_today = 0


def get_people_count():
    with _lock:
        return people_count


def get_max_people_count():
    with _lock:
        return max_people_count


def get_total_entries_today():
    with _lock:
        return total_entries_today


def set_people_count(value: int):
    global people_count
    global max_people_count

    with _lock:
        _check_new_day()

        people_count = max(value, 0)

        if people_count > max_people_count:
            max_people_count = people_count

        return people_count


def increment_people_count(amount: int):
    global people_count
    global max_people_count
    global total_entries_today

    with _lock:
        _check_new_day()

        old_count = people_count

        people_count += amount
        people_count = max(people_count, 0)

        if people_count > max_people_count:
            max_people_count = people_count

        # Count only entrances
        if amount > 0:
            total_entries_today += amount

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

def set_max_people_count(value: int):
    global max_people_count

    with _lock:
        _check_new_day()

        max_people_count = max(value, 0)

        return max_people_count