from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.dto.UsuarioDTO import (
    UsuarioCrearDTO,
    UsuarioRespuestaDTO,
    LoginDTO,
    LoginRespuestaDTO,
)
from app.servicios.UsuarioService import UsuarioService
from app.core.seguridad import crear_token_acceso
from app.core.auth import obtener_usuario_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
servicio = UsuarioService()

@router.post(
    "/register",
    response_model=UsuarioRespuestaDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
)
def registrar_usuario(datos:UsuarioCrearDTO, usuario_actual:dict=Depends(obtener_usuario_actual),):
    if usuario_actual["rol"].lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el administrador puede registrar usuarios",
        )
    try:
        usuario = servicio.registrar_usuario(datos)
        return usuario
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

@router.post(
    "/login",
    response_model=LoginRespuestaDTO,
    summary="Iniciar sesión y obtener token JWT",
)
def login(credenciales:LoginDTO):
    try:
        usuario_autenticado = servicio.autenticar_usuario(credenciales)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
    token = crear_token_acceso(usuario_autenticado)
    return LoginRespuestaDTO(
        access_token=token,
        **usuario_autenticado,
    )

@router.get(
    "/auth",
    response_model=UsuarioRespuestaDTO,
    summary="Obtener los datos del usuario autenticado",
)
def obtener_usuario(
    datos_usuario: dict = Depends(obtener_usuario_actual),
):
    return {
        "id_usuario": int(datos_usuario["id_usuario"]),
        "nombre": datos_usuario["nombre"],
        "email": datos_usuario["email"],
        "rol": datos_usuario["rol"],
    }

@router.get(
    "/{id_usuario}",
    response_model=UsuarioRespuestaDTO,
    summary="Buscar usuario por ID",
)
def buscar_byid(id_usuario, _ : dict = Depends(obtener_usuario_actual)):
    usuario = servicio.obtener_byid(id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {id_usuario} no encontrado"
        )
    return usuario

@router.get(
    "/",
    response_model=List[UsuarioRespuestaDTO],
    summary= f"Obtiene todos los usuarios de la base de datos",
)
def listar_usuarios(_: dict = Depends(obtener_usuario_actual)):
    usuarios = servicio.listar_usuarios()
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha podido listar los usuarios"
        )
    return usuarios
