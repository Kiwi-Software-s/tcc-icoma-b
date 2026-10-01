# Estado funcional do EcoPoints

Esta versão inclui:

- autenticação Firebase + sessão Flask;
- Firestore com usuários, códigos, resgates e trocas;
- pontos e kg acumulativos;
- dashboard com gráficos mensal/semanal/diário e ranking semanal;
- mapa com a Etec Sylvio de Mattos Carvalho;
- benefícios/descontos com saldo real e popup de confirmação;
- favoritos persistentes no Firestore;
- histórico de ganhos, kg e gastos;
- perfil do usuário com edição de nome e resumo do impacto;
- estados vazios e páginas 404/500;
- geração de novos lotes de códigos;
- seed de dados para apresentação;
- configuração de segurança para produção;
- arquivos de deploy para Render;
- smoke test e checklist de teste manual.

## Comandos do dia a dia

```bash
source .venv/Scripts/activate
python main.py
```

## Verificação antes da apresentação

```bash
python verificar_projeto.py
python -m unittest discover -s tests -v
```

## Novos códigos

```bash
python gerar_codigos.py
```

## Preparar conta de apresentação

```bash
python preparar_demo.py --email EMAIL_DA_CONTA
```
