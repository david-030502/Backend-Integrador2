from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Alerta(Base):
    __tablename__ = "alertas"
    __mapper_args__ = {"eager_defaults": True}

    id_alerta: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_alerta: Mapped[str] = mapped_column(String(60))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    fecha_vista: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    id_lectura: Mapped[int] = mapped_column(ForeignKey("telemetria.id_lectura"))
    id_usuario: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    descripcion: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
