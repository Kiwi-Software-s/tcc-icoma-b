Adicionar o SDK Admin do Firebase ao servidor
O Admin SDK é um conjunto de bibliotecas de servidor que permite interagir com o Firebase usando ambientes privilegiados para executar ações.
Pré-requisitos
•	Verifique se você tem um app de servidor.
•	Verifique se o servidor executa os parâmetros a seguir, dependendo do Admin SDK usado:
•	SDK Admin para Node.js: Node.js 18 ou superior (recomendamos o Node.js 20 ou superior)
•	SDK Admin para Java 8 ou mais recente
•	SDK Admin para Python 3.9 ou mais recente (recomendamos o Python 3.10 ou mais recente)
O suporte ao Python 3.9 foi descontinuado.
•	SDK Admin para Go 1.23 ou mais recente
•	SDK Admin para .NET: .NET Framework 4.6.2 ou mais recente, .NET Standard 2.0 ou .NET 6.0 ou mais recente (recomendamos .NET 8.0 ou mais recente)
O suporte para .NET 6.0 e 7.0 foi descontinuado.
Configurar um projeto e uma conta de serviço do Firebase
•	um projeto do Firebase;
•	conta de serviço do SDK Admin do Firebase para se comunicar com o Firebase.
•	um arquivo de configuração com as credenciais da sua conta de serviço.
Adicionar o SDK
O SDK Admin para Python do Firebase está disponível via PIP.
sudo pip install firebase-admin
Ou, para instalar a biblioteca apenas para o usuário atual, passe a flag --user:
pip install --user firebase-admin
Inicializar o SDK
default_app = firebase_admin.initialize_app()
Como usar um token de atualização do OAuth 2.0
cred = credentials.RefreshToken('path/to/refreshToken.json')
default_app = firebase_admin.initialize_app(cred)
Inicializar o SDK em ambientes que não são do Google
Para gerar um arquivo de chave privada da conta de serviço, siga estas etapas:
1.	No console Firebase, abra Configurações > Contas de serviço.
2.	Clique em Gerar nova chave privada e selecione Gerar chave para confirmar.
3.	Armazene com segurança o arquivo JSON que contém a chave.
Para definir a variável de ambiente:
Com o PowerShell:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\service-account-file.json"
Inicialize o SDK como mostrado:
default_app = firebase_admin.initialize_app()
Inicializar vários aplicativos
# Import the Firebase service
from firebase_admin import auth

# Initialize the default app
default_app = firebase_admin.initialize_app(cred)
print(default_app.name)  # "[DEFAULT]"

# Retrieve services via the auth package...
# auth.create_custom_token(...)
Alguns casos de uso exigem que você crie vários aplicativos ao mesmo tempo. Por exemplo, talvez você queira ler dados do Realtime Database de um projeto do Firebase e criar tokens personalizados para outro projeto. Com o SDK do Firebase, você cria vários apps ao mesmo tempo.
# Initialize the default app
default_app = firebase_admin.initialize_app(cred)

#  Initialize another app with a different config
other_app = firebase_admin.initialize_app(cred, name='other')

print(default_app.name)    # "[DEFAULT]"
print(other_app.name)      # "other"

# Retrieve default services via the auth package...
# auth.create_custom_token(...)

# Use the `app` argument to retrieve the other app's services
# auth.create_custom_token(..., app=other_app)
Definir escopos para Realtime Database e Authentication
gcloud
# Check the existing access scopes
gcloud compute instances describe [INSTANCE_NAME] --format json

# The above command returns the service account information. For example:
  "serviceAccounts": [
   {
    "email": "your.gserviceaccount.com",
    "scopes": [
     "https://www.googleapis.com/auth/cloud-platform",
     "https://www.googleapis.com/auth/userinfo.email"
     ]
    }
  ],

# Stop the VM, then run the following command, using the service account
# that gcloud returned when you checked the scopes.

gcloud compute instances set-service-account [INSTANCE_NAME] --service-account "your.gserviceaccount.com" --scopes "https://www.googleapis.com/auth/firebase.database,https://www.googleapis.com/auth/userinfo.email"
Como testar com credenciais de usuário final da gcloud
Mudanças são necessárias para usar o Firebase Authentication devido ao seguinte:
•	O Firebase Authentication não aceita credenciais de usuário final da gcloud geradas usando o ID do cliente do OAuth da gcloud.
•	O Firebase Authentication exige que o ID do projeto seja fornecido na inicialização para esse tipo de credencial de usuário final.
