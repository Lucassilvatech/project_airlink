from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ModelUser(BaseModel):
    nome: str
    email: str
    key_pw: str


class ModelUserReturn(BaseModel): # nomear com out e in esses modelos de entrada e saida
    nome: str
    email: str


class DataLogin(BaseModel):
    email: str 
    key_pw: str


class RecoverLogin(BaseModel):
    id: int
    key_pw: str


class HashLogin(BaseModel):
    id_user: int
    nome: str
    key_login: str
    

class Voos(BaseModel):
    origem: str
    destino: str
    data_partida: str
    data_chegada: str
    preco: float
    lugares_disponiveis: int
    numero_voo: str


class SearchVoos(BaseModel):
    origem: str
    destino: str


class DadosCarrinho(BaseModel):
    numero_voo: str
    user: int


class UserVooDelete(BaseModel):
    num_voo: str
    user: int
      