from contextlib import asynccontextmanager
import threading

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.people_counter.router import router as people_counter_router
from app.people_counter.utils import counter_service, counter_service_new
from app.ws_router import router as ws_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(
        # target=counter_service.run_people_counter,
        target=counter_service_new.run_people_counter,
        # target=counter_service.start_test_counter,
        daemon=True
    )
    thread.start()
    yield


app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.0.111:3000",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@api_router.get("/")
def health_check():
    return {"message": "API is running"}


api_router.include_router(people_counter_router)

app.include_router(api_router)
app.include_router(ws_router)