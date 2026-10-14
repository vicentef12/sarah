from sqlalchemy import text

from database.connection import engine


# Abrimos una conexión utilizando el Engine de SQLAlchemy.
with engine.connect() as connection:

    # Ejecutamos una consulta SQL muy simple.
    # SELECT 1 no consulta ninguna tabla:
    # simplemente permite comprobar que la conexión funciona.
    result = connection.execute(text("SELECT 1"))

    # Obtenemos el primer valor del resultado.
    value = result.scalar()

    print("Conexión exitosa. Resultado:", value)
