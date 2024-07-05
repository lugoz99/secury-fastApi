from fastapi import FastAPI
from database.db import Base, engine
from routes.user import router as user_router
from routes.rol import router as rol_router
from routes.permission import router as permission_router
from routes.auth import router as auth_router
from routes.rol_permission import router as permission_rol

app = FastAPI()
app.include_router(user_router)
app.include_router(rol_router)
app.include_router(permission_router)
app.include_router(auth_router)
app.include_router(permission_rol)
Base.metadata.create_all(bind=engine)


def read_root():
    return {"Hello": "World security"}
