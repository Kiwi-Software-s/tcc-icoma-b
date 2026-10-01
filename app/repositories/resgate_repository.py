from collections import defaultdict
from datetime import datetime, timedelta, timezone

from firebase_admin import firestore

from app.firebase_config import init_firebase
from app.repositories.user_repository import obter_usuario
from app.repositories.beneficio_repository import listar_trocas_usuario


BRT = timezone(timedelta(hours=-3))
MESES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


class CodigoInvalidoError(Exception):
    pass


class CodigoJaUsadoError(Exception):
    pass


def _db():
    init_firebase()
    return firestore.client()


def _normalizar_codigo(codigo: str) -> str:
    return (codigo or "").strip().upper()


def resgatar_codigo(uid: str, codigo: str, nome_usuario: str = "", email_usuario: str = "") -> dict:
    """Resgata um código de forma atômica.

    O mesmo código não pode ser usado duas vezes, mesmo que dois pedidos
    cheguem quase ao mesmo tempo.
    """
    codigo = _normalizar_codigo(codigo)
    if not codigo:
        raise CodigoInvalidoError("Digite um código para continuar.")

    db = _db()
    codigo_ref = db.collection("codigos").document(codigo)
    usuario_ref = db.collection("usuarios").document(uid)
    resgate_ref = db.collection("resgates").document()
    transaction = db.transaction()

    @firestore.transactional
    def _executar(transaction):
        codigo_snap = codigo_ref.get(transaction=transaction)
        if not codigo_snap.exists:
            raise CodigoInvalidoError("Código não encontrado.")

        dados_codigo = codigo_snap.to_dict() or {}
        if dados_codigo.get("usado"):
            raise CodigoJaUsadoError("Este código já foi utilizado.")

        try:
            kg = float(dados_codigo.get("kg", 0))
            pontos = int(dados_codigo.get("pontos", 0))
        except (TypeError, ValueError):
            raise CodigoInvalidoError("Código cadastrado com valores inválidos.")

        if kg <= 0 or pontos <= 0:
            raise CodigoInvalidoError("Código cadastrado com valores inválidos.")

        usuario_snap = usuario_ref.get(transaction=transaction)
        dados_usuario = usuario_snap.to_dict() if usuario_snap.exists else {}
        dados_usuario = dados_usuario or {}

        pontos_atuais = int(dados_usuario.get("pontos_total", 0) or 0)
        kg_atuais = float(dados_usuario.get("kg_total", 0) or 0)

        nome = (
            dados_usuario.get("nome")
            or (nome_usuario or "").strip()
            or ((email_usuario or "").split("@")[0] if email_usuario else "Usuário")
        )

        transaction.set(
            usuario_ref,
            {
                "nome": nome,
                "email": dados_usuario.get("email") or email_usuario or "",
                "pontos_total": pontos_atuais + pontos,
                "kg_total": round(kg_atuais + kg, 3),
            },
            merge=True,
        )

        agora = datetime.now(timezone.utc)
        transaction.update(
            codigo_ref,
            {
                "usado": True,
                "usado_por": uid,
                "usado_em": agora,
            },
        )

        material = str(dados_codigo.get("material", "reciclável"))
        transaction.set(
            resgate_ref,
            {
                "uid": uid,
                "nome_usuario": nome,
                "codigo": codigo,
                "material": material,
                "kg": kg,
                "pontos": pontos,
                "data": agora,
                "ponto_coleta": "etec-sylvio",
            },
        )

        return {
            "codigo": codigo,
            "material": material,
            "kg": kg,
            "pontos": pontos,
            "pontos_total": pontos_atuais + pontos,
            "kg_total": round(kg_atuais + kg, 3),
        }

    return _executar(transaction)


def listar_resgates_usuario(uid: str) -> list[dict]:
    db = _db()
    itens = []
    for snap in db.collection("resgates").where("uid", "==", uid).stream():
        dados = snap.to_dict() or {}
        dados["id"] = snap.id
        itens.append(dados)

    itens.sort(key=lambda x: x.get("data") or datetime.min.replace(tzinfo=timezone.utc))
    return itens


<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
def _normalizar_data_local(data):
    if not data:
        return None
    if data.tzinfo is None:
        data = data.replace(tzinfo=timezone.utc)
    return data.astimezone(BRT)


def _somar_meses(ano: int, mes: int, deslocamento: int) -> tuple[int, int]:
    total = ano * 12 + (mes - 1) + deslocamento
    return total // 12, (total % 12) + 1


def _periodos_mensais(agora: datetime) -> list[dict]:
    periodos = []
    for deslocamento in range(-5, 1):
        ano, mes = _somar_meses(agora.year, agora.month, deslocamento)
        prox_ano, prox_mes = _somar_meses(ano, mes, 1)
        inicio = datetime(ano, mes, 1, tzinfo=BRT)
        fim = datetime(prox_ano, prox_mes, 1, tzinfo=BRT)
        periodos.append({"inicio": inicio, "fim": fim, "label": MESES_PT[mes - 1]})
    return periodos


def _periodos_semanais(agora: datetime) -> list[dict]:
    inicio_semana_atual = (agora - timedelta(days=agora.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    periodos = []
    for deslocamento in range(-7, 1):
        inicio = inicio_semana_atual + timedelta(weeks=deslocamento)
        fim = inicio + timedelta(days=7)
        periodos.append({
            "inicio": inicio,
            "fim": fim,
            "label": inicio.strftime("%d/%m"),
        })
    return periodos


def _periodos_diarios(agora: datetime) -> list[dict]:
    hoje = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    periodos = []
    nomes = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    for deslocamento in range(-6, 1):
        inicio = hoje + timedelta(days=deslocamento)
        fim = inicio + timedelta(days=1)
        periodos.append({
            "inicio": inicio,
            "fim": fim,
            "label": f"{nomes[inicio.weekday()]} {inicio.day:02d}",
        })
    return periodos


def _montar_serie_periodo(resgates: list[dict], trocas: list[dict], saldo_atual: int, periodos: list[dict]) -> dict:
    # O ajuste representa qualquer saldo antigo/manual que não possua evento no histórico.
    total_ganho_eventos = sum(int(item.get("pontos", 0) or 0) for item in resgates)
    total_gasto_eventos = sum(int(item.get("pontos_gastos", 0) or 0) for item in trocas)
    ajuste_saldo = saldo_atual - (total_ganho_eventos - total_gasto_eventos)

    inicio_geral = periodos[0]["inicio"]
    saldo = ajuste_saldo
    kg_por_indice = [0.0 for _ in periodos]
    delta_pontos_por_indice = [0 for _ in periodos]

    def localizar_indice(data_local):
        for i, periodo in enumerate(periodos):
            if periodo["inicio"] <= data_local < periodo["fim"]:
                return i
        return None

    for item in resgates:
        data = _normalizar_data_local(item.get("data"))
        if not data:
            continue
        pontos = int(item.get("pontos", 0) or 0)
        kg = float(item.get("kg", 0) or 0)
        if data < inicio_geral:
            saldo += pontos
            continue
        indice = localizar_indice(data)
        if indice is not None:
            kg_por_indice[indice] += kg
            delta_pontos_por_indice[indice] += pontos

    for item in trocas:
        data = _normalizar_data_local(item.get("data"))
        if not data:
            continue
        pontos = int(item.get("pontos_gastos", 0) or 0)
        if data < inicio_geral:
            saldo -= pontos
            continue
        indice = localizar_indice(data)
        if indice is not None:
            delta_pontos_por_indice[indice] -= pontos

    desempenho = []
    evolucao = []
    for i, periodo in enumerate(periodos):
        saldo += delta_pontos_por_indice[i]
        desempenho.append({
            "label": periodo["label"],
            "valor": round(kg_por_indice[i], 2),
        })
        evolucao.append({
            "label": periodo["label"],
            "valor": max(0, saldo),
        })

    return {"desempenho": desempenho, "evolucao": evolucao}
<<<<<<< HEAD
=======
=======
def _seis_meses_referencia(agora_local: datetime) -> list[tuple[int, int]]:
    ano = agora_local.year
    mes = agora_local.month
    resultado = []
    for deslocamento in range(5, -1, -1):
        total = ano * 12 + (mes - 1) - deslocamento
        y = total // 12
        m = (total % 12) + 1
        resultado.append((y, m))
    return resultado
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70


def montar_metricas_dashboard(uid: str) -> dict:
    usuario = obter_usuario(uid)
    resgates = listar_resgates_usuario(uid)
    trocas = listar_trocas_usuario(uid)
    agora = datetime.now(BRT)
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
    saldo_atual = int(usuario.get("pontos_total", 0) or 0)

    graficos = {
        "mensal": _montar_serie_periodo(resgates, trocas, saldo_atual, _periodos_mensais(agora)),
        "semanal": _montar_serie_periodo(resgates, trocas, saldo_atual, _periodos_semanais(agora)),
        "diario": _montar_serie_periodo(resgates, trocas, saldo_atual, _periodos_diarios(agora)),
    }

    # O card continua mostrando o total do mês atual.
    kg_mes = graficos["mensal"]["desempenho"][-1]["valor"]
<<<<<<< HEAD
=======
=======
    meses = _seis_meses_referencia(agora)

    kg_por_mes = defaultdict(float)
    saldo_delta_por_mes = defaultdict(int)
    primeiro_ano, primeiro_mes = meses[0]

    # Calcula o saldo histórico pelos eventos. Um ajuste cobre qualquer saldo
    # antigo/manual que exista no usuário mas não tenha evento correspondente.
    total_ganho_eventos = sum(int(item.get("pontos", 0) or 0) for item in resgates)
    total_gasto_eventos = sum(int(item.get("pontos_gastos", 0) or 0) for item in trocas)
    saldo_atual = int(usuario.get("pontos_total", 0) or 0)
    ajuste_saldo = saldo_atual - (total_ganho_eventos - total_gasto_eventos)
    saldo_antes_periodo = ajuste_saldo

    for item in resgates:
        data = item.get("data")
        if not data:
            continue
        if data.tzinfo is None:
            data = data.replace(tzinfo=timezone.utc)
        local = data.astimezone(BRT)
        chave = (local.year, local.month)
        pontos = int(item.get("pontos", 0) or 0)
        kg = float(item.get("kg", 0) or 0)

        if chave < (primeiro_ano, primeiro_mes):
            saldo_antes_periodo += pontos
        else:
            kg_por_mes[chave] += kg
            saldo_delta_por_mes[chave] += pontos

    for item in trocas:
        data = item.get("data")
        if not data:
            continue
        if data.tzinfo is None:
            data = data.replace(tzinfo=timezone.utc)
        local = data.astimezone(BRT)
        chave = (local.year, local.month)
        pontos = int(item.get("pontos_gastos", 0) or 0)

        if chave < (primeiro_ano, primeiro_mes):
            saldo_antes_periodo -= pontos
        else:
            saldo_delta_por_mes[chave] -= pontos

    desempenho = []
    evolucao = []
    saldo = saldo_antes_periodo
    for ano, mes in meses:
        saldo += saldo_delta_por_mes[(ano, mes)]
        desempenho.append({"label": MESES_PT[mes - 1], "valor": round(kg_por_mes[(ano, mes)], 2)})
        evolucao.append({"label": MESES_PT[mes - 1], "valor": max(0, saldo)})

    kg_mes = round(kg_por_mes[(agora.year, agora.month)], 2)
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70

    return {
        "usuario": usuario,
        "kg_mes": kg_mes,
        "pontos_total": saldo_atual,
        "kg_total": round(float(usuario.get("kg_total", 0) or 0), 2),
<<<<<<< HEAD
        "desempenho": graficos["mensal"]["desempenho"],
        "evolucao": graficos["mensal"]["evolucao"],
        "graficos": graficos,
=======
<<<<<<< HEAD
        "desempenho": graficos["mensal"]["desempenho"],
        "evolucao": graficos["mensal"]["evolucao"],
        "graficos": graficos,
=======
        "desempenho": desempenho,
        "evolucao": evolucao,
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
    }


def ranking_semanal(uid_atual: str, limite: int = 3) -> list[dict]:
    db = _db()
    agora = datetime.now(BRT)
    inicio_semana = (agora - timedelta(days=agora.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

    pontos_por_uid = defaultdict(int)
    nomes = {}

    # Para o volume de um TCC, percorrer os resgates evita exigir índice composto.
    for snap in db.collection("resgates").stream():
        dados = snap.to_dict() or {}
        data = dados.get("data")
        if not data:
            continue
        if data.tzinfo is None:
            data = data.replace(tzinfo=timezone.utc)
        if data.astimezone(BRT) < inicio_semana:
            continue

        uid = dados.get("uid")
        if not uid:
            continue
        pontos_por_uid[uid] += int(dados.get("pontos", 0) or 0)
        if dados.get("nome_usuario"):
            nomes[uid] = str(dados["nome_usuario"])

    ranking = []
    for uid, pontos in pontos_por_uid.items():
        nome = nomes.get(uid)
        if not nome:
            usuario = obter_usuario(uid)
            nome = usuario.get("nome") or usuario.get("email") or "Usuário"
        ranking.append({
            "uid": uid,
            "nome": "Você" if uid == uid_atual else nome,
            "pontos": pontos,
        })

    ranking.sort(key=lambda item: (-item["pontos"], item["nome"].lower()))
    return ranking[:limite]
