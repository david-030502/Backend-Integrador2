from datetime import datetime

from sqlalchemy import select, func

from app.core.database import obtener_sesion
from app.entidades.Alerta import Alerta
from app.entidades.Telemetria import Telemetria
from app.entidades.Dispositivo import Dispositivo


class AlertaRepositorio:
    def guardar(self, alerta):
        with obtener_sesion() as sesion:
            sesion.add(alerta)
            sesion.flush()
        return alerta

    def obtener_alertas_recientes(self, pagina=1, limite=10):
        with obtener_sesion() as sesion:
            offset = (pagina - 1) * limite

            resultado = sesion.execute(
                select(Alerta, Telemetria, Dispositivo)
                .join(
                    Telemetria,
                    Alerta.id_lectura == Telemetria.id_lectura
                )
                .join(
                    Dispositivo,
                    Telemetria.id_dispositivo == Dispositivo.id_dispositivo
                )
                .order_by(Alerta.fecha_hora.desc())
                .offset(offset)
                .limit(limite)
            )

            alertas = []

            for alerta, telemetria, dispositivo in resultado.all():
                alerta.id_dispositivo = dispositivo.id_dispositivo
                alerta.placa = dispositivo.placa
                alertas.append(alerta)

            total = sesion.execute(
                select(func.count()).select_from(Alerta)
            ).scalar_one()

            return alertas, total

    def atender_alerta(self, id_alerta, id_usuario):
        with obtener_sesion() as sesion:
            resultado = sesion.execute(
                select(Alerta, Telemetria, Dispositivo)
                .join(
                    Telemetria,
                    Alerta.id_lectura == Telemetria.id_lectura
                )
                .join(
                    Dispositivo,
                    Telemetria.id_dispositivo == Dispositivo.id_dispositivo
                )
                .where(Alerta.id_alerta == id_alerta)
            )

            registro = resultado.first()

            if not registro:
                return None

            alerta, telemetria, dispositivo = registro

            alerta.fecha_vista = datetime.now()
            alerta.id_usuario = id_usuario

            sesion.flush()

            alerta.id_dispositivo = dispositivo.id_dispositivo
            alerta.placa = dispositivo.placa

            return alerta