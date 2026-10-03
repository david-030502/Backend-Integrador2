from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UsuarioCrearDTO(BaseModel):
    nombre:str = Field(..., max_length=70)
    email:EmailStr = Field(..., max_length=120)
    contrasena:str = Field(..., min_length=8, max_length=30)
    rol:str = Field(default="operador", max_length=20)

class UsuarioRespuestaDTO(BaseModel):
    id_usuario:int
    nombre:str
    email:str
    rol:str

    model_config = ConfigDict(from_attributes=True)

class LoginDTO(BaseModel):
    email:EmailStr
    contrasena:str

class LoginRespuestaDTO(BaseModel):
    access_token:str
    token_type:str = "bearer"
    id_usuario:int
    nombre:str
    email:str
    rol:str