from fastapi import FastAPI

from api.routes import router
from fastapi import FastAPI

from api.routes import router
from api.auth_routes import router as auth_router


app = FastAPI()


app.include_router(router)

app.include_router(auth_router)


app = FastAPI(
    title="AI Interviewer API",
    description="Backend API for the AI technical interviewer",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "AI Interviewer API is running"
    }