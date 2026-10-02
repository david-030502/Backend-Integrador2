import time
import random
import requests

# ==========================================
# CONFIGURACIÓN DEL SIMULADOR
# ==========================================
URL_API = "http://127.0.0.1:8000/api/telemetria/"
ID_DISPOSITIVO = 1
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
    print(f"Unidad ID: {ID_DISPOSITIVO}")
    print(f"Frecuencia: Cada {INTERVALO_ENVIO} segundos")
    print("=" * 65)

    temp_base = 22.0
    hum_base = 65.0
    gas_base = 120.0  # Normal < 300
    indice_ruta = 0
    batch_id = 1

    while True:
        try:
            timestamp_actual = int(time.time())
            lat, lon = RUTA_GPS[indice_ruta]
            indice_ruta = (indice_ruta + 1) % len(RUTA_GPS)

            # Variación natural
            temperatura = round(temp_base + random.uniform(-0.5, 0.5), 1)
            humedad = round(hum_base + random.uniform(-1.0, 1.0), 1)
            gases = round(gas_base + random.uniform(-3.0, 3.0), 1)

            payload = {
                "device_id": ID_DISPOSITIVO,
                "schema_version": 1,
                "batch_id": batch_id,
                "sent_at": timestamp_actual,
                "readings": [
                    {"sensor": "dht22_temp", "t": timestamp_actual, "v": temperatura},
                    {"sensor": "dht22_hum", "t": timestamp_actual, "v": humedad},
                    {"sensor": "mq135_raw", "t": timestamp_actual, "v": gases}
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
                "alerts": []
            }

            respuesta = requests.post(URL_API, json=payload, timeout=5)

            if respuesta.status_code in (200, 201):
                hora_str = time.strftime("%H:%M:%S")
                print(f"[{hora_str}] Batch #{batch_id} | Temp: {temperatura}°C | Hum: {humedad}% | Gases: {gases} ppm | Lat: {lat:.4f}, Lon: {lon:.4f}")
                batch_id += 1
            else:
                print(f"Error {respuesta.status_code}: {respuesta.text}")

        except requests.exceptions.ConnectionError:
            print("No se pudo conectar con FastAPI.")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(INTERVALO_ENVIO)

if __name__ == "__main__":
    simular_telemetria()