from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str
    cnpj: constr(min_length=10, max_length=14) # type: ignore
    endereco: Optional[str] = None
    email: EmailStr
    telefone: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int

    class Config:
        orm_mode = True

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str 
    empresa_id: int

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int

    class Config:
        orm_mode = True