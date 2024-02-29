from fastapi import FastAPI
from src.Routers.Usuarios import router as user_router
from src.Routers.Foro import router as foro_router

app = FastAPI()

app.include_router(user_router)
app.include_router(foro_router)