<<<<<<< HEAD
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


=======

from datetime import datetime, timezone
import secrets, string
from firebase_admin import firestore
from app.firebase_config import init_firebase

>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
def db():
    init_firebase()
    return firestore.client()

<<<<<<< HEAD

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
=======
PONTOS_KG = {"plastico":150,"papel":100,"vidro":80,"metal":200}

def gerar_codigo(material, kg, uid):
    material = material.lower()
    kg=float(kg)
    if material not in PONTOS_KG or kg<=0:
        raise ValueError("Dados inválidos")
    codigo="ECO-"+''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(8))
    pontos=int(kg*PONTOS_KG[material])
    db().collection("codigos").document(codigo).set({
        "material":material,
        "kg":kg,
        "pontos":pontos,
        "usado":False,
        "criado_por":uid,
        "criado_em":datetime.now(timezone.utc)
    })
    return {"codigo":codigo,"kg":kg,"pontos":pontos}
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
