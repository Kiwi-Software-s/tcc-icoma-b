<<<<<<< HEAD
from firebase_admin import firestore

from app.firebase_config import init_firebase

=======

from app.firebase_config import init_firebase
from firebase_admin import firestore
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70

def _db():
    init_firebase()
    return firestore.client()

<<<<<<< HEAD

def listar_usuarios():
    docs = _db().collection("usuarios").stream()
    usuarios = []
    for doc in docs:
        dados = doc.to_dict() or {}
        dados["uid"] = doc.id
        dados.setdefault("tipo", "usuario")
        usuarios.append(dados)

    usuarios.sort(key=lambda u: ((u.get("nome") or "").lower(), (u.get("email") or "").lower()))
    return usuarios


def alterar_tipo(uid, tipo):
    uid = (uid or "").strip()
    tipo = (tipo or "").strip().lower()
    if not uid:
        raise ValueError("Usuário inválido.")
    if tipo not in {"usuario", "funcionario", "admin"}:
        raise ValueError("Tipo de usuário inválido.")

    ref = _db().collection("usuarios").document(uid)
    if not ref.get().exists:
        raise ValueError("Usuário não encontrado.")
    ref.set({"tipo": tipo}, merge=True)


def listar_codigos(limite=100):
    colecao = _db().collection("codigos")
    try:
        docs = (
            colecao
            .order_by("criado_em", direction=firestore.Query.DESCENDING)
            .limit(limite)
            .stream()
        )
        lista = []
        for doc in docs:
            dados = doc.to_dict() or {}
            dados["codigo"] = doc.id
            lista.append(dados)
        return lista
    except Exception:
        # Códigos antigos/semeados podem não ter o campo criado_em.
        docs = colecao.limit(limite).stream()
        lista = []
        for doc in docs:
            dados = doc.to_dict() or {}
            dados["codigo"] = doc.id
            lista.append(dados)
        return lista
=======
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
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
