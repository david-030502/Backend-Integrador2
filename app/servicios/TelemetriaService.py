from app.dto.TelemetriaDTO import TelemetriaLoteEntradaDTO
from app.entidades.Telemetria import Telemetria
from app.repositorios.TelemetriaRepositorio import TelemetriaRepositorio
from app.entidades.Alerta import Alerta
from app.repositorios.AlertaRepositorio import AlertaRepositorio

class TelemetriaService:
    def __init__(self):
        self.telemetria_repositorio = TelemetriaRepositorio()
        self.alerta_repositorio = AlertaRepositorio()

    def procesar_lote_telemetria(self, lote:TelemetriaLoteEntradaDTO, id_dispositivo:int):
        temperatura = None
        humedad = None
        gases = None

        for lectura in lote.readings:
            if lectura.sensor == "dht22_temp":
                temperatura = lectura.v
            elif lectura.sensor == "dht22_hum":
                humedad = lectura.v
            elif lectura.sensor == "mq135_raw":
                gases = lectura.v

        latitud = None
        longitud = None
        if lote.gps:
            ultima_coordenada = lote.gps[-1]
            latitud = ultima_coordenada.lat
            longitud = ultima_coordenada.lon

        entidad_telemetria = Telemetria(
            temperatura = temperatura,
            humedad = humedad,
            gases = gases,
            latitud = latitud,
            longitud = longitud,
            id_dispositivo = id_dispositivo,
        )

        #Guardar en bd
        telemetria_guardado = self.telemetria_repositorio.guardar(entidad_telemetria)

        alertas_guardadas = []
        if lote.alerts:
            for alerta in lote.alerts:
                tipo_alerta = alerta.type
                if alerta.type == "temp_low":
                    descripcion = (
                        f"Temperatura crítica baja "
                        f"(Valor={alerta.value}, umbral={alerta.threshold})"
                    )
                elif alerta.type == "temp_high":
                    descripcion = (
                        f"Temperatura crítica alta "
                        f"(Valor={alerta.value}, umbral={alerta.threshold})"
                    )
                elif alerta.type == "hum_low":
                    descripcion = (
                        f"Humedad crítica baja "
                        f"(Valor={alerta.value}, umbral={alerta.threshold})"
                    )
                elif alerta.type == "hum_high":
                    descripcion = (
                        f"Humedad crítica alta "
                        f"(Valor={alerta.value}, umbral={alerta.threshold})"
                    )
                elif alerta.type == "gas_high":
                    descripcion = (
                        f"Concentración de gases crítica "
                        f"(Valor={alerta.value}, umbral={alerta.threshold})"
                    )
                else:
                    descripcion = (
                        f"Alerta detectada en {alerta.sensor}"
                        f"(valor={alerta.value}, umbral={alerta.threshold})"
                    )
                alertas_guardadas.append(
                    self.alerta_repositorio.guardar(
                        Alerta(
                            tipo_alerta = tipo_alerta,
                            descripcion = descripcion,
                            id_lectura = telemetria_guardado.id_lectura,
                        )
                    )
                )

        return{
            "mensaje":"Lote procesado exitosamente",
            "id_lectura":telemetria_guardado.id_lectura,
            "dispositivo":telemetria_guardado.id_dispositivo,
            "fecha_registro":telemetria_guardado.fecha_hora,
            "alerta_generada":{
                "id_alerta":(
                    alertas_guardadas[0].id_alerta
                    if alertas_guardadas
                    else None
                ),
                "tipo":(
                    alertas_guardadas[0].tipo_alerta
                    if alertas_guardadas
                    else None
                ),
            },  
            "alertas_generadas":[
                {
                    "id_alerta":alerta.id_alerta,
                    "tipo":alerta.tipo_alerta,
                }
                for alerta in alertas_guardadas
            ],
        }

    def obtener_ultimas_lecturas (self, limite: int=10):
        "Consulta el repositorio para traer las ultimas lecturas registradas."
        return self.telemetria_repositorio.obtener_ultimas_lecturas(limite)

    def obtener_ultimas_lecturas_byunidad(self, id_dispositivo, limite:int=50):
        return self.telemetria_repositorio.obtener_ultimas_lecturas_byunidad(id_dispositivo, limite)

    def obtener_ultima_lectura_byunidad(self, id_dispositivo):
        return self.telemetria_repositorio.obtener_ultima_lectura_byunidad(id_dispositivo)