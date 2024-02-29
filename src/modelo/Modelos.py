from typing import List
from typing import Optional
from sqlalchemy import ForeignKey,DateTime,String,Integer,select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = 'Usuario'
    idUsuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45))
    contraseña: Mapped[str] = mapped_column(String(45))

    foros: Mapped[List["Foro"]] = relationship('Foro', back_populates='usuario',cascade="all, delete-orphan")
    comentarios: Mapped[List["Comentario"]] = relationship('Comentario', back_populates='usuario',cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"Usuario(idUsuario={self.idUsuario!r}, nombre={self.nombre!r}, contraseña={self.contraseña!r})"

class Foro(Base):
    __tablename__ = 'foro'

    idforo: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[Optional[str]] = mapped_column(String(45))
    imagen: Mapped[Optional[str]] = mapped_column(String(45))
    texto: Mapped[Optional[str]] = mapped_column(String(45))
    id_Usuario: Mapped[int] = mapped_column(Integer, ForeignKey('Usuario.idUsuario'))

    usuario: Mapped[Usuario] = relationship('Usuario', back_populates='foros')
    comentarios: Mapped[List["Comentario"]] = relationship('Comentario', back_populates='foro')
    def __repr__(self) -> str:
        comentarios_repr = [str(comentario) for comentario in self.comentarios]
        return f"Foro(idforo={self.idforo!r}, titulo={self.titulo!r},imagen={self.imagen!r}, texto={self.texto!r},id_Usuario={self.id_Usuario!r},comentarios={comentarios_repr})"


class Comentario(Base):
    __tablename__ = 'Comentario'

    idComentario: Mapped[int] = mapped_column(Integer, primary_key=True)
    texto: Mapped[Optional[str]] = mapped_column(String)
    fecha: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    id_Usuario: Mapped[int] = mapped_column(Integer, ForeignKey('Usuario.idUsuario'))
    id_foro: Mapped[int] = mapped_column(Integer, ForeignKey('foro.idforo'))

    usuario: Mapped[Usuario] = relationship('Usuario', back_populates='comentarios')
    foro: Mapped[Foro] = relationship('Foro', back_populates='comentarios')
    def __repr__(self) -> str:
        return f"Comentario(id comentario={self.idComentario}, idusuario={self.id_Usuario},idcometario = {self.idComentario})"