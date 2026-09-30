
from app.firebase_config import init_firebase
from firebase_admin import firestore

def _db():
    init_firebase()
    return firestore.client()

def listar_usuarios():
    docs = _db().collection("usuarios").stream()
    usuarios=[]
    for d in docs:
        x=d.to_dict() or {}
        x["uid"]=d.id
        usuarios.append(x)
    return usuarios

def alterar_tipo(uid, tipo):
    if tipo not in ["usuario","funcionario","admin"]:
        raise ValueError("Tipo inválido")
    _db().collection("usuarios").document(uid).set({"tipo":tipo}, merge=True)

def listar_codigos():
    docs=_db().collection("codigos").order_by("criado_em", direction=firestore.Query.DESCENDING).stream()
    lista=[]
    for d in docs:
        x=d.to_dict() or {}
        x["codigo"]=d.id
        lista.append(x)
    return lista
