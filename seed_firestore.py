"""Cadastra códigos fixos de demonstração no Firestore.

Pré-requisito: o Firestore precisa ter sido criado uma vez no Firebase Console
e o arquivo serviceAccountKey.json deve estar na raiz do projeto.

Uso:
    python seed_firestore.py
"""

from firebase_admin import firestore

from app.firebase_config import init_firebase


CODIGOS = {
    "ECO-PAPEL-001": {"material": "papel", "kg": 1.5, "pontos": 150},
    "ECO-PAPEL-002": {"material": "papel", "kg": 2.0, "pontos": 200},
    "ECO-PAPEL-003": {"material": "papel", "kg": 3.0, "pontos": 300},
    "ECO-PLASTICO-001": {"material": "plastico", "kg": 1.0, "pontos": 150},
    "ECO-PLASTICO-002": {"material": "plastico", "kg": 2.0, "pontos": 300},
    "ECO-PLASTICO-003": {"material": "plastico", "kg": 3.0, "pontos": 450},
    "ECO-VIDRO-001": {"material": "vidro", "kg": 1.0, "pontos": 80},
    "ECO-VIDRO-002": {"material": "vidro", "kg": 2.5, "pontos": 200},
    "ECO-VIDRO-003": {"material": "vidro", "kg": 4.0, "pontos": 320},
    "ECO-METAL-001": {"material": "metal", "kg": 1.0, "pontos": 200},
    "ECO-METAL-002": {"material": "metal", "kg": 2.0, "pontos": 400},
    "ECO-METAL-003": {"material": "metal", "kg": 3.0, "pontos": 600},
}


def main():
    init_firebase()
    db = firestore.client()

    for codigo, dados in CODIGOS.items():
        ref = db.collection("codigos").document(codigo)
        snap = ref.get()

        # Não reativa código que já foi usado.
        if snap.exists and (snap.to_dict() or {}).get("usado"):
            print(f"[mantido] {codigo} já foi usado")
            continue

        ref.set({**dados, "usado": False}, merge=True)
        print(f"[ok] {codigo}: {dados['kg']} kg / {dados['pontos']} pontos")

    print("\nCódigos fixos cadastrados no Firestore.")


if __name__ == "__main__":
    main()
