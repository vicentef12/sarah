#modelo ORM

from sqlalchemy import String  #almacena texto
from sqlalchemy.orm import Mapped, mapped_column, relationship  #relaciona tablas
from database.connection import Base  #importa la conexion a la base de datos

class HealthCenter(Base):
    __tablename__ = "health_centers"  #nombre de la tabla en la base de datos

    id: Mapped[str] = mapped_column(primary_key=True)  #columna id, clave primaria
    name: Mapped[str] = mapped_column(String(100), nullable=False)  #columna nombre, no nula
    city: Mapped[str] = mapped_column(String(100), nullable=False)  #columna ciudad, no nula
    address: Mapped[str] = mapped_column(String(200), nullable=False)  #columna direccion, no nula
    phone: Mapped[str] = mapped_column(String(20), nullable=False)  #columna telefono, no nula
    email: Mapped[str] = mapped_column(String(100), nullable=False)  #columna email, no nula

    professionals: Mapped[list["Professional"]] = relationship(back_populates="health_center")  #relacion con profecionales 

