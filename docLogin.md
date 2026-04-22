Adicionar o SDK Admin do Firebase ao servidor
Admin SDK é um conjunto de bibliotecas de servidor que permite interagir com o Firebase usando ambientes privilegiados para executar ações.
Configurar um projeto e uma conta de serviço do Firebase
Para usar o Firebase Admin SDK, você precisa de um projeto do Firebase, uma conta de serviço do SDK Admin do Firebase (ela é gerada automaticamente quando você cria um projeto do Firebase) e um arquivo de configuração com as credenciais da sua conta de serviço.
Se você ainda não tem um projeto do Firebase, crie um no console do Firebase.
Adicionar o SDK
Será necessário instalar o SDK para a linguagem de sua escolha.
SDK Admin para Python do Firebase está disponível via PIP. Instale a biblioteca para todos os usuários:
sudo pip install firebase-admin
Para instalar a biblioteca apenas para o usuário atual:
pip install –user firebase-admin

Inicializar o SDK
Depois de criar um projeto do Firebase, é possível inicializar o SDK com o Application Default Credentials do Google. Como a pesquisa de credenciais padrão é totalmente automatizada esse método é recomendado para aplicativos executados em ambientes do Google.
Para especificar opções de inicialização para serviços, use a variável de ambiente FIREBASE_CONFIG. Caso o conteúdo da variável comece com {, ele será analisado como um objeto JSON. Caso contrário, a string será tratada pelo SDK como o caminho de um arquivo JSON que contém as opções.
default_app = firebase_admin.initialize_app()

Como usar um token de atualização do OAuth 2.0
Admin SDK fornece uma credencial que permite a autenticação com um token de atualização do Google OAuth2:
cred = credentials.RefreshToken('path/to/refreshToken.json')
default_app = firebase_admin.initialize_app(cred)

Inicializar o SDK em ambientes que não são do Google
Em um ambiente de servidor que não seja do Google em que a pesquisa de credenciais padrão não é totalmente automatizada, inicialize o SDK com um arquivo de chave da conta de serviço exportado.
Se você estiver desenvolvendo código ou implantando o aplicativo localmente, será possível usar credenciais recebidas por essa conta de serviço para autorizar solicitações do servidor. Para autenticar uma conta de serviço e autorizá-la para acessar os serviços do Firebase, gere um arquivo de chave privada no formato JSON.
Para gerar um arquivo de chave privada, siga estas etapas:
•	No console Firebase, abra Configurações > Contas de serviço.
•	Clique em Gerar nova chave privada e selecione Gerar chave.

Ao autorizar usando uma conta de serviço, existem duas opções para fornecer as credenciais ao seu aplicativo. Defina a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS ou transmita explicitamente o caminho para a chave da conta de serviço no código. A primeira opção é mais segura.
Para definir a variável de ambiente:
Defina GOOGLE_APPLICATION_CREDENTIALS como o caminho do arquivo JSON que contém a chave da conta de serviço. Essa variável só se aplica à sessão de shell atual. Dessa maneira, se você abrir uma nova sessão, defina a variável novamente.
Com o PowerShell:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\service-account-file.json"
Após concluir as etapas acima, o Application Default Credentials poderá determinar implicitamente suas credenciais, permitindo que você use as credenciais da conta de serviço ao testar ou executar em ambientes que não são do Google.
Inicialize o SDK:
default_app = firebase_admin.initialize_app()
Inicializar vários aplicativos
# Import the Firebase service
from firebase_admin import auth

# Initialize the default app
default_app = firebase_admin.initialize_app(cred)
print(default_app.name)  # "[DEFAULT]"

# Retrieve services via the auth package...
# auth.create_custom_token(...)
Alguns casos de uso exigem que você crie vários aplicativos ao mesmo tempo. Por exemplo, talvez você queira ler dados do Realtime Database de um projeto do Firebase e criar tokens personalizados para outro projeto. Com o SDK do Firebase, você cria vários apps ao mesmo tempo, cada um com as próprias informações de configuração.
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
Se você estiver usando uma VM do Google Compute Engine com o Application Default Credentials do Google para Realtime Database ou Authentication, configure também os escopos de acesso corretos. Para Realtime Database e Authentication, você precisa de escopos que terminem em userinfo.email e cloud-platform ou firebase.database. Para verificar os escopos de acesso existentes e alterá-los, execute os comandos abaixo usando a gcloud.
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
É possível gerar Application Default Credentials do Google na gcloud usando seu próprio ID do cliente do OAuth 2.0. O ID precisa ser do tipo app para computador.
gcloud auth application-default login --client-id-file=[/path/to/client/id/file]
É possível especificar o ID do projeto explicitamente na inicialização do app ou apenas usar a variável de ambiente GOOGLE_CLOUD_PROJECT.
Para especificar explicitamente o ID do projeto:
app_options = {'projectId': '<FIREBASE_PROJECT_ID>'}
default_app = firebase_admin.initialize_app(options=app_options)
