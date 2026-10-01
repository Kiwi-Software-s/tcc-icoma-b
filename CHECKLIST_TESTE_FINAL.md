# Checklist final do EcoPoints

Execute primeiro:

```bash
source .venv/Scripts/activate
python verificar_projeto.py
python main.py
```

## Fluxo do usuário

- [ ] Criar uma conta nova.
- [ ] Fazer login e confirmar que a dashboard abre zerada sem quebrar.
- [ ] Resgatar um código válido e conferir pontos + kg.
- [ ] Tentar o mesmo código novamente e confirmar a mensagem de código já utilizado.
- [ ] Digitar um código inexistente e confirmar a mensagem de erro.
- [ ] Alternar os gráficos entre Mensal, Semanal e Diário.
- [ ] Favoritar um benefício, atualizar a página e confirmar que continua marcado.
- [ ] Resgatar benefício com saldo suficiente e confirmar a queda do saldo.
- [ ] Tentar benefício sem saldo suficiente e confirmar o bloqueio.
- [ ] Abrir Histórico e conferir ganho, kg, gasto e protocolo.
- [ ] Abrir Meu perfil, alterar o nome e atualizar a página.
- [ ] Abrir o mapa e confirmar a Etec como único ponto de coleta.
- [ ] Fazer logout e login novamente; confirmar que os dados continuam salvos.

## Fluxo de funcionário e admin

- [ ] Entrar com uma conta admin e abrir `/admin`.
- [ ] Transformar uma conta comum em `funcionario` pelo painel admin.
- [ ] Entrar com a conta funcionário e abrir `/funcionario`.
- [ ] Gerar um código informando material e peso.
- [ ] Copiar o código e resgatá-lo em uma conta de usuário.
- [ ] Confirmar que o código aparece como usado no painel admin.
- [ ] Confirmar que usuário comum recebe 403 ao tentar abrir `/funcionario` ou `/admin`.
- [ ] Confirmar que o admin não consegue remover o próprio acesso por engano.

## Mobile e acabamento

- [ ] Testar a largura de celular no DevTools (375 px ou semelhante).
- [ ] Confirmar que aparece o menu de três barras e a sidebar desktop some.
- [ ] Abrir e fechar o menu móvel pelo botão, fundo escuro e tecla Esc.
- [ ] Conferir dashboard, descontos, histórico, dicas, mapa, funcionário e admin no mobile.
- [ ] Confirmar que não existe rolagem horizontal indesejada.
- [ ] Conferir ícones e textos de navegação em todas as telas.
- [ ] Abrir uma URL inexistente e conferir a página 404.

## Antes do deploy

- [ ] `serviceAccountKey.json` não está no GitHub.
- [ ] `FLASK_SECRET_KEY` está configurada em produção.
- [ ] `FLASK_DEBUG` está desligado em produção.
- [ ] Manter alguns códigos disponíveis para a apresentação.
