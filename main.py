import time
from fastapi import FastAPI, Request, status
from fastapi.websockets import WebSocket
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.db.core.database import Database
database = Database()
from app.router.index import INDEX
from app.router.user import USER
from app.db.core.authorization import verify_access_token

app = FastAPI(
    title="Test API",
    description="Test CRUD API project",
    version="0.0.1"
)
templates = Jinja2Templates(directory="app/templates")
app.mount(path="/static",
          app=StaticFiles(directory="app/templates/static"),
          name="static")
app.include_router(router=INDEX)
app.include_router(router=USER)
app.add_middleware(middleware_class=TrustedHostMiddleware,
                   allowed_hosts=["localhost"])
origins = [
    "http://localhost:5000",
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# 서버 시작시 db connect
@app.on_event("startup")
async def startup():
    # database.connect()
    print("doing something with test DB")


# 서버 종료시 db disconnect
@app.on_event("shutdown")
async def shutdown():
    # database.dispose()
    print("doing something with test DB")


# middleware 사전처리
@app.middleware("http")
async def add_process_time_header(
        request: Request,
        call_next
):
    start_time = time.time()
    response = await call_next(request)
    access_token = request.cookies.get("access_token")
    if access_token is None and \
        not str(request.url).endswith("user/auth") and \
            not str(request.url).endswith("user/signin"):
        response = RedirectResponse(url="/user/signin",
                                    status_code=302)
    elif access_token is not None:
        access_user = await verify_access_token(access_token)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Websocket 테스트
@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()


# Jinja2 Template 테스트
@app.get(path="/",
         description="root path",
         status_code=status.HTTP_200_OK)
async def root_path(request: Request):
    login_token = await verify_access_token(request.cookies.get("access_token"))
    # 로그인 토큰 만료시 동작이 필요
    message = f"Hello {login_token}!" if login_token is not None else "User Token Expired"
    return templates.TemplateResponse(name="item.html",
                                      context={"request": request,
                                               "message": message})
