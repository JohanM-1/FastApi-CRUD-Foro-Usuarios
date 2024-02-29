
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends,FastAPI
from src.modelo.modeloAsync import Usuario
from fastapi import FastAPI, Depends
from passlib.context import CryptContext
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.modelo.usuarios_funciones import get_usuario_nombre,insert_usuario,log_aut
from env.Token import verify_token



class UsuarioBase(BaseModel):
    nombre: str
    id: int
    
class CrearUsuario(BaseModel):
    nombre:str
    contraseña:str

class Response(BaseModel):
    status: str
    message: str
    data: str | None = None
    access_token: str | None = None


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Ruta para crear un nuevo usuario
@router.post("/crear",tags=["Usuario"])  
async def create_user(user: CrearUsuario):
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user.contraseña = pwd_context.hash(user.contraseña)
        db_user = Usuario(nombre=user.nombre, contraseña=user.contraseña)
        return await insert_usuario(db_user)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@router.post("/login",tags=["Usuario"])
async def login_usuario(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        db_user = Usuario(nombre=form_data.username, contraseña=form_data.password)
        result = await get_usuario_nombre(db_user)

        if result:
            return result
        else:
            return HTTPException(status_code=400, detail="Incorrect username or password")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al Iniciar : {str(e)}")




async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    str = verify_token(token)
    if not str:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    return str


@router.get("/users/me",tags=["Usuario"])
async def read_users_me(
    current_user: Annotated[UsuarioBase, Depends(get_current_user)]
):
    return current_user