from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ModelUser(BaseModel):
    nome: str
    email: str
    key_pw: str
    detail: str 
    
