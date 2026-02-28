# Finance API 💰

API RESTful para autenticação de usuários com JWT usando FastAPI + PostgreSQL.

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

## 🚀 Quick start (rápido)

1. Copie o exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```
2. Suba o banco (docker):
```bash
docker compose up -d db
```
3. Rode a API (local) ou via Docker:
```bash
# local
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# via docker-compose (recomendado quando o DB estiver em container)
docker compose up --build
```

A documentação interativa: http://localhost:8000/docs

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

## 🖥️ Web Interface

A aplicação agora inclui páginas HTML simples para interagir com a API via navegador:

* **/** – página inicial com links para registro/login
* **/register** – formulário de cadastro de usuário
* **/login** – formulário de login, armazena o token no localStorage
* **/me/page** – mostra os dados do usuário logado (requer token válido no localStorage)

Os templates estão em `app/templates` e os arquivos estáticos em `app/static`.


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

## 🔐 Autenticação (resumido)

1. Registrar: `POST /register/` com JSON {"email","password"}.  
   **Obs:** a senha não deve exceder 72 bytes (aprox. 72 caracteres UTF‑8) por causa do limite do bcrypt. O esquema Pydantic valida os caracteres e, se o valor em bytes for maior que 72, ele será **cortado automaticamente** antes de armazenar (o usuário verá um avisocomo resposta 200, mas apenas os primeiros 72 bytes serão usados).
2. Login: `POST /token` (form) com `username=email` e `password` → recebe `access_token`.
3. Usar: incluir header `Authorization: Bearer <token>` nas requisições.
4. Token expira em 30 minutos por padrão.

**Nota:** se o servidor retornar um erro 500 ao cadastrar, verifique se a senha excede 72 bytes ou se a biblioteca `bcrypt` está atualizada; o código agora converte essa condição em um 400.

Curl rápido:
```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@example.com&password=senha"

curl -H "Authorization: Bearer SEU_TOKEN" http://localhost:8000/me
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
