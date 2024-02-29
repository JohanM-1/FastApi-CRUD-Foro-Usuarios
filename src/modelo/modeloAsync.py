from __future__ import annotations
import asyncio
from typing import List,Optional


from sqlalchemy import ForeignKey,DateTime,Integer,String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from env.Database import engine

#ORM TABLES --USUARIO-COMENTARIO-FORO--
class Base(AsyncAttrs, DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = 'Usuario'
    idUsuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45))
    contraseña: Mapped[str] = mapped_column(String(60))

    foros: Mapped[List["Foro"]] = relationship('Foro', back_populates='usuario',cascade="all, delete-orphan")
    comentarios: Mapped[List["Comentario"]] = relationship('Comentario', back_populates='usuario',cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"Id={self.idUsuario!r}, Nombre={self.nombre!r}"


class Foro(Base):
    __tablename__ = 'foro'

    idforo: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(45))
    imagen: Mapped[str] = mapped_column(String(45))
    texto: Mapped[str] = mapped_column(String(45))
    id_Usuario: Mapped[int] = mapped_column(Integer, ForeignKey('Usuario.idUsuario'),nullable=False)

    usuario: Mapped[Usuario] = relationship('Usuario', back_populates='foros')
    comentarios: Mapped[List["Comentario"]] = relationship('Comentario', back_populates='foro')
    def __repr__(self) -> str:
        comentarios_repr = [str(comentario) for comentario in self.comentarios]
        return f"Foro(idforo={self.idforo!r}, titulo={self.titulo!r},imagen={self.imagen!r}, texto={self.texto!r},id_Usuario={self.id_Usuario!r},comentarios={comentarios_repr})"

class Comentario(Base):
    __tablename__ = 'Comentario'

    idComentario: Mapped[int] = mapped_column(Integer, primary_key=True)
    texto: Mapped[str] = mapped_column(String(45))
    fecha: Mapped[DateTime] = mapped_column(DateTime)
    id_Usuario: Mapped[int] = mapped_column(Integer, ForeignKey('Usuario.idUsuario'),nullable=False)
    id_foro: Mapped[int] = mapped_column(Integer, ForeignKey('foro.idforo'),nullable=False)

    usuario: Mapped[Usuario] = relationship('Usuario', back_populates='comentarios')
    foro: Mapped[Foro] = relationship('Foro', back_populates='comentarios')
    def __repr__(self) -> str:
        return f"Comentario(id comentario={self.idComentario}, idusuario={self.id_Usuario},idcometario = {self.idComentario})"


#Creacion de tablas en la base de datos "asyncio.run(async_main())"
async def async_main() -> None:
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()




