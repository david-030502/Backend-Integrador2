from app.entidades.Dispositivo import Dispositivo
from app.repositorios.DispositivoRepositorio import DispositivoRepositorio

class DispositivoService:
    def __init__(self):
        self.repositorio = DispositivoRepositorio()

    def registrar_dispositivo(self, datos):
        placa_corregida = datos.placa.strip().upper()
        dispositivo_existente = self.repositorio.obtener_byplaca(placa_corregida)
        if dispositivo_existente:
            raise ValueError(f"El dispositivo del camión {placa_corregida} ya está registrado")
        entidad = Dispositivo(
            placa = placa_corregida,
            nombre_chofer= datos.nombre_chofer.strip(),
            estado = datos.estado.strip(),
        )
        return self.repositorio.guardar(entidad)

    def obtener_byid(self, id_dispositivo):
        return self.repositorio.obtener_byid(id_dispositivo)

    def actualizar_dispositivo(self, id_dispositivo, datos):
        cambios = datos.model_dump(exclude_unset=True)
        if not cambios:
            raise ValueError("Debe enviar al menos un campo para actualizar")

        if any(valor is None for valor in cambios.values()):
            #raise ValueError("Los campos enviados no pueden ser nulos")
            # Por ahora lo dejo como si los campos son nulos, no hacer nada.
            return None

        if "placa" in cambios:
            cambios["placa"] = cambios["placa"].strip().upper()
            dispositivo_existente = self.repositorio.obtener_byplaca(cambios["placa"])
            if (
                dispositivo_existente
                and dispositivo_existente.id_dispositivo != id_dispositivo
            ):
                raise ValueError(
                    f"El dispositivo del camión {cambios['placa']} ya está registrado"
                )
        if "nombre_chofer" in cambios:
            cambios["nombre_chofer"] = cambios["nombre_chofer"].strip()
        if "estado" in cambios:
            cambios["estado"] = cambios["estado"].strip()

        return self.repositorio.actualizar(id_dispositivo, cambios)

    def obtener_dispositivo_bymac(self, mac: str):
        mac_limpio = mac.strip()
        return self.repositorio.obtener_bymac(mac_limpio)

    def registrar_dispositivo_bymac(self, mac: str):
        mac_limpio = mac.strip()
        entidad = Dispositivo(
            mac = mac_limpio,
            placa = "",
            nombre_chofer = "Pendiente",
            estado = "Activo",
        )
        return self.repositorio.guardar(entidad)

    def listar_dispositivos(self):
        return self.repositorio.listar_dispositivos()