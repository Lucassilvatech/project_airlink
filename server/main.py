from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from typing import Union, Optional

from modulos.manager_db import Manager_DB
from modulos.modelo import (
    ModelUser, DataLogin, HashLogin, ModelUserReturn, SearchVoos, Voos, DadosCarrinho
    )
from modulos.gera_keys import rendom_key, hex_crypt, chack_password

query = Manager_DB()

app = FastAPI()

origins = [
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'https://localhost:5500',
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
async def read_client(data_login: DataLogin) -> HashLogin:
    """Busca cliente na base de dados"""
    data = data_login.dict()
    result = query.select('users', 'email', data['email'])
    if not result: 
        raise HTTPException(status_code=409, detail='email_not_exist')

    if not chack_password(data['key_pw'], result[0]['key_pw']):
        raise HTTPException(status_code=409, detail='password_error') 

    key_lp = rendom_key()
    query.atualiza('permission_login','key_login', key_lp, 'id_user', result[0]['id'])
    result = {'id_user':result[0]['id'], 'nome':result[0]['nome'],'key_login': key_lp}
    return result


@app.get('/client/singin/permission')
async def read_permission(token:str):
    result = query.select('permission_login', 'key_login', token)
    if not result:
        return {'error': 'token_not_exist'}
    return result


@app.post('/client/singup', response_model=ModelUserReturn, status_code=201)
async def insert_client(user: ModelUser):
    """Inseri novos usuarios na base de dados"""
    user_dict = user.dict()
    user_dict['key_pw'] = hex_crypt(user_dict['key_pw'])
    keys = '(nome, email, key_pw)'
    values = tuple(user_dict.values())
    try:
        query.insert('users', keys, values)
        result = query.select('users','email', user_dict['email'])
        query.insert('permission_login', '(id_user, key_login)', (result[0]['id'], ''))
    except Exception as err:
        print(err)
        raise HTTPException(status_code=409, detail='DuplicateError')
    return user


@app.post('/client/carrinho/')
async def insert_passagem(carrinho: DadosCarrinho):
    carr = carrinho.dict()
    result = query.select('voos', 'numero_voo', carr['numero_voo'])
    query.insert(
        table='carrinho', keys='(id_voo, id_user)',
        values=(int(result[0]['id']), int(carr['user']))
        )
    if not result:
        return {'error': 'value_not_exist'}
    return result


@app.get('/search/carrinho/{user_id}')
async def search_passagem(user_id:int):
    response = []
    result = query.select_voos('carrinho', 'id_voo', 'id_user', int(user_id))
    if not result:
        return {'error': 'value_not_exist'}
    for valor in result:
        r = query.select('voos', 'id', int(valor['id_voo']))
        response.append(r)
    return response


@app.put('/voos')
async def read_voos():
    voos = query.select('voos')
    return voos


@app.post('/voos/search')
async def search_voos(search_voo: SearchVoos):
    voo = search_voo.dict()
    voos = query.select_passagens('voos', 'origem', voo['origem'], 'destino', voo['destino'] )
    return voos


@app.post('/staff/voos')
async def insert_voo(voo: Voos):
    values = tuple(voo.dict().values())
    keys = '(origem, destino, data_partida, data_chegada,\
             preco, lugares_disponiveis, numero_voo)'
    query.insert('voos', keys, values)
    return voo
