from __future__ import annotations
import asyncio
from pydantic import BaseModel

from sqlalchemy import select,delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from env.Database import engine,async_session
from .modeloAsync import Foro,Comentario
from .base_models import ComentarioBase, ForoBase, UsuarioBase, Response 


#buscar en la tabla foro por id    
async def get_foro_all(id :int, async_session: async_sessionmaker[AsyncSession] = async_session):

    try:
        
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Foro).where(Foro.idforo == id)
                result = await session.execute(stm)
                foro = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado

                if foro:
                    comentarios = await session.execute(select(Comentario).where(Comentario.id_foro == foro.idforo))
                    comentarios = comentarios.scalars().all()
                    
                    foro1 = ForoBase(titulo=foro.titulo,imagen=foro.imagen,texto=foro.texto)
                    coments = []
                    for coment in comentarios:
                        coments.append(ComentarioBase(texto=coment.texto, fecha=coment.fecha))
                        
                    resp = Response(status="complete",message="hola",foro=foro1,comentario=coments)
                else:
                    resp = Response(status="incomplete",message=f"No se encontró un foro con el ID {id}",foro=None,comentario=None)

    except Exception as error:
        # Manejo de la excepción
        resp = Response(status="incomplete",message=f"Se ha producido un error al realizar la busqueda: {error}",foro=None,comentario=None)

    finally:
        await engine.dispose()
    return resp


async def eliminar_forodb(idforo:int,idusuario:int, async_session: async_sessionmaker[AsyncSession] = async_session):
    try:  
        async with async_session() as session:
            async with session.begin():
                stm = select(Foro).where(Foro.idforo == idforo)
                result = await session.execute(stm)
                foro = result.scalar()
                if(foro):
                    if(foro.id_Usuario == idusuario):
                        stm = delete(Foro).where(Foro.idforo == idforo)
                        await session.execute(stm)
                        return idforo
                    return
                return "Foro no existe"
    except Exception as error:
        # Manejo de la excepción
        return(f"Se ha producido un error al realizar la busqueda: {error}")
    finally:
        await engine.dispose()
        
async def insert_forodb(foro: Foro, async_session: async_sessionmaker[AsyncSession] = async_session) -> None:
    try:
        
        async with async_session() as session:
            async with session.begin():
                session.add(foro)
                await session.commit()
                session.refresh(foro)
                return(foro)
    except Exception as error:
        # Manejo de la excepción
        return(f"Se ha producido un error al insertar el foro: {error}")
    finally:
        await engine.dispose()
        
async def insert_coments_idforodb(id :int,comentario:Comentario, async_session: async_sessionmaker[AsyncSession] = async_session):
    response = {"status": "", "message": ""}
    try:
        async with async_session() as session:
            async with session.begin():
                if get_foro_all(id):
                    comentario.id_foro = id
                    session.add(comentario)
                    await session.commit()
                    session.refresh(comentario)
                    response["status"] = "Complete"
                    response["message"] = comentario
    except Exception as error:
        # Manejo de la excepción
        response["status"] = "error"
        response["message"] = f"Se ha producido un error al realizar la busqueda: {error}"
    finally:
        await engine.dispose()
    return response
        
        
        
        
        
        
        