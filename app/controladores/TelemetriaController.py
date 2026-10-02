from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from app.dto.TelemetriaDTO import TelemetriaLoteEntradaDTO, TelemetriaRespuestaDTO
from app.servicios.TelemetriaService import TelemetriaService
from app.servicios.DispositivoService import DispositivoService
from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/telemetria", tags = ["Telemetria"])
servicio = TelemetriaService()
servicio_dispositivos = DispositivoService()

@router.post("/",status_code=status.HTTP_201_CREATED)
def recibir_telemetria(datos: TelemetriaLoteEntradaDTO):
    """
        Endpoint que recibe el paquete JSON desde el ESP32,
        lo valida mediante el DTO y lo manda a procesar al
        servicio
    """
    dispositivo = servicio_dispositivos.obtener_dispositivo_bymac(datos.device_id)
    if not dispositivo:
        dispositivo = servicio_dispositivos.registrar_dispositivo_bymac(
            datos.device_id
        )

    print("Payload recibido:", datos.model_dump_json())
    respuesta = servicio.procesar_lote_telemetria(datos, dispositivo.id_dispositivo)
    return respuesta

@router.get("/")
def consultar_telemetria(limite: int=10, _: dict = Depends(obtener_usuario_actual)):
    """Endpoint para que el front reciba las últimas lecturas de los camiones"""
    if limite < 0 :
        # TODO: Decidir despues si para este caso emitir una excepcion o solo ignorar. Por ahora se ignora.
        # raise HTTPException(
        #    status_code=status.HTTP_400_BAD_REQUEST,
        #    detail=f"No existe un limite negativo"
        #)
        limite = 10

    return servicio.obtener_ultimas_lecturas(limite)

@router.get(
    "/dispositivo/{id_dispositivo}",
    response_model=List[TelemetriaRespuestaDTO],
    summary="Historial de telemetría del camión"
)
def obtener_historial_camion(id_dispositivo, limite:int = 10, _: dict = Depends(obtener_usuario_actual)):
    if limite < 0:
        #default
        limite = 10
    return servicio.obtener_ultimas_lecturas_byunidad(id_dispositivo, limite)

@router.get(
    "/dispositivo/{id_dispositivo}/ultima",
    response_model=TelemetriaRespuestaDTO,
    summary="Ultima lectura y ubicacion del camión"
)
def obtener_ultima_lectura_byunidad(id_dispositivo, _: dict = Depends(obtener_usuario_actual)):
    lectura = servicio.obtener_ultima_lectura_byunidad(id_dispositivo)
    if not lectura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron lecturas para el dispositivo {id_dispositivo}"
        )
    return lectura

@router.get(
    "/recientes",
    response_model=List[TelemetriaRespuestaDTO],
    summary="Historial general"
)
def obtener_historial_general(limite: int = 10, _: dict = Depends(obtener_usuario_actual)):
    if limite < 0:
        # default
        limite = 10
    return servicio.obtener_ultimas_lecturas(limite)