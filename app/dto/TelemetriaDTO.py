from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class LecturaSensorDTO(BaseModel):
    sensor:str
    t:int
    v:float

class CoordenadasDTO(BaseModel):
    t:int
    lat:float
    lon:float
    speed:Optional[float] = 0.0
    alt:Optional[float] = 0.0
    fix:int

class AlertasDTO(BaseModel):
    sensor:str
    type:str
    threshold:float
    value:float
    t:int

class TelemetriaLoteEntradaDTO(BaseModel):
    device_id: str
    schema_version:int
    batch_id:int
    sent_at:int
    nonce: int = Field(ge=0, le=4294967295)
    signature: str = Field(min_length=64, max_length=64)
    readings:List[LecturaSensorDTO]
    gps:List[CoordenadasDTO]
    alerts:Optional[List[AlertasDTO]] = []

class TelemetriaRespuestaDTO(BaseModel):
    id_lectura:int
    id_dispositivo:int
    temperatura:float
    humedad:float
    gases:float
    latitud:float
    longitud:float
    fecha_hora:datetime

    model_config = ConfigDict(from_attributes=True)