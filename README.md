# Finance API 💰

API RESTful para gerenciamento de autenticação de usuários com JWT, desenvolvida em FastAPI com PostgreSQL.

## 📋 Características

- 🔐 Autenticação JWT segura
- 👤 Registro e login de usuários
- 🔒 Senhas com hash bcrypt
- 🗄️ Banco de dados PostgreSQL
- 🐳 Docker & Docker Compose
- 📚 FastAPI com validação automática (Pydantic)
- 🛡️ Proteção de rotas com tokens

## 📦 Requisitos

- Docker & Docker Compose
- Python 3.9+ (se rodar localmente)
- PostgreSQL 14+ (se rodar localmente)

## 🚀 Instalação e Configuração

### Usando Docker (Recomendado)

1. **Clone o repositório**
   ```bash
   git clone <seu-repo>
   cd finance-api
   ```

2. **Configure as variáveis de ambiente** (opcional)
   ```bash
   cp .env.example .env
   ```
   
   Ou crie um arquivo `.env`:
   ```env
   SECRET_KEY=sua-chave-secreta-muito-segura-aqui
   DATABASE_URL=postgresql://user:password@db:5432/finance_db
   ```

3. **Inicie os containers**
   ```bash
   sudo docker compose up --build
   ```

4. **Acesse a API**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Instalação Local

1. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o banco de dados**
   ```bash
   # Atualize a DATABASE_URL no app/database.py
   ```

4. **Execute a aplicação**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📁 Estrutura do Projeto

```
finance-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Rotas e configuração FastAPI
│   ├── models.py            # Modelos SQLAlchemy (Banco de dados)
│   ├── schemas.py           # Schemas Pydantic (Validação)
│   ├── database.py          # Configuração do banco de dados
│   └── __pycache__/
├── Dockerfile               # Imagem Docker da aplicação
├── docker-compose.yml       # Orquestração de containers
├── requirements.txt         # Dependências Python
├── .env.example             # Exemplo de variáveis de ambiente
└── README.md                # Este arquivo
```

## 🔗 Endpoints

### 1. Registrar Novo Usuário
```http
POST /register/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "senha_segura_123"
}
```

**Resposta (200):**
```json
{
  "id": 1,
  "email": "usuario@example.com"
}
```

### 2. Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=usuario@example.com&password=senha_segura_123
```

**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Obter Dados do Usuário Autenticado
```http
GET /me
Authorization: Bearer {access_token}
```

**Resposta (200):**
```json
{
  "id": 1,
  "email": "usuario@example.com"
}
```

### 4. Raiz da API
```http
GET /
```

**Resposta (200):**
```json
{
  "message": "Welcome to the Finance API!"
}
```

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Fluxo de autenticação:

1. Usuário se registra em `/register/` com email e senha
2. Usuário faz login em `/token` recebendo um `access_token`
3. Usuário inclui o token no header `Authorization: Bearer {token}` para acessar rotas protegidas
4. Token expira em 30 minutos (configurável)

### Usando o token com curl:
```bash
curl -H "Authorization: Bearer seu_token_aqui" http://localhost:8000/me
```

## 🔧 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Segurança JWT
SECRET_KEY=sua-chave-secreta-muito-segura-aqui

# Banco de dados
DATABASE_URL=postgresql://user:password@db:5432/finance_db

# FastAPI
DEBUG=False
```

## 🧪 Testando a API

### Usando Swagger UI (Recomendado)
Abra no navegador: http://localhost:8000/docs

### Usando curl

**Registrar:**
```bash
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com",
    "password": "senha123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@example.com&password=senha123"
```

**Acessar rota protegida:**
```bash
curl -H "Authorization: Bearer SEU_TOKEN" http://localhost:8000/me
```

## 🐳 Comandos Docker

```bash
# Iniciar containers
sudo docker compose up -d

# Parar containers
sudo docker compose down

# Limpar volumes (dados)
sudo docker compose down -v

# Ver logs
sudo docker compose logs -f app

# Executar comando no container
sudo docker compose exec app python script.py
```

## 🛠️ Desenvolvimento

### Instalar dependências adicionais
```bash
pip install -r requirements.txt
```

### Criar nova migração (com Alembic)
```bash
alembic revision --autogenerate -m "Descrição da mudança"
alembic upgrade head
```

### Rodando testes (quando implementar)
```bash
pytest
```

## 📊 Banco de Dados

### Tabela Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL
);
```

As tabelas são criadas automaticamente ao iniciar a aplicação.

## 🔄 Ciclo de vida do container

1. **Build**: Docker cria a imagem da aplicação
2. **Run**: Container PostgreSQL inicia
3. **Init**: FastAPI cria as tabelas automaticamente
4. **Listen**: Aplicação aguarda requisições em `0.0.0.0:8000`

## 🚨 Troubleshooting

### Erro: "port 5432 already in use"
```bash
# Libere a porta ou use outra
sudo docker compose down -v
# ou configure outra porta no docker-compose.yml
```

### Erro: "Connection refused"
```bash
# Verifique se todos os containers estão rodando
sudo docker compose ps

# Veja os logs
sudo docker compose logs db
```

### Erro: "relation users does not exist"
```bash
# Reinicie do zero
sudo docker compose down -v
sudo docker compose up --build
```

## 📝 Exemplo de Extensão

Para adicionar novas rotas protegidas:

```python
@app.post("/transacoes/")
def criar_transacao(
    transacao: schemas.TransacaoCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    # Validar token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    
    # Buscar usuário
    usuario = db.query(models.User).filter(models.User.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Criar transação
    nova_transacao = models.Transacao(usuario_id=usuario.id, **transacao.dict())
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao
```

## 📄 Licença

MIT License - Sinta-se livre para usar em seus projetos!

## 👨‍💻 Autor

Desenvolvido com ❤️ usando FastAPI

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Abra uma issue ou PR.

---

**Última atualização:** Fevereiro 2026
