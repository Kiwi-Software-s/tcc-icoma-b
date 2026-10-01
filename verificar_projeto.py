<<<<<<< HEAD
"""Verificação rápida do EcoPoints sem escrever no Firestore.
=======
"""Smoke test local, sem escrever no Firestore.
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70

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
<<<<<<< HEAD
        "templates/ecopoints/funcionario.html",
        "templates/ecopoints/admin.html",
        "templates/ecopoints/mobile_nav.html",
        "templates/mapa/mapa.html",
        "static/mobile-nav.css",
        "static/mobile-nav.js",
        "app/repositories/resgate_repository.py",
        "app/repositories/beneficio_repository.py",
        "app/repositories/funcionario_repository.py",
        "app/repositories/admin_repository.py",
=======
        "app/repositories/resgate_repository.py",
        "app/repositories/beneficio_repository.py",
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
    ]
    for nome in obrigatorios:
        if (ROOT / nome).exists():
            ok(f"Arquivo presente: {nome}")
        else:
            tudo_ok = fail(f"Arquivo ausente: {nome}") and tudo_ok

<<<<<<< HEAD
    # Evita repetir o problema de marcadores de conflito Git dentro do Python/HTML.
    conflitos = []
    ignorar = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    for arquivo in ROOT.rglob("*"):
        if not arquivo.is_file() or any(parte in ignorar for parte in arquivo.parts):
            continue
        if arquivo.suffix.lower() not in {".py", ".html", ".css", ".js", ".md"}:
            continue
        try:
            texto = arquivo.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(marcador in texto for marcador in ("<<<<<<< ", "=======\n", ">>>>>>> ")):
            conflitos.append(str(arquivo.relative_to(ROOT)))
    if conflitos:
        tudo_ok = fail("Conflitos Git encontrados: " + ", ".join(conflitos)) and tudo_ok
    else:
        ok("Nenhum marcador de conflito Git encontrado")

=======
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8", errors="ignore")
    if "serviceAccountKey.json" in gitignore:
        ok("serviceAccountKey.json está protegido pelo .gitignore")
    else:
        tudo_ok = fail("Adicione serviceAccountKey.json ao .gitignore") and tudo_ok

    if (ROOT / "serviceAccountKey.json").exists() or os.environ.get("FIREBASE_CREDENTIALS"):
        ok("Credencial Firebase encontrada para execução")
    else:
<<<<<<< HEAD
        print("[AVISO] Firebase não configurado neste ambiente; login e Firestore não poderão ser testados.")
=======
        print("[AVISO] Firebase não configurado neste ambiente; páginas públicas ainda podem abrir.")
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70

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
<<<<<<< HEAD
        esperadas = [
            "/dashboard", "/perfil", "/meus-descontos", "/historico",
            "/resgatar-codigos", "/mapa-de-pontos", "/funcionario", "/admin",
            "/funcionario/gerar", "/admin/tipo",
        ]
        for rota in esperadas:
=======
        for rota in ["/dashboard", "/perfil", "/meus-descontos", "/historico", "/resgatar-codigos", "/mapa-de-pontos"]:
>>>>>>> 00cb19d9a33f9dbe87dcea517577a29742de9f70
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
