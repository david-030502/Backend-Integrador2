from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.dto.AlertaDTO import AlertaRespuestaDTO, AlertasPaginadasDTO
from app.servicios.AlertaService import AlertaService

from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/alertas", tags=["Alertas"])
servicio = AlertaService()

@router.get("/", response_model=AlertasPaginadasDTO)
def listar_alertas(pagina: int = 1, limite: int = 10, _: dict = Depends(obtener_usuario_actual)):
    if pagina < 1:
        pagina = 1

    if limite < 1:
        limite = 10

    elif limite > 50:
        limite = 50

    alertas, total = servicio.listar_alertas_recientes(pagina, limite)

    total_paginas = (total + limite - 1) // limite

    return {
        "alertas": alertas,
        "pagina": pagina,
        "limite": limite,
        "total": total,
        "total_paginas": total_paginas
    }

@router.put(
    "/{id_alerta}/atender",
    response_model=AlertaRespuestaDTO,
    summary="Marcar alerta como atendida",
)
def atender_alerta(id_alerta:int,
                   usuario: dict = Depends(obtener_usuario_actual)):
    alerta_atendida = servicio.atender_alerta(id_alerta, usuario["id_usuario"])
    if not alerta_atendida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La alerta con ID {id_alerta} no existe",
        )
    return alerta_atendida