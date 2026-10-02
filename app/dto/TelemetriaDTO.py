from pydantic import BaseModel, ConfigDict
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