from datetime import datetime, timedelta, timezone

from app.repositories.beneficio_repository import (
    BeneficioInvalidoError,
    SaldoInsuficienteError,
<<<<<<< HEAD
    definir_favorito,
    listar_beneficios,
    listar_favoritos_usuario,
=======
    listar_beneficios,
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
    listar_trocas_usuario,
    trocar_beneficio,
)
from app.repositories.resgate_repository import listar_resgates_usuario


BRT = timezone(timedelta(hours=-3))


def _data_local(data):
    if not data:
        return None
    if data.tzinfo is None:
        data = data.replace(tzinfo=timezone.utc)
    return data.astimezone(BRT)


def montar_historico_usuario(uid: str) -> dict:
    resgates = listar_resgates_usuario(uid)
    trocas = listar_trocas_usuario(uid)

    pontos_ganhos = sum(int(item.get("pontos", 0) or 0) for item in resgates)
    pontos_gastos = sum(int(item.get("pontos_gastos", 0) or 0) for item in trocas)
    kg_total = round(sum(float(item.get("kg", 0) or 0) for item in resgates), 2)
    produtos_resgatados = sum(1 for item in trocas if item.get("tipo") == "produto")
    descontos_resgatados = sum(1 for item in trocas if item.get("tipo") == "desconto")
    locais = {item.get("ponto_coleta") for item in resgates if item.get("ponto_coleta")}

    eventos = []

    for item in resgates:
        data = _data_local(item.get("data"))
        material = str(item.get("material") or "reciclável").capitalize()
        kg = float(item.get("kg", 0) or 0)
        pontos = int(item.get("pontos", 0) or 0)
        eventos.append(
            {
                "data": data,
                "data_label": data.strftime("%d/%m/%Y • %H:%M") if data else "Data indisponível",
                "data_type": "ganhos reciclagens descartes",
                "css": "",
                "icone": "bi-recycle",
                "titulo": "Reciclagem registrada",
                "meta_linha1": f"{kg:g} kg de {material}",
                "meta_linha2": "Etec Sylvio de Mattos Carvalho",
                "delta": pontos,
                "delta_sinal": "+",
                "delta_minus": False,
            }
        )

    for item in trocas:
        data = _data_local(item.get("data"))
        tipo = item.get("tipo") or "desconto"
        nome = str(item.get("nome_beneficio") or "Benefício")
        desconto = int(item.get("desconto", 0) or 0)
        pontos = int(item.get("pontos_gastos", 0) or 0)
        protocolo = str(item.get("protocolo") or "")

        if tipo == "produto":
            titulo = "Produto resgatado"
            meta1 = nome
            css = "purple"
            icone = "bi-gift-fill"
        else:
            titulo = "Desconto resgatado"
            meta1 = f"{desconto}% OFF em {nome}" if desconto else nome
            css = "orange"
            icone = "bi-percent"

        eventos.append(
            {
                "data": data,
                "data_label": data.strftime("%d/%m/%Y • %H:%M") if data else "Data indisponível",
                "data_type": "gastos resgates",
                "css": css,
                "icone": icone,
                "titulo": titulo,
                "meta_linha1": meta1,
                "meta_linha2": f"Protocolo {protocolo}" if protocolo else "EcoPoints",
                "delta": pontos,
                "delta_sinal": "-",
                "delta_minus": True,
            }
        )

    minimo = datetime.min.replace(tzinfo=BRT)
    eventos.sort(key=lambda item: item.get("data") or minimo, reverse=True)

    return {
        "pontos_ganhos": pontos_ganhos,
        "pontos_gastos": pontos_gastos,
        "kg_total": kg_total,
        "produtos_resgatados": produtos_resgatados,
        "descontos_resgatados": descontos_resgatados,
        "pontos_descarte": len(locais),
        "eventos": eventos,
<<<<<<< HEAD
        "quantidade_eventos": len(eventos),
        "quantidade_resgates": len(resgates),
        "quantidade_trocas": len(trocas),
=======
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
    }


__all__ = [
    "BeneficioInvalidoError",
    "SaldoInsuficienteError",
<<<<<<< HEAD
    "definir_favorito",
    "listar_beneficios",
    "listar_favoritos_usuario",
=======
    "listar_beneficios",
>>>>>>> 40045d14bc5afcf18652c9804bdce5877a5f3ee6
    "listar_trocas_usuario",
    "montar_historico_usuario",
    "trocar_beneficio",
]
