from datetime import datetime, timezone
import math
import secrets
import string

from firebase_admin import firestore

from app.firebase_config import init_firebase


PONTOS_KG = {
    "plastico": 150,
    "papel": 100,
    "vidro": 80,
    "metal": 200,
}


def db():
    init_firebase()
    return firestore.client()


def gerar_codigo(material, kg, uid):
    material = (material or "").strip().lower()
    if material not in PONTOS_KG:
        raise ValueError("Selecione um material válido.")

    try:
        kg = float(kg)
    except (TypeError, ValueError):
        raise ValueError("Informe um peso válido.")

    if not math.isfinite(kg) or kg <= 0:
        raise ValueError("O peso deve ser maior que zero.")
    if kg > 1000:
        raise ValueError("O peso informado é muito alto. Confira a pesagem.")

    kg = round(kg, 3)
    pontos = int(round(kg * PONTOS_KG[material]))
    banco = db()
    alfabeto = string.ascii_uppercase + string.digits

    # A colisão é extremamente improvável, mas evitamos sobrescrever um código
    # existente caso ela aconteça.
    for _ in range(10):
        codigo = "ECO-" + "".join(secrets.choice(alfabeto) for _ in range(8))
        ref = banco.collection("codigos").document(codigo)
        if ref.get().exists:
            continue

        ref.set({
            "material": material,
            "kg": kg,
            "pontos": pontos,
            "usado": False,
            "criado_por": uid,
            "criado_em": datetime.now(timezone.utc),
        })
        return {"codigo": codigo, "material": material, "kg": kg, "pontos": pontos}

    raise RuntimeError("Não foi possível gerar um código único. Tente novamente.")
