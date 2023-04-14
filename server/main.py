from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from typing import Union, Optional

from modulos.manager_db import Manager_DB, IntegrityError
from modulos.modelo import (
    ModelUser, DataLogin, HashLogin, ModelUserReturn, SearchVoos, Voos, DadosCarrinho,
    UserVooDelete
    )
from modulos.gera_keys import rendom_key, hex_crypt, chack_password, number_key
from modulos.send_email import send_email_recovery

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
    """Verifica as permissoes de login do usuário"""
    result = query.select('permission_login', 'key_login', token)
    if not result:
        return {'error': 'token_not_exist'}
    return result


@app.post('/user/code')
async def get_code_recovery(id_user):
    """Retorna um codigo para recuperação de senha"""
    result = query.select('key_recovery', 'id_user', id_user)
    if not result:
        return {'error': 'email_not_exist'}
    return{'codigo':result[0]['codigo']}


@app.post('/user/recovery/code')
async def set_code_recovery_pw(email:str):
    """Retorna um codigo para recuperação de senha"""
    result = query.select('users', 'email', email)
    if not result:
        return {'error': 'email_not_exist'}
    codigo = number_key()
    try:
        query.insert('key_recovery','(id_user, codigo)', (result[0]['id'], codigo))
    except IntegrityError as err:
        query.delete_record('key_recovery','id_user', result[0]['id'])
        query.insert('key_recovery','(id_user, codigo)', (result[0]['id'], codigo))

    send_email_recovery(email_destinatario=email, codigo=codigo)
    return {'id':result[0]['id']}


@app.post('/client/singup', response_model=ModelUserReturn, status_code=201)
async def insert_client(user: ModelUser):
    """Inseri novos usuários na base de dados"""
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
    """Insere as passagens na tabela carrinho"""
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
    """Busca as passagens no carrinho referente ao usuário"""
    response = []
    result = query.select_voos('carrinho', 'id_voo', 'id_user', int(user_id))
    if not result:
        return {'error': 'value_not_exist'}
    for valor in result:
        resp = query.select('voos', 'id', int(valor['id_voo']))
        response.append(resp)
    return response


@app.delete('/search/carrinho/remove/')
async def passagem_remove(voo_user:UserVooDelete):
    """Deleta passagens do carrinho"""
    voo_user = voo_user.dict()
    voo = query.select_voos('voos', values='*', column='numero_voo', value=voo_user['num_voo'])
    query.delete_carrinho('carrinho', id_voo=voo[0]['id'], id_user=voo_user['user'])
    


@app.put('/voos')
async def read_voos():
    """Busca por voos de forma genérica na base de dados"""
    voos = query.select('voos')
    return voos


@app.post('/voos/search')
async def search_voos(search_voo: SearchVoos):
    """Busca por voos especificos"""
    voo = search_voo.dict()
    voos = query.select_passagens('voos', 'origem', voo['origem'], 'destino', voo['destino'] )
    return voos


@app.post('/staff/voos')
async def insert_voo(voo: Voos):
    """Insere novos voos"""
    values = tuple(voo.dict().values())
    keys = '(origem, destino, data_partida, data_chegada,\
             preco, lugares_disponiveis, numero_voo)'
    query.insert('voos', keys, values)
    return voo

