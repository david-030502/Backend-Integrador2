from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class AlertaRespuestaDTO(BaseModel):
    id_alerta:int
    tipo_alerta:str
    descripcion:Optional[str] = None
    fecha_hora:datetime
    fecha_vista:Optional[datetime]=None
    id_lectura:int
    id_usuario:Optional[int]=None
    id_dispositivo: int
    placa: str

    model_config = ConfigDict(from_attributes=True)
    
class AlertasPaginadasDTO(BaseModel):
    alertas: List[AlertaRespuestaDTO]
    pagina: int
    limite: int
    total: int
    total_paginas: int

class AtenderAlertaDTO(BaseModel):
    id_usuario:int