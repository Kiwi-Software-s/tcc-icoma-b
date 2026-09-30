"""Prepara uma conta EXISTENTE para apresentação do TCC.

O script adiciona alguns resgates históricos e uma troca de benefício para que
os gráficos, histórico e saldo tenham dados visíveis. Ele não cria usuário de
login: use um e-mail que já exista no Firebase Authentication.

Uso:
    python preparar_demo.py --email seu@email.com

O seed é idempotente: a mesma conta não recebe os dados duas vezes.
"""

import argparse
from datetime import datetime, timedelta, timezone

from firebase_admin import auth, firestore

from app.firebase_config import init_firebase


DEMO_RESGATES = [
    (150, 1.0, "plastico", 150),
    (120, 1.5, "papel", 150),
    (90, 2.0, "vidro", 160),
    (60, 1.0, "metal", 200),
    (30, 2.5, "plastico", 375),
    (5, 3.0, "papel", 300),
]
DEMO_TROCA_PONTOS = 150


def main():
    parser = argparse.ArgumentParser(description="Prepara uma conta EcoPoints para demonstração.")
    parser.add_argument("--email", required=True, help="E-mail de uma conta já criada no Firebase Authentication.")
    args = parser.parse_args()

    init_firebase()
    db = firestore.client()

    try:
        auth_user = auth.get_user_by_email(args.email.strip())
    except auth.UserNotFoundError:
        raise SystemExit("Conta não encontrada no Firebase Authentication. Crie/login nessa conta primeiro.")

    uid = auth_user.uid
    marker_ref = db.collection("demo_seeds").document(uid)
    if marker_ref.get().exists:
        print("Esta conta já foi preparada para demonstração. Nenhum dado foi duplicado.")
        return

    usuario_ref = db.collection("usuarios").document(uid)
    usuario_snap = usuario_ref.get()
    usuario = usuario_snap.to_dict() if usuario_snap.exists else {}
    usuario = usuario or {}
    nome = usuario.get("nome") or auth_user.display_name or args.email.split("@")[0]

    agora = datetime.now(timezone.utc)
    pontos_adicionados = 0
    kg_adicionados = 0.0
    batch = db.batch()

    for indice, (dias_atras, kg, material, pontos) in enumerate(DEMO_RESGATES, start=1):
        data = agora - timedelta(days=dias_atras)
        ref = db.collection("resgates").document(f"demo-{uid[:10]}-r{indice}")
        batch.set(ref, {
            "uid": uid,
            "nome_usuario": nome,
            "codigo": f"DEMO-{indice:03d}",
            "material": material,
            "kg": kg,
            "pontos": pontos,
            "data": data,
            "ponto_coleta": "etec-sylvio",
            "demo": True,
        })
        pontos_adicionados += pontos
        kg_adicionados += kg

    troca_ref = db.collection("trocas").document(f"demo-{uid[:10]}-t1")
    batch.set(troca_ref, {
        "uid": uid,
        "nome_usuario": nome,
        "beneficio_id": "ecobag-sustentavel",
        "nome_beneficio": "EcoBag sustentável",
        "tipo": "desconto",
        "desconto": 30,
        "pontos_gastos": DEMO_TROCA_PONTOS,
        "data": agora - timedelta(days=12),
        "status": "resgatado",
        "protocolo": f"DEMO-{uid[:8].upper()}",
        "demo": True,
    })

    saldo_atual = int(usuario.get("pontos_total", 0) or 0)
    kg_atual = float(usuario.get("kg_total", 0) or 0)
    saldo_liquido = pontos_adicionados - DEMO_TROCA_PONTOS

    batch.set(usuario_ref, {
        "nome": nome,
        "email": usuario.get("email") or args.email.strip(),
        "pontos_total": saldo_atual + saldo_liquido,
        "kg_total": round(kg_atual + kg_adicionados, 3),
    }, merge=True)

    batch.set(marker_ref, {
        "uid": uid,
        "email": args.email.strip(),
        "criado_em": agora,
        "pontos_adicionados": saldo_liquido,
        "kg_adicionados": kg_adicionados,
    })

    batch.commit()

    print("Conta preparada com sucesso.")
    print(f"+{kg_adicionados:g} kg no histórico")
    print(f"+{pontos_adicionados} pontos ganhos")
    print(f"-{DEMO_TROCA_PONTOS} pontos em um benefício")
    print(f"Saldo líquido adicionado: +{saldo_liquido} pontos")


if __name__ == "__main__":
    main()
