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
        temperatura = 0.0
        humedad = 0.0
        gases = 0.0

        for lectura in lote.readings:
            if lectura.sensor == "dht22_temp":
                temperatura = lectura.v
            elif lectura.sensor == "dht22_hum":
                humedad = lectura.v
            elif lectura.sensor == "mq135_raw":
                gases = lectura.v

        latitud = 0.0
        longitud = 0.0
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
                # Cambiar el formato a gusto, yo considero que es lo que deberia ponerse en la bd, tiene todos los campos
                # que el esp32 envia como procesador de alertas.
                # El frontend utiliza tipo_alerta para mostrarlo como mensaje descriptivo, cosa que rompe este esquema.
                # Evalua crear otro campo descripcion en telemetria para enviar al front.
                # Te dejo un ejemplo basico, por si lo quieres implementar.
                """
                    descripcion: str = "Error desconocido"
                    switch(alerta.sensor):
                        case "dht_22_temp":
                            if alerta.type == "temp_low": 
                                descripcion = "Temperatura crítica alta."
                            else:
                                descripcion = "Temperatura crítica baja."
                        case "dht_22_hum":
                            if alerta.type == "hum_low":
                                descripcion = "Humedad crítica baja."
                            else:
                                descripcion = "Humedad crítica alta."
                        case "mq135_raw":
                            if alerta.type == "gas_high":
                                descripcion = "Concentración de gases crítica"
                        case "esp_now":
                            descripcion = "No hay comunicacion de los sensores."
                            
                       / ... /     
                    alerta.descripcion = descripcion
                    alertas_guardaras.append(self.alerta_repositorio.guardar(...))       
                """
                tipo_alerta = (
                    f"{alerta.type}: {alerta.sensor} "
                    f"(valor={alerta.value}, umbral={alerta.threshold})"
                )
                alertas_guardadas.append(
                    self.alerta_repositorio.guardar(
                        Alerta(
                            tipo_alerta=tipo_alerta,
                            id_lectura=telemetria_guardado.id_lectura,
                        )
                    )
                )
        # Mantengo el bloque manual de generacion de alertas comentando, si se necesita en un futuro o como ejemplo.

        # else:
        #     tipo_alerta = None
        #     if temperatura > 32.0:
        #         tipo_alerta = f"Alerta: Calor crítico ({temperatura}°C)"
        #     elif temperatura < 12.0:
        #         tipo_alerta = f"Alerta: Temperatura baja ({temperatura}°C)"
        #     elif gases > 300:
        #         tipo_alerta = f"Concentracion alta de gases ({gases} ppm)"
        #
        #     if tipo_alerta:
        #         alertas_guardadas.append(
        #             self.alerta_repositorio.guardar(
        #                 Alerta(
        #                     tipo_alerta=tipo_alerta,
        #                     id_lectura=telemetria_guardado.id_lectura,
        #                 )
        #             )
        #         )

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