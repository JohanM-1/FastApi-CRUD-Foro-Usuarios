from typing import Annotated
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter,FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

from src.modelo.foro__funciones import get_foro_all,insert_forodb,eliminar_forodb,insert_coments_idforodb
from src.modelo.modeloAsync import Foro,Comentario
from .Usuarios import get_current_user
from src.modelo.base_models import ComentarioBase, ForoBase, UsuarioBase, Response
router = APIRouter()


          
@router.get("/foro/{idforo}",tags=["Foro"])
async def get_foroid(idforo:int):
    result = await get_foro_all(idforo)
    
    if result.status == "incomplete":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.message,
            )
    response = result.foro
    return result

@router.post("/foro/create",tags=["Foro"])
async def insert_forodbb(fore: ForoBase,current_user: Annotated[UsuarioBase, Depends(get_current_user)]):
    forodb = Foro()
    forodb.titulo = fore.titulo
    forodb.imagen= fore.imagen
    forodb.texto = fore.texto
    forodb.id_Usuario= current_user.id
    response = await insert_forodb(foro=forodb)
    return response

@router.delete("/foro/delete/{id:int}",tags=["Foro"])
async def delete_foro(id:int,current_user: Annotated[UsuarioBase, Depends(get_current_user)]): 

    result = await eliminar_forodb(id,current_user.id)
    if(result):
        return result
    raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    
@router.post("/foro/crearcomentario/{id:int}",tags=["comentarios"])  
async def insert_coment(id:int,comentariobase:ComentarioBase,current_user: Annotated[UsuarioBase, Depends(get_current_user)]):
    foro = await get_foro_all(id)
    if foro.status == "complete":
        comentario = Comentario(texto=comentariobase.texto,fecha=comentariobase.fecha,id_Usuario=current_user.id,id_foro=id)
        result = await insert_coments_idforodb(id,comentario)
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=foro.message,
            )

    
    
    