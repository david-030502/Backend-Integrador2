def test_inicio(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()


def test_openapi(cliente):
    respuesta = cliente.get("/openapi.json")
    assert respuesta.status_code == 200
    assert respuesta.json()["info"]["title"] == "Monitoreo Avícola Los Andes"
