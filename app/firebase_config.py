import os

import firebase_admin
from firebase_admin import credentials


def init_firebase():
    """
    Inicializa o Firebase Admin SDK uma única vez.

    O caminho do arquivo de credenciais (baixado em:
    Console do Firebase > Configurações do projeto > Contas de serviço >
    Gerar nova chave privada) é lido da variável de ambiente
    FIREBASE_CREDENTIALS. Se não existir, usa "serviceAccountKey.json"
    na raiz do projeto (não versionar esse arquivo — adicione ao .gitignore).
    """
    if firebase_admin._apps:
        return

    cred_path = os.environ.get("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
