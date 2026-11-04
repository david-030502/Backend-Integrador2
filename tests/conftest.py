import os

os.environ.setdefault("DB_USER", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "db_senavi_test")
os.environ.setdefault("JWT_SECRET", "test_jwt_secret_0123456789abcdef0123456789abcdef")
os.environ.setdefault("SENAVI_HMAC_SECRET", "test_hmac_secret_0123456789abcdef0123456789abcdef")

import psycopg2
import pytest
from fastapi.testclient import TestClient
from psycopg2 import sql

from app.core.config import settings
from app.core.database import Base, engine

import app.entidades  # noqa: F401


def _crear_base_si_no_existe():
    try:
        conexion = psycopg2.connect(
            dbname="postgres",
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
        )
    except psycopg2.OperationalError as error:
        raise RuntimeError(
            "No se pudo conectar a PostgreSQL para crear la base de tests. "
            "Verificá que PostgreSQL esté corriendo y que DB_USER/DB_PASSWORD/DB_HOST/DB_PORT "
            "apunten a un usuario con permisos CREATEDB (o creá 'db_senavi_test' a mano)."
        ) from error

    conexion.autocommit = True
    cursor = conexion.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.db_name,))
    if cursor.fetchone() is None:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(settings.db_name)))
    cursor.close()
    conexion.close()


@pytest.fixture(scope="session")
def preparar_base():
    _crear_base_si_no_existe()


@pytest.fixture(autouse=True)
def base_limpia(preparar_base):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def cliente():
    from main import app

    with TestClient(app) as client:
        yield client
