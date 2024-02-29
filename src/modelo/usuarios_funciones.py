from __future__ import annotations
import asyncio

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import jwt

from env.Database import engine,async_session
from .modeloAsync import Usuario
from env.Token import SECRET_KEY
import os
from pydantic import BaseModel

class Response(BaseModel):
    status: str
    message: str
    data: str | None = None
    access_token: str | None = None




#Funciones para interactuar con la tabla --USUARIOS-- 
# session es opcional (async_session = async_sessionmaker(engine, expire_on_commit=False))

async def insert_usuario(user: Usuario, async_session: async_sessionmaker[AsyncSession] = async_session) -> None:
    try:
        
        async with async_session() as session:
            async with session.begin():
                stm = select(Usuario).where(Usuario.nombre == user.nombre)
                result = await session.execute(stm)
                result = result.scalar()
                if(result):
                   return (f"Usuario ya registrado {result}")
                session.add(user)
                await session.commit()
                session.refresh(user)
                return(f"usuario: {user.nombre} agreado ")
    except Exception as error:
        # Manejo de la excepción
        return(f"Se ha producido un error al insertar el usuario: {error}")
    finally:
        await engine.dispose()

#buscar en la tabla usuario por id    
async def get_usuario_id(id :int, async_session: async_sessionmaker[AsyncSession] = async_session):
    try:  
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Usuario).where(Usuario.idUsuario == id)
                result = await session.execute(stm)
                user_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                if user_obj:
                    print(user_obj)
                    print(id)
                else:
                    print(f"No se encontró un usuario con el ID {id}")
    except Exception as error:
        # Manejo de la excepción
        print(f"Se ha producido un error al realizar la busqueda: {error}")
    finally:
        await engine.dispose()
 
                    
async def get_usuario_nombre(user:Usuario, async_session: async_sessionmaker[AsyncSession] = async_session) -> Response:
    try:  
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Usuario).where(Usuario.nombre == user.nombre)
                result = await session.execute(stm)
                user_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                if user_obj:
                    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #objeto de clase CryptContext para Hasheo de la contraseña
                    if pwd_context.verify(user.contraseña, user_obj.contraseña): #verificacion de la contraseña
                        print(user_obj)
                        token = jwt.encode({'id': user_obj.idUsuario, 'nombre': user_obj.nombre}, SECRET_KEY, algorithm='HS256')
                        return Response(status="success",message="Inicio de sesión exitoso",data=str(user_obj),access_token=token)
                        
                    else:
                        return Response(status="fail",message="Inicio de sesión fallido Contraseña incorrecta")
                else:
                    return Response(status="fail",message="Inicio de sesión fallido Usuario incorrecto")

    except Exception as error:
        # Manejo de la excepción
        return(Response(status="ERROR",message=error))
    finally:
        await engine.dispose()

async def log_aut(token:str):
    from env.Token import verify_token
    return verify_token(token)

