
import datetime
from typing import Optional
from pydantic import BaseModel


class ComentarioBase(BaseModel):
    texto:str
    fecha:datetime.datetime 

class ForoBase(BaseModel):
    titulo:str
    imagen:str
    texto:str
    
class UsuarioBase(BaseModel):
    nombre: str
    id: int
      
class Response(BaseModel):
    status: str
    message: str 
    foro:Optional[ForoBase]
    comentario:Optional[list]