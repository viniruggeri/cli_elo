# backend/database/models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    papel: str
    email: str
    
class Bairro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    area_risco_prop: float
    pop_densidade: float
    
    
class Ocorrencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    categoria: str
    data: str # YYYY-MM-DD
    status: str
    localizacao: str
    usuario_id: int = Field(foreign_key="usuario.id")
    bairro_id: int  = Field(foreign_key="bairro.id")