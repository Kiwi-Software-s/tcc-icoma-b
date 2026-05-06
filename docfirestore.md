#  Modelo de Dados do Cloud Firestore

O **Cloud Firestore** é um banco de dados NoSQL orientado a documentos. Diferente de bancos SQL tradicionais, ele não utiliza tabelas ou linhas. Toda a estrutura é baseada em **Documentos** e **Coleções**.

##  Documentos
A unidade básica de armazenamento no Firestore é o **documento**. Ele funciona como um registro leve que contém campos mapeados para valores (semelhante a um objeto JSON). <img width="635" height="247" alt="image" src="https://github.com/user-attachments/assets/8b7480b5-39fd-43d7-b0f2-fbdd5473a5f1" />


- **Pares Chave-Valor:** Podem armazenar tipos primitivos (strings, números, booleanos, timestamps) e objetos complexos.
- **Mapas (Maps):** São objetos aninhados dentro de um documento, ideais para estruturar dados internos (ex: um campo `nome` contendo `primeiro` e `ultimo`). <img width="342" height="226" alt="image" src="https://github.com/user-attachments/assets/14c8864b-4680-4f5d-862b-cf12d404998a" />

- **Limites:** O Firestore é otimizado para lidar com *grandes coleções de documentos pequenos*.

##  Coleções
<img width="402" height="324" alt="image" src="https://github.com/user-attachments/assets/006dae2c-dd37-4d46-ad17-5674c9ed75b9" />

Os documentos não ficam soltos; eles precisam, obrigatoriamente, pertencer a **coleções**. Uma coleção atua como um "recipiente" para os documentos.

- **Criação Implícita:** Não é necessário "criar" ou "excluir" coleções previamente. Ao salvar o primeiro documento, a coleção passa a existir. Se todos os documentos forem apagados, a coleção deixa de existir.
- **Sem Esquemas (Schemaless):** Documentos na mesma coleção podem ter campos diferentes, embora seja uma boa prática manter a consistência para facilitar consultas. <img width="778" height="466" alt="image" src="https://github.com/user-attachments/assets/25c1d2a4-66a4-4ce9-ba72-a44040e9fdaa" />

- **Regra de Ouro:** Uma coleção contém **apenas documentos**. Ela não pode conter campos brutos (valores) nem outras coleções diretamente.

[Assista à explicação oficial no YouTube](https://youtu.be/v_hR4K4auoQ)

##  Referências
Para ler ou gravar dados, você precisa apontar para a localização deles usando uma **referência**. Criar uma referência é uma operação leve e não executa chamadas de rede.

**Exemplo em Python:**
```python
# Referência a um documento específico
a_lovelace_ref = db.collection("users").document("alovelace")

# Ou usando o caminho em formato de string
a_lovelace_ref = db.document("users/alovelace")

# Referência a uma coleção inteira
users_ref = db.collection("users")
