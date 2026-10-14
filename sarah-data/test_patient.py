from datetime import date

from database.connection import SessionLocal

from models.patient import Patient


# Creamos una nueva sesión con la base de datos.
db = SessionLocal()


try:

    # Creamos un paciente como objeto Python.
    patient = Patient(
        id="patient-001",
        first_name="Juan",
        last_name="Pérez",
        rut="12.345.678-5",
        birth_date=date(1985, 5, 20),
        sex="M",
        email="juan.perez@example.com",
        phone="+56912345678",
        current_height=1.75,
        current_weight=82.5,
        lives_alone=False,
        bmi=26.9,
        context="Paciente con sobrepeso que desea mejorar sus hábitos de vida.",
        psychological_profile="Motivado, pero con dificultades para mantener hábitos a largo plazo.",
    )

    # Agregamos el paciente a la sesión.
    db.add(patient)

    # Confirmamos la transacción.
    db.commit()

    print("Paciente creado correctamente:")
    print("ID:", patient.id)
    print("Nombre:", patient.first_name, patient.last_name)


except Exception as e:

    # Si ocurre un error, deshacemos los cambios pendientes.
    db.rollback()

    print("Error al crear el paciente:")
    print(e)


finally:

    # Cerramos la sesión.
    db.close()





























from datetime import date

from repositories.patients import (
    create_patient,
    get_patient,
    update_patient,
    delete_patient,
)


# ----------------------------------------------------
# Create
# ----------------------------------------------------

print("=== CREATE ===")

patient = create_patient(
    first_name="Maria",
    last_name="Gonzalez",
    rut="15.234.567-8",
    birth_date=date(1990, 8, 12),
    sex="F",
    email="maria.gonzalez@example.com",
    phone="+56987654321",
    current_height=1.65,
    current_weight=70.0,
    lives_alone=True,
    bmi=25.7,
    context="Paciente que desea mejorar sus hábitos de vida.",
    psychological_profile="Motivada para realizar cambios.",
)

print("Paciente creado:")
print("ID:", patient.id)
print("Nombre:", patient.first_name, patient.last_name)


# ----------------------------------------------------
# Read
# ----------------------------------------------------

print("\n=== READ ===")

patient = get_patient(patient.id)

if patient:

    print("Paciente encontrado:")
    print("ID:", patient.id)
    print("Nombre:", patient.first_name, patient.last_name)
    print("RUT:", patient.rut)
    print("Email:", patient.email)

else:

    print("Paciente no encontrado.")


# ----------------------------------------------------
# Update
# ----------------------------------------------------

print("\n=== UPDATE ===")

patient = update_patient(
    patient.id,
    current_weight=68.5,
    email="maria.gonzalez.new@example.com",
)

if patient:

    print("Paciente actualizado:")
    print("Peso:", patient.current_weight)
    print("Email:", patient.email)

else:

    print("Paciente no encontrado.")


# ----------------------------------------------------
# Delete
# ----------------------------------------------------

print("\n=== DELETE ===")

deleted_patient = delete_patient(
    patient.id
)

if deleted_patient:

    print("Paciente eliminado:")
    print(
        "ID:",
        deleted_patient.id,
    )

else:

    print("Paciente no encontrado.")


# ----------------------------------------------------
# Verify deletion
# ----------------------------------------------------

print("\n=== VERIFY DELETE ===")

patient = get_patient(
    deleted_patient.id
)

if patient is None:

    print("El paciente ya no existe en la base de datos.")

else:

    print("ERROR: el paciente todavía existe.")
