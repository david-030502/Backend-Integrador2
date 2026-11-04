import pytest

from app.dto.UsuarioDTO import UsuarioCrearDTO
from app.servicios.UsuarioService import UsuarioService


ADMIN = {
    "nombre": "Admin Test",
    "email": "admin@test.com",
    "contrasena": "Password123",
    "rol": "admin",
}


@pytest.fixture
def token_admin(cliente):
    UsuarioService().registrar_usuario(UsuarioCrearDTO(**ADMIN))
    respuesta = cliente.post(
        "/api/usuarios/login",
        json={"email": ADMIN["email"], "contrasena": ADMIN["contrasena"]},
    )
    assert respuesta.status_code == 200
    return respuesta.json()["access_token"]


def test_endpoint_protegido_sin_token_devuelve_401(cliente):
    respuesta = cliente.get("/api/telemetria/")
    assert respuesta.status_code == 401


def test_login_entrega_token(cliente):
    UsuarioService().registrar_usuario(UsuarioCrearDTO(**ADMIN))
    respuesta = cliente.post(
        "/api/usuarios/login",
        json={"email": ADMIN["email"], "contrasena": ADMIN["contrasena"]},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["access_token"]
    assert datos["rol"] == "admin"


def test_login_credenciales_invalidas(cliente):
    UsuarioService().registrar_usuario(UsuarioCrearDTO(**ADMIN))
    respuesta = cliente.post(
        "/api/usuarios/login",
        json={"email": ADMIN["email"], "contrasena": "PasswordIncorrecta1"},
    )
    assert respuesta.status_code == 401


def test_admin_puede_registrar_usuario(cliente, token_admin):
    respuesta = cliente.post(
        "/api/usuarios/register",
        json={
            "nombre": "Operador",
            "email": "operador@test.com",
            "contrasena": "Password123",
            "rol": "operador",
        },
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert respuesta.status_code == 201


def test_operador_no_puede_registrar(cliente, token_admin):
    cliente.post(
        "/api/usuarios/register",
        json={
            "nombre": "Operador",
            "email": "operador@test.com",
            "contrasena": "Password123",
            "rol": "operador",
        },
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    login = cliente.post(
        "/api/usuarios/login",
        json={"email": "operador@test.com", "contrasena": "Password123"},
    )
    token_operador = login.json()["access_token"]
    respuesta = cliente.post(
        "/api/usuarios/register",
        json={
            "nombre": "Otro",
            "email": "otro@test.com",
            "contrasena": "Password123",
            "rol": "operador",
        },
        headers={"Authorization": f"Bearer {token_operador}"},
    )
    assert respuesta.status_code == 403
