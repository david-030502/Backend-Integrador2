import hashlib
import hmac
import secrets
import time

from app.core.config import configuracion_hmac


def _firmar(payload):
    lecturas = {lectura["sensor"]: lectura for lectura in payload["readings"]}
    temperatura = lecturas["dht22_temp"]
    humedad = lecturas["dht22_hum"]
    gases = lecturas["mq135_raw"]
    mensaje = "|".join(
        (
            payload["device_id"],
            str(payload["nonce"]),
            str(temperatura["t"]),
            str(int(temperatura["v"] * 10)),
            str(int(humedad["v"] * 10)),
            str(int(gases["v"])),
        )
    )
    return hmac.new(
        configuracion_hmac.secret.encode("utf-8"),
        mensaje.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _payload(device_id="E0:8C:FE:77:6D:D0", batch_id=1, nonce=None):
    if nonce is None:
        nonce = secrets.randbits(32)
    ahora = int(time.time())
    payload = {
        "device_id": device_id,
        "schema_version": 1,
        "batch_id": batch_id,
        "sent_at": ahora,
        "nonce": nonce,
        "readings": [
            {"sensor": "dht22_temp", "t": ahora, "v": 33.5},
            {"sensor": "dht22_hum", "t": ahora, "v": 60.0},
            {"sensor": "mq135_raw", "t": ahora, "v": 150.0},
        ],
        "gps": [
            {
                "t": ahora,
                "lat": -13.4080,
                "lon": -76.1320,
                "speed": 45.0,
                "alt": 150.0,
                "fix": 1,
            }
        ],
        "alerts": [],
    }
    payload["signature"] = _firmar(payload)
    return payload


def test_telemetria_valida(cliente):
    respuesta = cliente.post("/api/telemetria/", json=_payload())
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["mensaje"] == "Lote procesado exitosamente"
    assert "id_lectura" in cuerpo


def test_telemetria_firma_invalida(cliente):
    payload = _payload()
    payload["signature"] = "0" * 64
    respuesta = cliente.post("/api/telemetria/", json=payload)
    assert respuesta.status_code == 401


def test_telemetria_nonce_repetido(cliente):
    payload = _payload()
    assert cliente.post("/api/telemetria/", json=payload).status_code == 201
    assert cliente.post("/api/telemetria/", json=payload).status_code == 401


def test_telemetria_con_alerta(cliente):
    payload = _payload()
    # Las alertas no forman parte de la firma canónica, por lo que la firma sigue siendo válida.
    payload["alerts"] = [
        {
            "sensor": "dht22_temp",
            "type": "temp_high",
            "threshold": 30.0,
            "value": 33.5,
            "t": int(time.time()),
        }
    ]
    respuesta = cliente.post("/api/telemetria/", json=payload)
    assert respuesta.status_code == 201
    assert respuesta.json()["alerta_generada"]["id_alerta"] is not None
