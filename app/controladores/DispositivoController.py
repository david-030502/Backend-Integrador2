from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.dto.DispositivoDTO import (
    DispositivoActualizarDTO,
    DispositivoCrearDTO,
    DispositivoRespuestaDTO,
)
from app.servicios.DispositivoService import DispositivoService

from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/dispositivos", tags=["Dispositivos"])
servicio = DispositivoService()

@router.post(
    "/register",
    response_model=DispositivoRespuestaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo dispositivo",
    )
def registrar_dispositivo(datos:DispositivoCrearDTO, _: dict = Depends(obtener_usuario_actual)):
    try:
        dispositivo = servicio.registrar_dispositivo(datos)
        return dispositivo
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

@router.get(
    "/",
    response_model=List[DispositivoRespuestaDTO],
    summary="Listar dispositivos registrados"
)
def listar_dispositivos(_: dict = Depends(obtener_usuario_actual)):
    return servicio.listar_dispositivos()

@router.get(
    "/{id_dispositivo}",
    response_model=DispositivoRespuestaDTO,
    summary="Buscar por id",
)
def obtener_byid(id_dispositivo, _: dict = Depends(obtener_usuario_actual)):
    dispositivo = servicio.obtener_byid(id_dispositivo)
    if not dispositivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {id_dispositivo} no encontrado"
        )
    return dispositivo

@router.put(
    "/{id_dispositivo}",
    response_model=DispositivoRespuestaDTO,
    summary="Actualizar parcialmente un dispositivo",
)
def actualizar_dispositivo(
    id_dispositivo: int,
    datos: DispositivoActualizarDTO,
    _: dict = Depends(obtener_usuario_actual),
):
    try:
        dispositivo = servicio.actualizar_dispositivo(id_dispositivo, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    if not dispositivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {id_dispositivo} no encontrado",
        )
    return dispositivo