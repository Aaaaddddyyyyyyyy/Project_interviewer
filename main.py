from fastapi import FastAPI

from api.routes import router
from api.auth_routes import router as auth_router
from api.tts_routes import router as tts_router


app = FastAPI()

app.include_router(router)
app.include_router(auth_router)
app.include_router(tts_router)