import unicodedata
from repositories import patients as patient_repo


def normalize_text(text: str) -> str: 
    """Elimina tildes y pasa a minúsculas para comparaciones robustas."""
    text = text.lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def generate_sarah_response(patient_id: str, incoming_message: str) -> str:
    """Genera una respuesta contextualizada de Sarah considerando los datos clínicos del paciente."""
    patient = patient_repo.get_patient(patient_id)
    nombre = patient.first_name if patient else "estimado/a paciente"
    contexto = patient.context if patient and patient.context else ""

    text = normalize_text(incoming_message)

    # 1. Alertas de urgencia / síntomas graves
    if any(k in text for k in ["pecho", "infarto", "ahogo", "aire", "desmayo", "dificultad para respirar"]):
        return (
            f"Hola {nombre}. Lo que describes puede requerir atención médica inmediata. "
            "Por favor acude de inmediato al servicio de urgencias más cercano (CESFAM o SAPU) o comunícate con el 131 (SAMU)."
        )

    # 2. Dolores comunes o malestares generales
    if any(k in text for k in ["cabeza", "cefalea", "fiebre", "temperatura", "mareo"]):
        return (
            f"Comprendo que te sientas mal, {nombre}. Es importante monitorear si presentas otros síntomas como fiebre sobre 38°C o rigidez. "
            "Mantente hidratado/a y descansando. Si el malestar persiste por más de 24 horas, te sugiero agendar una hora médica con tu profesional asignado."
        )

    # 3. Consultas sobre peso, nutrición o estilo de vida
    if any(k in text for k in ["peso", "dieta", "comida", "ejercicio", "imc", "grasa"]):
        detalles_imc = f" (tu IMC registrado es {patient.bmi:.1f})" if patient and patient.bmi else ""
        return (
            f"Hola {nombre}. Con respecto a tus metas de salud{detalles_imc}, una alimentación balanceada y actividad física regular son fundamentales. "
            "Podemos coordinar una evaluación nutricional en tu centro de salud para ajustar un plan a tu medida."
        )

    # 4. Saludos
    if any(k in text for k in ["hola", "buen dia", "buenas tardes", "buenas noches", "saludos"]):
        intro_salud = f" Veo en tu ficha médica: '{contexto}'." if contexto else ""
        return (
            f"¡Hola {nombre}! Soy Sarah, tu asistente de salud virtual.{intro_salud} "
            "¿En qué te puedo orientar o ayudar el día de hoy?"
        )

    # 5. Agradecimientos o despedidas
    if any(k in text for k in ["gracias", "muchas gracias", "chao", "adios", "hasta luego"]):
        return f"De nada, {nombre}. Recuerda que estoy aquí para apoyarte en el seguimiento de tu salud. ¡Que tengas un excelente día!"

    # 6. Respuesta por defecto orientadora
    return (
        f"Gracias por escribirme, {nombre}. He registrado tu mensaje sobre '{incoming_message}'. "
        "Recuerda que estoy aquí para apoyarte en tu seguimiento médico preventivo. "
        "Si tienes dudas específicas sobre tu tratamiento o síntomas nuevos, podemos comunicarlo a tu equipo médico."
    )