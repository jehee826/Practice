from fastapi import FastAPI, APIRouter
from api import fake_llm
from api import chat

# FastAPi 앱 선언
app = FastAPI()

# 모든요청앞에 /api를 붙이기위해 router하나 선언
api_router = APIRouter(prefix="/api")

# 다른파일에서 만든 router를 위 router에 붙인다 => 그냥 기존처럼 app에 붙였다면 /api가 들어가지못함
api_router.include_router(fake_llm.router)

# 중요 => router끼리 붙였다면 다 붙이고 제일 마지막에 app에 붙여줘야 모든 router를 인식한다
app.include_router(api_router)

@api_router.get("/status")
def status():
    return {"status": "ok"}
