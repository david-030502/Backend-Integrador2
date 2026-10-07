import time
import random
import hashlib
import hmac
import secrets
import requests

from app.core.config import configuracion_hmac

# ==========================================
# CONFIGURACIÓN DEL SIMULADOR
# ==========================================
URL_API = "http://127.0.0.1:8000/api/telemetria/"
ID_DISPOSITIVO = "E0:8C:FE:77:6D:D0"
INTERVALO_ENVIO = 5  # Segundos entre paquetes

# Coordenadas sobre la Panamericana Sur (Chincha)
RUTA_GPS = [
    (-13.4080, -76.1320),
    (-13.4120, -76.1335),
    (-13.4152, -76.1348),
    (-13.4190, -76.1362),
    (-13.4235, -76.1379),
    (-13.4280, -76.1395),
    (-13.4330, -76.1412),
    (-13.4385, -76.1430),
    (-13.4440, -76.1450),
    (-13.4500, -76.1472),
]


def simular_telemetria():

    print("=" * 65)
    print("SIMULADOR IoT INICIADO - MONITOREO AVÍCOLA LOS ANDES")
    print(f"Endpoint: {URL_API}")
    print(f"Dispositivo: {ID_DISPOSITIVO}")
    print(f"Frecuencia: Cada {INTERVALO_ENVIO} segundos")
    print("=" * 65)

    indice_ruta = 0
    batch_id = 1

    while True:
        try:
            timestamp_actual = int(time.time())

            lat, lon = RUTA_GPS[indice_ruta]
            indice_ruta = (indice_ruta + 1) % len(RUTA_GPS)

            # ==========================================
            # VALORES NORMALES
            # ==========================================
            temperatura = round(random.uniform(32.5, 35.0), 1)
            humedad = round(random.uniform(61.0, 65.0), 1)
            gases = round(random.uniform(100.0, 200.0), 1)

            # ==========================================
            # ALERTAS
            # ==========================================
            alerts = []

            # Cada 3 paquetes generamos una alerta
            if batch_id % 3 == 0:

                # Alerta de temperatura baja
                temperatura = round(random.uniform(27.0, 31.0), 1)

                alerts.append({
                    "sensor": "dht22_temp",
                    "type": "temp_low",
                    "threshold": 32.0,
                    "value": temperatura,
                    "t": timestamp_actual
                })

            # Cada 5 paquetes generamos una alerta de humedad
            if batch_id % 5 == 0:

                humedad = round(random.uniform(55.0, 59.9), 1)

                alerts.append({
                    "sensor": "dht22_hum",
                    "type": "hum_low",
                    "threshold": 60.0,
                    "value": humedad,
                    "t": timestamp_actual
                })

            # Cada 7 paquetes generamos una alerta de gases
            if batch_id % 7 == 0:

                gases = round(random.uniform(301.0, 400.0), 1)

                alerts.append({
                    "sensor": "mq135_raw",
                    "type": "gas_high",
                    "threshold": 300.0,
                    "value": gases,
                    "t": timestamp_actual
                })

            # ==========================================
            # PAYLOAD ACTUAL
            # ==========================================
            payload = {
                "device_id": ID_DISPOSITIVO,
                "schema_version": 1,
                "batch_id": batch_id,
                "sent_at": timestamp_actual,
                "nonce": secrets.randbits(32),

                "readings": [
                    {
                        "sensor": "dht22_temp",
                        "t": timestamp_actual,
                        "v": temperatura
                    },
                    {
                        "sensor": "dht22_hum",
                        "t": timestamp_actual,
                        "v": humedad
                    },
                    {
                        "sensor": "mq135_raw",
                        "t": timestamp_actual,
                        "v": gases
                    }
                ],

                "gps": [
                    {
                        "t": timestamp_actual,
                        "lat": lat,
                        "lon": lon,
                        "speed": 45.0,
                        "alt": 150.0,
                        "fix": 1
                    }
                ],

                "alerts": alerts
            }

            firma_canonica = "|".join(
                (
                    payload["device_id"],
                    str(payload["nonce"]),
                    str(timestamp_actual),
                    str(int(temperatura * 10)),
                    str(int(humedad * 10)),
                    str(int(gases)),
                )
            )
            payload["signature"] = hmac.new(
                configuracion_hmac.secret.encode("utf-8"),
                firma_canonica.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            # ==========================================
            # ENVIAR AL BACKEND
            # ==========================================
            respuesta = requests.post(
                URL_API,
                json=payload,
                timeout=5
            )

            if respuesta.status_code in (200, 201):

                hora_str = time.strftime("%H:%M:%S")

                print(
                    f"[{hora_str}] "
                    f"Batch #{batch_id} | "
                    f"Temp: {temperatura}°C | "
                    f"Hum: {humedad}% | "
                    f"Gases: {gases} ppm | "
                    f"Alertas: {len(alerts)}"
                )

                if alerts:
                    for alerta in alerts:
                        print(
                            f"   ⚠️ {alerta['type']} | "
                            f"{alerta['sensor']} | "
                            f"Valor: {alerta['value']} | "
                            f"Umbral: {alerta['threshold']}"
                        )

                batch_id += 1

            else:
                print(
                    f"Error {respuesta.status_code}: "
                    f"{respuesta.text}"
                )

        except requests.exceptions.ConnectionError:
            print("No se pudo conectar con FastAPI.")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(INTERVALO_ENVIO)


if __name__ == "__main__":
    simular_telemetria()