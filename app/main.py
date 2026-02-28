from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, schemas, database
import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os

# --- Configurações JWT ---
# `SECRET_KEY` deve ser definido no arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-muito-segura-aqui")
# Algoritmo usado para assinar/validar JWT
ALGORITHM = "HS256"
# Tempo de expiração do token em minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Segurança ---
# Dependência OAuth2 que lê o token do header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Criar tabelas ---
models.Base.metadata.create_all(bind=database.engine)

# --- App FastAPI ---
app = FastAPI()

# --- Static & Templates ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --- Rotas ---

@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Registrar novo usuário.

    Recebe JSON com `email` e `password`. Salva usuário com senha hasheada.
    Retorna o usuário criado (sem a senha).
    """
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    

    pwd_bytes = user.password.encode("utf-8")
    if len(pwd_bytes) > 72:
        
        pwd_bytes = pwd_bytes[:72]
       
        user_password = pwd_bytes.decode("utf-8", errors="ignore")
    else:
        user_password = user.password

    hashed_bytes = bcrypt.hashpw(user_password.encode("utf-8"), bcrypt.gensalt())
    hashed_password = hashed_bytes.decode("utf-8")
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Login: retorna um JWT.

    Recebe dados form `username` (email) e `password` como `application/x-www-form-urlencoded`.
    Se credenciais válidas, retorna `access_token` (Bearer).
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not bcrypt.checkpw(form_data.password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.email, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Retorna os dados do usuário autenticado.

    Espera header `Authorization: Bearer <token>`.
    Decodifica o JWT e retorna o usuário correspondente.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@app.get("/")
def read_root(request: Request):
    # Página inicial (template)
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/register")
def register_page(request: Request):
    # Página de registro (formulário)
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    # Página de login (formulário que envia para /token)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/me/page")
def read_me_page(request: Request):
    # Página que exibe informações do usuário logado (usa token no front-end)
    return templates.TemplateResponse("me.html", {"request": request})
