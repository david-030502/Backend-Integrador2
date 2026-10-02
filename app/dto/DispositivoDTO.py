from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class DispositivoCrearDTO(BaseModel):
    placa:str = Field(..., max_length=7)
    nombre_chofer:str = Field(..., max_length=70)
    estado:str = Field(default="Activo", max_length=20)

class DispositivoActualizarDTO(BaseModel):
    placa: Optional[str] = Field(default=None, max_length=7)
    nombre_chofer: Optional[str] = Field(default=None, max_length=70)
    estado: Optional[str] = Field(default=None, max_length=20)

class DispositivoRespuestaDTO(BaseModel):
    id_dispositivo:int
    placa:str
    nombre_chofer:str
    estado:str

    model_config = ConfigDict(from_attributes=True)