"""Gera novos lotes de códigos de reciclagem sem reutilizar códigos antigos.

O script procura o maior número já usado em cada material e continua a sequência.
Ele NÃO apaga, reativa ou sobrescreve códigos resgatados.

Uso rápido:
    python gerar_codigos.py

Isso cria 10 códigos por material (40 códigos ao todo).

Outros exemplos:
    python gerar_codigos.py --quantidade 25
    python gerar_codigos.py --quantidade 10 --material plastico
"""

import argparse
import re
from datetime import datetime, timezone

from firebase_admin import firestore

from app.firebase_config import init_firebase


MATERIAIS = {
    "papel": {
        "prefixo": "PAPEL",
        "pontos_por_kg": 100,
        "kg_ciclo": [1.0, 1.5, 2.0, 2.5, 3.0],
    },
    "plastico": {
        "prefixo": "PLASTICO",
        "pontos_por_kg": 150,
        "kg_ciclo": [1.0, 1.5, 2.0, 2.5, 3.0],
    },
    "vidro": {
        "prefixo": "VIDRO",
        "pontos_por_kg": 80,
        "kg_ciclo": [1.0, 1.5, 2.0, 2.5, 3.0],
    },
    "metal": {
        "prefixo": "METAL",
        "pontos_por_kg": 200,
        "kg_ciclo": [1.0, 1.5, 2.0, 2.5, 3.0],
    },
}


def _maior_numero_existente(db, prefixo: str) -> int:
    padrao = re.compile(rf"^ECO-{re.escape(prefixo)}-(\d+)$")
    maior = 0

    for snap in db.collection("codigos").stream():
        match = padrao.match(snap.id)
        if match:
            maior = max(maior, int(match.group(1)))

    return maior


def gerar_lote(quantidade: int, material: str | None = None) -> list[dict]:
    if quantidade < 1:
        raise ValueError("A quantidade precisa ser maior que zero.")

    init_firebase()
    db = firestore.client()
    agora = datetime.now(timezone.utc)

    nomes_materiais = [material] if material else list(MATERIAIS.keys())
    criados = []

    for nome_material in nomes_materiais:
        config = MATERIAIS[nome_material]
        prefixo = config["prefixo"]
        proximo = _maior_numero_existente(db, prefixo) + 1

        batch = db.batch()
        pendentes = []

        for deslocamento in range(quantidade):
            numero = proximo + deslocamento
            codigo = f"ECO-{prefixo}-{numero:03d}"
            kg = config["kg_ciclo"][(numero - 1) % len(config["kg_ciclo"])]
            pontos = int(round(kg * config["pontos_por_kg"]))

            dados = {
                "material": nome_material,
                "kg": kg,
                "pontos": pontos,
                "usado": False,
                "criado_em": agora,
                "origem": "lote-manual",
            }

            ref = db.collection("codigos").document(codigo)
            batch.set(ref, dados)
            pendentes.append({"codigo": codigo, **dados})

        batch.commit()
        criados.extend(pendentes)

    return criados


def main():
    parser = argparse.ArgumentParser(description="Gera novos códigos EcoPoints no Firestore.")
    parser.add_argument(
        "--quantidade",
        type=int,
        default=10,
        help="Quantidade por material. Padrão: 10.",
    )
    parser.add_argument(
        "--material",
        choices=list(MATERIAIS.keys()),
        help="Gera apenas para um material. Se omitido, gera para todos.",
    )
    args = parser.parse_args()

    try:
        criados = gerar_lote(args.quantidade, args.material)
    except ValueError as exc:
        raise SystemExit(str(exc))

    print(f"\n{len(criados)} código(s) criado(s) com sucesso:\n")
    for item in criados:
        print(f"[ok] {item['codigo']}: {item['kg']:g} kg / {item['pontos']} pontos")

    print("\nNenhum código antigo foi apagado ou reativado.")


if __name__ == "__main__":
    main()
