# 💸 API de Conta Digital com FastAPI

Projeto desenvolvido como desafio técnico do bootcamp do **Magazine Luiza** na plataforma **DIO (Digital Innovation One)**.

---

## 🚀 Sobre o projeto

Esta API simula um sistema de conta digital, permitindo:

* 👤 Cadastro de usuários
* 🔐 Autenticação com JWT
* 🏦 Criação automática de conta (1:1)
* 💸 Depósitos e saques
* 📊 Consulta de extrato com paginação e filtros

---

## 🧠 Regras de negócio

* Um usuário possui **uma única conta** (1:1)
* Uma conta possui **várias transações** (1:N)
* Não é possível sacar valores maiores que o saldo
* Apenas usuários autenticados podem realizar transações

---

## 🛠️ Tecnologias utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy (Async)
* PostgreSQL
* JWT (python-jose)
* Bcrypt
* Poetry

---

## 📂 Estrutura do projeto

```
project/
│
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py
│       │   ├── usuario.py
│       │   └── transacao.py
│       └── api.py
│
├── core/
│   ├── auth.py
│   ├── security.py
│   ├── deps.py
│   ├── database.py
│   └── configs.py
│
├── models/
│   ├── usuario_model.py
│   ├── conta_model.py
│   └── transacoes_model.py
│
├── schemas/
│   ├── usuario_schema.py
│   ├── conta_schema.py
│   └── transacao_schema.py
│
├── services/
│   ├── user_service.py
│   └── transaction_service.py
│
├── main.py
└── criar_tabelas.py
```

---

## 🔐 Autenticação

A autenticação é feita via JWT.

### Login:

```
POST /api/v1/auth/login
```

Retorna:

```json
{
  "access_token": "TOKEN",
  "token_type": "bearer"
}
```

Use o token no Swagger ou via header:

```
Authorization: Bearer TOKEN
```

---

## 📌 Endpoints principais

### 👤 Criar usuário

```
POST /api/v1/users
```

```json
{
  "email": "user@email.com",
  "senha": "123456"
}
```

---

### 🔐 Login

```
POST /api/v1/auth/login
```

---

### 💸 Criar transação

```
POST /api/v1/transactions
```

```json
{
  "amount": 100,
  "transaction_type": "credit"
}
```

---

### 📊 Extrato

```
GET /api/v1/transactions
```

#### Parâmetros opcionais:

```
?page=1&limit=10&type=credit
```

---

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório

```
git clone <seu-repo>
cd projeto
```

---

### 2. Instalar dependências

```
poetry install
```

---

### 3. Configurar variáveis de ambiente

Exemplo de `DATABASE_URL`:

```
postgresql+asyncpg://postgres:123456@localhost:5432/banco_transacoes
```

---

### 4. Criar as tabelas

```
poetry run python criar_tabelas.py
```

---

### 5. Rodar a aplicação

```
fastapi dev
```

---

## 🌐 Acessar documentação

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Fluxo de uso

1. Criar usuário
2. Fazer login
3. Autorizar no Swagger
4. Criar transações
5. Consultar extrato

---

## 📈 Possíveis melhorias

* Paginação com metadata (total, páginas)
* Filtros avançados
* Testes automatizados
* Dockerização
* Deploy em cloud
* Logs estruturados

---

## 👨‍💻 Autor

Desenvolvido por **Marconys Moura**

---

## 🏆 Desafio

Projeto desenvolvido como parte do bootcamp do **Magazine Luiza** na plataforma **DIO**.
