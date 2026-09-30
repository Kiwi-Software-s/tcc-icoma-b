"""Smoke test local, sem escrever no Firestore.

Rode com a venv ativa:
    python verificar_projeto.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def ok(mensagem):
    print(f"[OK] {mensagem}")


def fail(mensagem):
    print(f"[ERRO] {mensagem}")
    return False


def main():
    tudo_ok = True

    obrigatorios = [
        "main.py",
        "templates/dashboard/dashboard.html",
        "templates/ecopoints/descontos.html",
        "templates/ecopoints/historico.html",
        "templates/ecopoints/perfil.html",
        "app/repositories/resgate_repository.py",
        "app/repositories/beneficio_repository.py",
    ]
    for nome in obrigatorios:
        if (ROOT / nome).exists():
            ok(f"Arquivo presente: {nome}")
        else:
            tudo_ok = fail(f"Arquivo ausente: {nome}") and tudo_ok

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8", errors="ignore")
    if "serviceAccountKey.json" in gitignore:
        ok("serviceAccountKey.json está protegido pelo .gitignore")
    else:
        tudo_ok = fail("Adicione serviceAccountKey.json ao .gitignore") and tudo_ok

    if (ROOT / "serviceAccountKey.json").exists() or os.environ.get("FIREBASE_CREDENTIALS"):
        ok("Credencial Firebase encontrada para execução")
    else:
        print("[AVISO] Firebase não configurado neste ambiente; páginas públicas ainda podem abrir.")

    try:
        from main import app
        client = app.test_client()
        resp = client.get("/health")
        if resp.status_code == 200 and resp.get_json().get("status") == "ok":
            ok("/health respondeu corretamente")
        else:
            tudo_ok = fail("/health falhou") and tudo_ok

        resp404 = client.get("/pagina-que-nao-existe")
        if resp404.status_code == 404:
            ok("Página 404 personalizada funcionando")
        else:
            tudo_ok = fail("Tratamento 404 falhou") and tudo_ok

        rotas = {rule.rule for rule in app.url_map.iter_rules()}
        for rota in ["/dashboard", "/perfil", "/meus-descontos", "/historico", "/resgatar-codigos", "/mapa-de-pontos"]:
            if rota in rotas:
                ok(f"Rota registrada: {rota}")
            else:
                tudo_ok = fail(f"Rota ausente: {rota}") and tudo_ok
    except Exception as exc:
        tudo_ok = fail(f"Falha ao carregar Flask: {exc}") and tudo_ok

    print("\nResultado:", "PROJETO PRONTO PARA TESTE MANUAL" if tudo_ok else "CORRIJA OS ERROS ACIMA")
    raise SystemExit(0 if tudo_ok else 1)


if __name__ == "__main__":
    main()
