import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import state


router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"]
)


@router.websocket("/people-counter")
async def people_counter_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({
                "people_count": state.get_people_count(),
                "max_people_count": state.get_max_people_count(),
                "total_entries_today": state.get_total_entries_today(),
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")