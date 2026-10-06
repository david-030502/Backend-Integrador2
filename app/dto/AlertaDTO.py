from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AlertaRespuestaDTO(BaseModel):
    id_alerta:int
    tipo_alerta:str
    descripcion:Optional[str] = None
    fecha_hora:datetime
    fecha_vista:Optional[datetime]=None
    id_lectura:int
    id_usuario:Optional[int]=None

    model_config = ConfigDict(from_attributes=True)

class AtenderAlertaDTO(BaseModel):
    id_usuario:int