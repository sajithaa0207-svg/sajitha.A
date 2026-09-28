from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz, QuizResponse
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# ============================================================
# EDU GENIE - FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EduGenie API",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class HealthResponse(BaseModel):
    status: str


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok"
    }


# ============================================================
# QUESTION & ANSWER
# ============================================================

@app.post("/qa")
async def qa(payload: TextRequest):
    try:
        result = answer_question(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ============================================================
# EXPLANATION
# ============================================================

@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        result = explain_topic(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ============================================================
# QUIZ
# ============================================================

@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: TextRequest):
    try:
        return generate_quiz(payload.text)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ============================================================
# SUMMARY
# ============================================================

@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        result = summarize_text(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ============================================================
# LEARNING RECOMMENDATIONS
# ============================================================

@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):
    try:
        result = get_learning_recommendations(payload.text)

        return {
            "result": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )