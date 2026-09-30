
from datetime import datetime, timezone
import secrets, string
from firebase_admin import firestore
from app.firebase_config import init_firebase

def db():
    init_firebase()
    return firestore.client()

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
