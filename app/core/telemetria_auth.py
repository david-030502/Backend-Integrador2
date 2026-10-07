import hashlib
import hmac
import threading
import time

from app.core.config import configuracion_hmac
from app.dto.TelemetriaDTO import TelemetriaLoteEntradaDTO


TIEMPO_VIGENCIA_NONCE_SEGUNDOS = 15 * 60
_nonces_vistos: dict[tuple[str, int], float] = {}
_bloqueo_nonces = threading.Lock()


def _construir_mensaje_canonico(payload: TelemetriaLoteEntradaDTO) -> str:
    lecturas = {lectura.sensor: lectura for lectura in payload.readings}
    try:
        temperatura = lecturas["dht22_temp"]
        humedad = lecturas["dht22_hum"]
        gases = lecturas["mq135_raw"]
    except KeyError as error:
        raise ValueError(f"Falta lectura requerida para autenticar: {error.args[0]}") from error

    return "|".join(
        (
            payload.device_id,
            str(payload.nonce),
            str(temperatura.t),
            str(int(temperatura.v * 10)),
            str(int(humedad.v * 10)),
            str(int(gases.v)),
        )
    )


def verificar_firma(payload: TelemetriaLoteEntradaDTO) -> bool:
    mensaje = _construir_mensaje_canonico(payload).encode("utf-8")
    esperado = hmac.new(
        configuracion_hmac.secret.encode("utf-8"),
        mensaje,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(esperado, payload.signature.lower())


def reservar_nonce(payload: TelemetriaLoteEntradaDTO) -> bool:
    ahora = time.monotonic()
    clave = (payload.device_id, payload.nonce)
    with _bloqueo_nonces:
        expirados = [
            nonce
            for nonce, vencimiento in _nonces_vistos.items()
            if vencimiento <= ahora
        ]
        for nonce in expirados:
            del _nonces_vistos[nonce]
        if clave in _nonces_vistos:
            return False
        _nonces_vistos[clave] = ahora + TIEMPO_VIGENCIA_NONCE_SEGUNDOS
        return True
