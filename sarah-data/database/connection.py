import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Carga las variables definidas en el archivo .env
# Esto permite mantener la configuración fuera del código fuente.
load_dotenv()


# Obtiene la URL de conexión a PostgreSQL desde la variable de entorno.
DATABASE_URL = os.getenv("DATABASE_URL")


# Clase base para todos nuestros modelos ORM.
# Más adelante, Patient, Message, Conversation, etc.
# heredarán de esta clase.
#
# Base.metadata también permitirá a Alembic conocer
# la estructura de nuestras tablas.
class Base(DeclarativeBase):

    pass


# Crea el Engine de SQLAlchemy.
# El Engine administra las conexiones entre nuestra aplicación
# Python y la base de datos PostgreSQL.
#
# echo=True permite ver en la consola las consultas SQL
# que SQLAlchemy genera y ejecuta. Es útil durante el aprendizaje
# y el desarrollo, pero normalmente se desactiva en producción.
engine = create_engine(

    DATABASE_URL,

    echo=True,

)


# Crea una fábrica de sesiones SQLAlchemy.
# Cada vez que necesitemos trabajar con la base de datos,
# podremos crear una nueva sesión mediante:
#
#     db = SessionLocal()
#
# La sesión nos permitirá consultar, insertar, modificar
# y eliminar objetos persistidos en PostgreSQL.
SessionLocal = sessionmaker(

    bind=engine,

    # Evita que SQLAlchemy fuerce automáticamente
    # la sincronización de cambios antes de ciertas consultas.
    autoflush=False,

    # La aplicación controlará explícitamente las transacciones
    # mediante commit() y rollback().
    autocommit=False,

)

