import time
import requests

URL = "http://127.0.0.1:8000/docs"

duracion = 10 * 60
intervalo = 5

inicio = time.time()
exitosas = 0
fallidas = 0

while time.time() - inicio < duracion:
    try:
        respuesta = requests.get(URL, timeout=3)

        if respuesta.status_code == 200:
            exitosas += 1
            print(f"✓ Prueba {exitosas + fallidas}: Backend disponible")
        else:
            fallidas += 1
            print(
                f"✗ Prueba {exitosas + fallidas}: "
                f"Error HTTP {respuesta.status_code}"
            )

    except requests.exceptions.RequestException as e:
        fallidas += 1
        print(f"✗ Prueba {exitosas + fallidas}: Backend no disponible")

    time.sleep(intervalo)

total = exitosas + fallidas
disponibilidad = (exitosas / total) * 100

print("\n========== RESULTADO RNF-02 ==========")
print(f"Pruebas realizadas: {total}")
print(f"Respuestas exitosas: {exitosas}")
print(f"Respuestas fallidas: {fallidas}")
print(f"Disponibilidad: {disponibilidad:.2f}%")