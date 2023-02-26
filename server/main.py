from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from typing import Union, Optional

from manager_db import Manager_DB
from modelo import ModelUser

query = Manager_DB()

app = FastAPI()

origins = [
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'https://localhost:5000',

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def read_root():
    return{'algo': 'outro'} 


@app.get('/airfare/{id_airfare}')
async def read_airfare(id_airfare: int, destination: Optional[Union[str, None]] = None):
    return {'id_airfare':id_airfare, 'destination': destination}


@app.get('/client/singin')
async def read_client(email:str, password:str = None):
    """busca cliente na base de dados"""
    result = query.select('users', 'email', email)
    if not result: 
        return {'error': 'email_not_exist'}

    if not result[0]['key_pw'] == password:
        return {'error':'password_error'}
    
    return result

@app.get('/client', response_model=list[ModelUser])
async def read_client():
    """Busca por todos os clientes da base de dados"""
    result = query.select('users')
    if result: 
        return result


@app.post('/client/singup', response_model=ModelUser, status_code=201)
async def insert_client(user: ModelUser):
    """Inseri novos usuarios na base de dados"""
    keys = '(nome, email, key_pw, detail)'
    values = tuple(user.dict().values())
    try:
        query.insert('users', keys, values)
    except Exception:
        raise HTTPException(status_code=405, detail='DuplicateError')
    return user


