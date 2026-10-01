# Firestore - configuração rápida do EcoPoints

## 1. Criar o banco (uma única vez)

No Firebase Console do mesmo projeto usado pelo login:

1. Abra **Firestore Database**.
2. Clique em **Criar banco de dados**.
3. Escolha **Modo de produção**.
4. Escolha a região mais próxima disponível.
5. Confirme a criação.

O backend usa o Firebase Admin SDK, então não é necessário liberar regras públicas para o navegador.

## 2. Confirmar a chave local

Na raiz do projeto deve existir:

`serviceAccountKey.json`

Esse arquivo já está no `.gitignore` e não deve ser enviado ao GitHub.

## 3. Criar os códigos fixos

Com o ambiente virtual ativo:

```bash
python seed_firestore.py
```

O script cria códigos de papel, plástico, vidro e metal. Ele não reativa códigos que já tenham sido usados.

## 4. Iniciar o projeto

```bash
python main.py
```

Depois acesse `http://127.0.0.1:10000`.

## Códigos de demonstração

- ECO-PAPEL-001
- ECO-PAPEL-002
- ECO-PAPEL-003
- ECO-PLASTICO-001
- ECO-PLASTICO-002
- ECO-PLASTICO-003
- ECO-VIDRO-001
- ECO-VIDRO-002
- ECO-VIDRO-003
- ECO-METAL-001
- ECO-METAL-002
- ECO-METAL-003

## Troca de GreenPoints por benefícios

A tela **Meus descontos** também usa o Firestore. Não é preciso criar outra coleção manualmente.
Na primeira troca o sistema cria automaticamente a coleção `trocas` e desconta os GreenPoints do campo `usuarios/{uid}/pontos_total` usando uma transação.

O histórico passa a combinar automaticamente:

- `resgates`: pontos e kg recebidos pelos códigos de reciclagem;
- `trocas`: GreenPoints gastos em descontos/benefícios.

O ranking semanal continua considerando somente os pontos conquistados com reciclagem, enquanto o gráfico de evolução mostra o saldo de pontos depois dos ganhos e gastos.

## Gerar novos códigos quando os atuais acabarem

Os códigos continuam sendo de uso único. Para criar um novo lote sem apagar ou reativar códigos antigos, rode:

```bash
python gerar_codigos.py
```

Por padrão são criados **10 novos códigos para cada material** (40 no total), continuando a numeração existente.

Para criar 25 por material:

```bash
python gerar_codigos.py --quantidade 25
```

Para gerar apenas plástico:

```bash
python gerar_codigos.py --quantidade 10 --material plastico
```

A pontuação segue a mesma regra do projeto:

- Papel: 100 GreenPoints/kg
- Plástico: 150 GreenPoints/kg
- Vidro: 80 GreenPoints/kg
- Metal: 200 GreenPoints/kg

## Benefícios na dashboard

A seção **Benefícios Disponíveis** da dashboard agora usa exatamente o mesmo catálogo da tela **Meus descontos**. Assim, nome, imagem, porcentagem e preço em GreenPoints não ficam duplicados nem divergentes. Os cards e o botão **Ver todos os benefícios** levam para `/meus-descontos`.

## Perfil e favoritos

A partir desta versão, o documento `usuarios/{uid}` também pode conter:

- `favoritos`: lista de IDs dos benefícios favoritados;
- `updated_at`: última alteração do nome no perfil.

Não é necessário criar esses campos manualmente. O sistema adiciona quando forem usados.

## Conta de demonstração

Depois de criar/login em uma conta de teste, você pode preencher gráficos e histórico sem alterar os códigos existentes:

```bash
python preparar_demo.py --email EMAIL_DA_CONTA
```

O script só roda uma vez por UID e cria um marcador em `demo_seeds` para evitar duplicação.
