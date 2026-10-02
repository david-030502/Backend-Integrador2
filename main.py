from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controladores import TelemetriaController, AlertaController, UsuarioController, DispositivoController
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield

#App principal
app = FastAPI(
    title = "Monitoreo Avícola Los Andes",
    description = "API IoT para el monitoreo de aves durante el transporte",
    version = "1.0.0",
    lifespan=lifespan,
)

#Configuracion de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "https://www.losandes.smashiv.com",
                   "https://losandes.smashiv.com",
                   "https://smashiv.com",
                   "https://www.smashiv.com",
                   # TODO: agregar aca despues la ip del servidor.
                   ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

#Conectar el controlador 
app.include_router(TelemetriaController.router, prefix="/api")
app.include_router(AlertaController.router, prefix="/api" )
app.include_router(UsuarioController.router, prefix="/api")
app.include_router(DispositivoController.router, prefix="/api")

@app.get("/")
def inicio():
    return{
        "mensaje" : "Servidor Monitoreo IoT",
        "documentacion" : "/docs"
    }
