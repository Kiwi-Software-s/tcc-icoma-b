from datetime import datetime, timezone

from firebase_admin import firestore

from app.firebase_config import init_firebase


class BeneficioInvalidoError(Exception):
    pass


class SaldoInsuficienteError(Exception):
    pass


<<<<<<< HEAD
# Catálogo fixo por enquanto. O backend usa estes valores como fonte de
# verdade, então o navegador não consegue alterar o preço pelo DevTools.
=======
# Catálogo fixo por enquanto, como o restante dos benefícios do protótipo.
# O backend usa estes valores como fonte de verdade, então o navegador não
# consegue alterar o preço de um resgate pelo DevTools.
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
BENEFICIOS = {
    "ecobag-sustentavel": {
        "id": "ecobag-sustentavel",
        "nome": "EcoBag sustentável",
        "preco_pontos": 150,
        "desconto": 30,
        "tipo": "desconto",
<<<<<<< HEAD
        "categoria": "Acessórios",
        "loja": "EcoViva",
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
        "imagem": "dashboard/premios/ecobag.png",
        "icone": None,
    },
    "garrafa-reutilizavel": {
        "id": "garrafa-reutilizavel",
        "nome": "Garrafa reutilizável",
        "preco_pontos": 150,
        "desconto": 20,
        "tipo": "desconto",
<<<<<<< HEAD
        "categoria": "Casa & dia a dia",
        "loja": "Verde Mais",
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
        "imagem": "dashboard/premios/garrafa.png",
        "icone": None,
    },
    "vaso-ecologico": {
        "id": "vaso-ecologico",
        "nome": "Vaso ecológico",
        "preco_pontos": 150,
        "desconto": 15,
        "tipo": "desconto",
<<<<<<< HEAD
        "categoria": "Casa & jardim",
        "loja": "Raiz Verde",
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
        "imagem": "dashboard/premios/vaso.png",
        "icone": None,
    },
    "kit-produtos-naturais": {
        "id": "kit-produtos-naturais",
        "nome": "Kit produtos naturais",
        "preco_pontos": 150,
        "desconto": 10,
        "tipo": "desconto",
<<<<<<< HEAD
        "categoria": "Bem-estar",
        "loja": "Naturalmente",
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
        "imagem": None,
        "icone": "bi-bag-heart",
    },
}


def _db():
    init_firebase()
    return firestore.client()


def listar_beneficios() -> list[dict]:
    return [dict(item) for item in BENEFICIOS.values()]


def obter_beneficio(beneficio_id: str) -> dict | None:
    beneficio_id = (beneficio_id or "").strip().lower()
    item = BENEFICIOS.get(beneficio_id)
    return dict(item) if item else None


<<<<<<< HEAD
def listar_favoritos_usuario(uid: str) -> list[str]:
    snap = _db().collection("usuarios").document(uid).get()
    if not snap.exists:
        return []
    dados = snap.to_dict() or {}
    favoritos = dados.get("favoritos") or []
    return [str(item) for item in favoritos if str(item) in BENEFICIOS]


def definir_favorito(uid: str, beneficio_id: str, favorito: bool) -> list[str]:
    beneficio = obter_beneficio(beneficio_id)
    if not beneficio:
        raise BeneficioInvalidoError("Benefício não encontrado.")

    db = _db()
    ref = db.collection("usuarios").document(uid)
    transaction = db.transaction()

    @firestore.transactional
    def _executar(transaction):
        snap = ref.get(transaction=transaction)
        dados = snap.to_dict() if snap.exists else {}
        dados = dados or {}
        favoritos = {str(item) for item in (dados.get("favoritos") or []) if str(item) in BENEFICIOS}

        if favorito:
            favoritos.add(beneficio["id"])
        else:
            favoritos.discard(beneficio["id"])

        ordenados = sorted(favoritos)
        transaction.set(ref, {"favoritos": ordenados}, merge=True)
        return ordenados

    return _executar(transaction)


=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
def trocar_beneficio(
    uid: str,
    beneficio_id: str,
    nome_usuario: str = "",
    email_usuario: str = "",
) -> dict:
    beneficio = obter_beneficio(beneficio_id)
    if not beneficio:
        raise BeneficioInvalidoError("Benefício não encontrado.")

    db = _db()
    usuario_ref = db.collection("usuarios").document(uid)
    troca_ref = db.collection("trocas").document()
    transaction = db.transaction()

    @firestore.transactional
    def _executar(transaction):
        usuario_snap = usuario_ref.get(transaction=transaction)
        dados_usuario = usuario_snap.to_dict() if usuario_snap.exists else {}
        dados_usuario = dados_usuario or {}

        pontos_atuais = int(dados_usuario.get("pontos_total", 0) or 0)
        custo = int(beneficio["preco_pontos"])

        if pontos_atuais < custo:
            faltam = custo - pontos_atuais
            raise SaldoInsuficienteError(
                f"Você precisa de mais {faltam} EcoPoints para este resgate."
            )

        nome = (
            dados_usuario.get("nome")
            or (nome_usuario or "").strip()
            or ((email_usuario or "").split("@")[0] if email_usuario else "Usuário")
        )
        saldo_apos = pontos_atuais - custo
        agora = datetime.now(timezone.utc)
        protocolo = f"ECO-{troca_ref.id[:8].upper()}"

        transaction.set(
            usuario_ref,
            {
                "nome": nome,
                "email": dados_usuario.get("email") or email_usuario or "",
                "pontos_total": saldo_apos,
            },
            merge=True,
        )

        transaction.set(
            troca_ref,
            {
                "uid": uid,
                "nome_usuario": nome,
                "beneficio_id": beneficio["id"],
                "nome_beneficio": beneficio["nome"],
                "tipo": beneficio["tipo"],
                "desconto": int(beneficio.get("desconto", 0) or 0),
                "pontos_gastos": custo,
                "data": agora,
                "status": "resgatado",
                "protocolo": protocolo,
            },
        )

        return {
            "beneficio_id": beneficio["id"],
            "nome": beneficio["nome"],
            "tipo": beneficio["tipo"],
            "desconto": int(beneficio.get("desconto", 0) or 0),
            "pontos_gastos": custo,
            "pontos_total": saldo_apos,
            "protocolo": protocolo,
        }

    return _executar(transaction)


def listar_trocas_usuario(uid: str) -> list[dict]:
    db = _db()
    itens = []
    for snap in db.collection("trocas").where("uid", "==", uid).stream():
        dados = snap.to_dict() or {}
        dados["id"] = snap.id
        itens.append(dados)

    minimo = datetime.min.replace(tzinfo=timezone.utc)
    itens.sort(key=lambda x: x.get("data") or minimo)
    return itens
