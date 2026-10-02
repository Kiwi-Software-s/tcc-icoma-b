from firebase_admin import firestore

from app.firebase_config import init_firebase


def _db():
    init_firebase()
    return firestore.client()


def listar_usuarios():
    docs = _db().collection("usuarios").stream()
    usuarios = []
    for doc in docs:
        dados = doc.to_dict() or {}
        dados["uid"] = doc.id
        dados.setdefault("tipo", "usuario")
        dados.setdefault("origem", False)
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
    snap = ref.get()
    if not snap.exists:
        raise ValueError("Usuário não encontrado.")

    dados = snap.to_dict() or {}
    if dados.get("origem") is True:
        raise ValueError("Esta é uma conta de origem e seu cargo não pode ser alterado.")

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
