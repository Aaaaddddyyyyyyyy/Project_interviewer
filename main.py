from fastapi import FastAPI

from api.routes import router


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