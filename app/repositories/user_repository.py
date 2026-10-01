from firebase_admin import firestore

from app.firebase_config import init_firebase


def _db():
    init_firebase()
    return firestore.client()


def garantir_usuario(uid: str, nome: str = "", email: str = "") -> dict:
    """Cria o perfil do usuário no Firestore na primeira autenticação.

    Se o documento já existir, preserva pontos/kg/favoritos e apenas preenche
    dados básicos que estejam ausentes.
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
            "favoritos": [],
            "tipo": "usuario",
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
    if "favoritos" not in dados:
        atualizacoes["favoritos"] = []
    if "tipo" not in dados:
        atualizacoes["tipo"] = "usuario"

    if atualizacoes:
        ref.set(atualizacoes, merge=True)
        dados.update(atualizacoes)

    return dados


def obter_usuario(uid: str) -> dict:
    snap = _db().collection("usuarios").document(uid).get()
    if not snap.exists:
        return {}
    return snap.to_dict() or {}


def atualizar_nome_usuario(uid: str, nome: str) -> str:
    nome = " ".join((nome or "").strip().split())
    if len(nome) < 2:
        raise ValueError("Digite um nome com pelo menos 2 caracteres.")
    if len(nome) > 60:
        raise ValueError("O nome pode ter no máximo 60 caracteres.")
    if any(ord(ch) < 32 for ch in nome):
        raise ValueError("O nome contém caracteres inválidos.")

    _db().collection("usuarios").document(uid).set(
        {"nome": nome, "updated_at": firestore.SERVER_TIMESTAMP},
        merge=True,
    )
    return nome


def obter_tipo_usuario(uid: str) -> str:
    """Retorna o nível de acesso do usuário."""
    dados = obter_usuario(uid)

    if not dados:
        return "usuario"

    return dados.get("tipo", "usuario")
