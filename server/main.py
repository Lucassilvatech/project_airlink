from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from typing import Union, Optional

from manager_db import Manager_DB
from modelo import ModelUser, DataLogin
from gera_keys import rendom_key, hex_crypt, chack_password

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


@app.post('/client/singin')
async def read_client(data_login: DataLogin):
    """Busca cliente na base de dados"""
    data = data_login.dict()
    result = query.select('users', 'email', data['email'])
    if not result: 
        raise HTTPException(status_code=405, detail='email_not_exist')

    if not chack_password(data['key_pw'], result[0]['key_pw']):
        raise HTTPException(status_code=405, detail='password_error') 

    key_lp = rendom_key()
    query.atualiza('permission_login','key_login', key_lp, 'id_user', result[0]['id'])
    result = {'key_login': key_lp}
    return result


@app.get('/client/singin/permission')
async def read_permission(token:str):
    result = query.select('permission_login', 'key_login', token)
    if not result:
        return {'error': 'token_not_exist'}
    return result


@app.post('/client/singup', response_model=ModelUser, status_code=201)
async def insert_client(user: ModelUser):
    """Inseri novos usuarios na base de dados"""
    user_dict = user.dict()
    user_dict['key_pw'] = hex_crypt(user_dict['key_pw'])
    keys = '(nome, email, key_pw, detail)'
    values = tuple(user_dict.values())
    try:
        query.insert('users', keys, values)
        result = query.select('users','email', user_dict['email'])
        query.insert('permission_login', '(id_user, key_login)', (result[0]['id'], ''))
    except Exception as err:
        print(err)
        raise HTTPException(status_code=405, detail='DuplicateError')
    return user


