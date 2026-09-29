from firebase_admin import firestore

from app.firebase_config import init_firebase


def _db():
    init_firebase()
    return firestore.client()


def garantir_usuario(uid: str, nome: str = "", email: str = "") -> dict:
    """Cria o perfil do usuário no Firestore na primeira autenticação.

    Se o documento já existir, preserva pontos/kg e apenas preenche dados
    básicos que estejam ausentes.
    """
    db = _db()
    ref = db.collection("usuarios").document(uid)
    snap = ref.get()

    nome = (nome or "").strip()
    email = (email or "").strip()

    if not snap.exists:
        dados = {
            "nome": nome or (email.split("@")[0] if email else "Usuário"),
            "email": email,
            "pontos_total": 0,
            "kg_total": 0.0,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        ref.set(dados)
        return dados

    dados = snap.to_dict() or {}
    atualizacoes = {}

    if nome and not dados.get("nome"):
        atualizacoes["nome"] = nome
    if email and not dados.get("email"):
        atualizacoes["email"] = email
    if "pontos_total" not in dados:
        atualizacoes["pontos_total"] = 0
    if "kg_total" not in dados:
        atualizacoes["kg_total"] = 0.0

    if atualizacoes:
        ref.set(atualizacoes, merge=True)
        dados.update(atualizacoes)

    return dados


def obter_usuario(uid: str) -> dict:
    snap = _db().collection("usuarios").document(uid).get()
    if not snap.exists:
        return {}
    return snap.to_dict() or {}
