# Deploy do EcoPoints (Render)

O projeto já está preparado para rodar com `gunicorn main:app`.

## Antes de publicar

1. Confirme que `serviceAccountKey.json` **não** foi enviado ao GitHub.
2. No Render, crie um Web Service a partir do repositório ou use o `render.yaml`.
3. Configure a variável `FIREBASE_CREDENTIALS` com o conteúdo JSON completo da service account.
4. `FLASK_SECRET_KEY` é gerada automaticamente pelo `render.yaml`. Se criar o serviço manualmente, gere uma chave longa e aleatória.
5. O app usa `PORT` automaticamente e `debug` fica desligado em produção.

## Comandos

Build:

```bash
pip install -r requirements.txt
```

Start:

```bash
gunicorn main:app
```

Health check:

```text
/health
```

## Firebase

O Firestore pode permanecer em modo de produção. O backend usa Firebase Admin e não depende de liberar leitura/escrita pública no Firestore.
