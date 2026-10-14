"""
client.py
Cliente de prueba integral para evaluar los servicios REST de Sarah y el asistente Sarah IA.
"""

import sys
import random
import requests

BASE_URL = "http://127.0.0.1:8000"


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(f" {title}") 
    print("=" * 60)


def run_pipeline():
    # -------------------------------------------------------------
    # 0. Verificar salud de la API
    # -------------------------------------------------------------
    print_separator("0. VERIFICANDO CONEXIÓN CON LA API")
    try:
        res = requests.get(f"{BASE_URL}/")
        if res.status_code == 200:
            print("✅ API en línea:", res.json())
        else:
            print("⚠️ API respondió con código:", res.status_code)
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API.")
        print("Asegúrate de que 'uvicorn api.main:app --reload --port 8000' esté corriendo.")
        sys.exit(1)

    # RUT dinámico para evitar colisiones por 'unique' en la BD
    rut_sufijo = random.randint(100, 999)

    # -------------------------------------------------------------
    # 1. Crear Centro de Salud
    # -------------------------------------------------------------
    print_separator("1. CREANDO CENTRO DE SALUD")
    center_payload = {
        "name": "CESFAM San José de la Mariquina",
        "city": "San José de la Mariquina",
        "address": "Calle Central 123",
        "phone": "+56911223344",
        "email": "contacto@cesfam-mariquina.cl",
    }
    res_center = requests.post(f"{BASE_URL}/health-centers/", json=center_payload)
    if res_center.status_code not in (200, 201):
        print("❌ Error al crear centro de salud:", res_center.text)
        sys.exit(1)
    center_data = res_center.json()
    center_id = center_data["id"]
    print(f"✅ Centro creado exitosamente:")
    print(f"   ID: {center_id}")
    print(f"   Nombre: {center_data['name']} ({center_data['city']})")

    # -------------------------------------------------------------
    # 2. Crear Profesional de Salud
    # -------------------------------------------------------------
    print_separator("2. CREANDO PROFESIONAL DE SALUD")
    prof_payload = {
        "first_name": "Valeria",
        "last_name": "Gómez",
        "specialty": "Medicina General",
        "rut": f"15.432.{rut_sufijo}-K",
        "birth_date": "1988-06-12",
        "sex": "F",
        "email": f"dr.gomez_{rut_sufijo}@salud.cl",
        "phone": "+56987654321",
        "health_center_id": center_id,
    }
    res_prof = requests.post(f"{BASE_URL}/professionals/", json=prof_payload)
    if res_prof.status_code not in (200, 201):
        print("❌ Error al crear profesional:", res_prof.text)
        sys.exit(1)
    prof_data = res_prof.json()
    prof_id = prof_data["id"]
    print(f"✅ Profesional creado:")
    print(f"   ID: {prof_id}")
    print(f"   Dr(a). {prof_data['first_name']} {prof_data['last_name']} - {prof_data['specialty']}")

    # -------------------------------------------------------------
    # 3. Crear Paciente
    # -------------------------------------------------------------
    print_separator("3. CREANDO PACIENTE")
    patient_payload = {
        "first_name": "Carlos",
        "last_name": "Soto",
        "rut": f"19.876.{rut_sufijo}-1",
        "birth_date": "1999-04-15",
        "sex": "M",
        "email": f"carlos.soto_{rut_sufijo}@gmail.com",
        "phone": "+56955443322",
        "current_height": 1.76,
        "current_weight": 82.5,
        "lives_alone": False,
        "bmi": 26.6,
        "context": "Hipertensión leve en control preventivo",
        "psychological_profile": "Receptivo a recomendaciones, moderada adherencia",
    }
    res_patient = requests.post(f"{BASE_URL}/patients", json=patient_payload)
    if res_patient.status_code not in (200, 201):
        print("❌ Error al crear paciente:", res_patient.text)
        sys.exit(1)
    patient_data = res_patient.json()
    patient_id = patient_data["id"]
    print(f"✅ Paciente registrado:")
    print(f"   ID: {patient_id}")
    print(f"   Nombre: {patient_data['first_name']} {patient_data['last_name']}")
    print(f"   Contexto Clínico: {patient_data.get('context')}")

    # -------------------------------------------------------------
    # 4. Crear Conversación
    # -------------------------------------------------------------
    print_separator("4. INICIANDO CONVERSACIÓN CON ASISTENTE")
    convo_payload = {
        "patient_id": patient_id,
        "professional_id": prof_id,
    }
    res_convo = requests.post(f"{BASE_URL}/conversations/", json=convo_payload)
    if res_convo.status_code not in (200, 201):
        print("❌ Error al crear conversación:", res_convo.text)
        sys.exit(1)
    convo_data = res_convo.json()
    convo_id = convo_data["id"]
    print(f"✅ Conversación inicializada con ID: {convo_id}")

    # -------------------------------------------------------------
    # 5. Diálogo con Sarah IA (Endpoint /chat)
    # -------------------------------------------------------------
    print_separator("5. INTERACCIÓN SIMULADA CON SARAH IA (/chat)")
    mensajes_prueba = [
        "Hola Sarah, buenos días.",
        "He tenido mucho dolor de cabeza y algo de mareo desde ayer.",
        "¿Qué me recomiendas respecto a mi peso y dieta para mejorar?",
        "Muchas gracias por la ayuda, Sarah.",
    ]

    for texto in mensajes_prueba:
        print(f"\n👤 [Paciente]: {texto}")
        chat_payload = {
            "sender": "patient",
            "content": texto,
        }
        res_chat = requests.post(f"{BASE_URL}/conversations/{convo_id}/chat", json=chat_payload)
        if res_chat.status_code not in (200, 201):
            print(f"❌ Error en chat ({res_chat.status_code}):", res_chat.text)
            break
        chat_data = res_chat.json()
        print(f"🤖 [Sarah IA]: {chat_data['sarah_message']['content']}")

    # -------------------------------------------------------------
    # 6. Validar Historial de Mensajes Almacenados
    # -------------------------------------------------------------
    print_separator("6. VERIFICANDO PERSISTENCIA EN BD (/messages)")
    res_history = requests.get(f"{BASE_URL}/conversations/{convo_id}/messages")
    if res_history.status_code == 200:
        history = res_history.json()
        print(f"✅ Total de mensajes almacenados en la conversación: {len(history)}")
        for idx, m in enumerate(history, 1):
            tag = "👤 Paciente" if m["sender"] == "patient" else "🤖 Sarah IA"
            print(f"   [{idx}] {tag} ({m['created_at'][:19]}): {m['content'][:60]}...")
    else:
        print("⚠️ No se pudo obtener el historial:", res_history.text)

    print_separator("RESUMEN: FLUJO COMPLETADO AL 100% CON ÉXITO")


if __name__ == "__main__":
    run_pipeline()