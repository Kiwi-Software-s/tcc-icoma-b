import os
import json
import firebase_admin
from firebase_admin import credentials


def init_firebase():
    """
    Inicializa o Firebase Admin SDK.

    No Render:
    usa FIREBASE_CREDENTIALS.

    Localmente:
    usa serviceAccountKey.json.
    """

    if firebase_admin._apps:
        return

    firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")

    if firebase_credentials:
        # Render: JSON armazenado na variável de ambiente
        try:
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)

        except json.JSONDecodeError as e:
            raise RuntimeError(
                "FIREBASE_CREDENTIALS não contém um JSON válido."
            ) from e

    else:
        # Local: arquivo serviceAccountKey.json
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        cred_path = os.path.join(
            base_dir,
            "serviceAccountKey.json"
        )

        if not os.path.exists(cred_path):
            raise RuntimeError(
                "serviceAccountKey.json não encontrado."
            )

        cred = credentials.Certificate(cred_path)

    firebase_admin.initialize_app(cred)