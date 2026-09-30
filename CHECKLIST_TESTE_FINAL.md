# Checklist final do EcoPoints

Execute primeiro:

```bash
source .venv/Scripts/activate
python verificar_projeto.py
python main.py
```

Depois teste no navegador, nesta ordem:

- [ ] Criar uma conta nova.
- [ ] Fazer login e confirmar que a dashboard abre zerada sem quebrar.
- [ ] Resgatar um código válido e conferir pontos + kg.
- [ ] Tentar o mesmo código novamente e confirmar a mensagem "já utilizado".
- [ ] Digitar um código inexistente e confirmar a mensagem de erro.
- [ ] Alternar os gráficos entre Mensal, Semanal e Diário.
- [ ] Conferir ranking com 1 usuário e depois com mais usuários.
- [ ] Favoritar um benefício, atualizar a página e confirmar que o coração continua marcado.
- [ ] Resgatar benefício com saldo suficiente e confirmar a queda do saldo.
- [ ] Tentar benefício sem saldo suficiente e confirmar bloqueio/mensagem.
- [ ] Abrir Histórico e conferir ganho, kg, gasto e protocolo.
- [ ] Abrir Meu perfil, alterar o nome e atualizar a página.
- [ ] Abrir o mapa e confirmar a Etec como ponto de coleta.
- [ ] Fazer logout e login novamente; confirmar que tudo continua salvo.
- [ ] Abrir uma URL inexistente e conferir a página 404.

Para uma conta com dados bonitos de apresentação:

```bash
python preparar_demo.py --email EMAIL_DA_CONTA
```

Esse script não duplica os dados se for executado duas vezes para o mesmo usuário.
