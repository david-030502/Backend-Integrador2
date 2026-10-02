from sqlalchemy import select

from app.core.database import obtener_sesion
from app.entidades.Dispositivo import Dispositivo


class DispositivoRepositorio:
    def guardar(self, dispositivo):
        with obtener_sesion() as sesion:
            sesion.add(dispositivo)
            sesion.flush()
        return dispositivo

    def obtener_byplaca(self, placa):
        with obtener_sesion() as sesion:
            resultado = sesion.execute(
                select(Dispositivo).where(Dispositivo.placa == placa)
            )
            return resultado.scalar_one_or_none()

    def obtener_byid(self, id_dispositivo):
        with obtener_sesion() as sesion:
            return sesion.get(Dispositivo, id_dispositivo)

    def actualizar(self, id_dispositivo, cambios):
        with obtener_sesion() as sesion:
            dispositivo = sesion.get(Dispositivo, id_dispositivo)
            if not dispositivo:
                return None
            for campo, valor in cambios.items():
                setattr(dispositivo, campo, valor)
            sesion.flush()
            return dispositivo

    def obtener_bymac(self, mac):
        with obtener_sesion() as sesion:
            resultado = sesion.execute(
                select(Dispositivo).where(Dispositivo.mac == mac)
            )
            return resultado.scalar_one_or_none()

    def listar_dispositivos(self):
        with obtener_sesion() as sesion:
            resultado = sesion.execute(select(Dispositivo))
            return resultado.scalars().all()
