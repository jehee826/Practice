from fastapi import APIRouter

router = APIRouter(prefix="/llm")

@router.get("/test")
def fake():
    return {"test": "LLM입니다람쥐"}