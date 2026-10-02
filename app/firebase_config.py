import json
import os

import firebase_admin
from firebase_admin import credentials


# Deve ser o mesmo projectId usado nas telas de login e cadastro.
FIREBASE_PROJECT_ID = "tcc-ecopoint"


def _validar_projeto(project_id):
    if project_id != FIREBASE_PROJECT_ID:
        raise RuntimeError(
            "As credenciais do servidor precisam pertencer ao projeto "
            f"{FIREBASE_PROJECT_ID}. Confira o project_id de FIREBASE_CREDENTIALS "
            "ou de serviceAccountKey.json."
        )


def init_firebase():
    """Inicializa o Admin SDK com as credenciais do mesmo projeto do site."""
    try:
        firebase_app = firebase_admin.get_app()
    except ValueError:
        firebase_app = None

    if firebase_app is not None:
        _validar_projeto(firebase_app.project_id)
        return firebase_app

    firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")

    if firebase_credentials:
        try:
            cred_dict = json.loads(firebase_credentials)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "FIREBASE_CREDENTIALS não contém um JSON válido. "
                "Use o conteúdo completo do arquivo da conta de serviço."
            ) from exc

        if not isinstance(cred_dict, dict):
            raise RuntimeError("FIREBASE_CREDENTIALS deve conter um objeto JSON.")

        _validar_projeto(cred_dict.get("project_id"))
        try:
            cred = credentials.Certificate(cred_dict)
        except (ValueError, TypeError, KeyError) as exc:
            raise RuntimeError(
                "FIREBASE_CREDENTIALS não contém uma conta de serviço válida. "
                "Confira o JSON completo, incluindo a chave privada."
            ) from exc
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cred_path = os.path.join(base_dir, "serviceAccountKey.json")

        if not os.path.exists(cred_path):
            raise RuntimeError(
                "serviceAccountKey.json não encontrado. No Render, configure "
                "FIREBASE_CREDENTIALS com o JSON completo da conta de serviço."
            )

        try:
            cred = credentials.Certificate(cred_path)
        except (ValueError, TypeError, KeyError) as exc:
            raise RuntimeError("serviceAccountKey.json não contém credenciais válidas.") from exc

        _validar_projeto(cred.project_id)

    return firebase_admin.initialize_app(cred)
