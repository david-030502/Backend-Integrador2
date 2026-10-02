from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id_dispositivo: Mapped[int] = mapped_column(Integer, primary_key=True)
    placa: Mapped[str] = mapped_column(String(7))
    nombre_chofer: Mapped[str] = mapped_column(String(70))
    estado: Mapped[str] = mapped_column(String(20), default="Activo")
    mac: Mapped[Optional[str]] = mapped_column(String(17), unique=True, nullable=True)
