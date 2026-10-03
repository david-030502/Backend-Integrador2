import hmac

from pwdlib.exceptions import PwdlibError
from datetime import datetime, timedelta, timezone
from app.core.seguridad import password_hash
from app.dto.UsuarioDTO import UsuarioCrearDTO
from app.entidades.Usuario import Usuario
from app.repositorios.UsuarioRepositorio import UsuarioRepositorio

class UsuarioService:
    def __init__(self):
        self.repositorio = UsuarioRepositorio()

    def registrar_usuario(self, datos:UsuarioCrearDTO):
        usuario_existente = self.repositorio.obtener_byemail(datos.email)
        if usuario_existente:
            raise ValueError(
                f"El correo '{datos.email}' ya se encuentra registrado"
            )

        #Validar contraseña
        if not any(c.isalpha() for c in datos.contrasena) or not any(c.isdigit() for c in datos.contrasena):
            raise ValueError("La contraseña debe tener letras y numeros")
        
        entidad = Usuario(
            nombre = datos.nombre,
            email = datos.email,
            contrasena = password_hash.hash(datos.contrasena),
            rol = datos.rol,
        )
        return self.repositorio.guardar(entidad)

    def eliminar_usuario(self, id_usuario):
        return self.repositorio.eliminar(id_usuario)

    def obtener_byid(self, id_usuario):
        return self.repositorio.obtener_byid(id_usuario)

    def listar_usuarios(self):
        return self.repositorio.listar_usuarios()

    def autenticar_usuario(self, datos):
        usuario = self.repositorio.obtener_byemail(datos.email)
        if not usuario:
            raise ValueError("Credenciales inválidas")

        #verificar si la cuenta está bloqueada
        ahora = datetime.now(timezone.utc)
        if usuario.bloqueado_hasta and usuario.bloqueado_hasta > ahora:
            raise ValueError(
                "Cuenta bloqueda temporalmente. Intente más tarde"
            )

        try:
            contrasena_valida = password_hash.verify(datos.contrasena, usuario.contrasena)
        except PwdlibError:
            contrasena_valida = hmac.compare_digest(
                datos.contrasena,
                usuario.contrasena,
            )
            if contrasena_valida:
                self.repositorio.actualizar_contrasena(
                    usuario.id_usuario,
                    password_hash.hash(datos.contrasena),
                )

        #Contraseña incorrecta
        if not contrasena_valida:
            intentos = usuario.intentos_fallidos + 1
            bloqueado_hasta = None
            if intentos >= 5:
                bloqueado_hasta = ahora + timedelta(minutes=15)
            self.repositorio.actualizar_intentos_login(
                usuario.id_usuario,
                intentos,
                bloqueado_hasta,
            )
            if intentos >= 5:
                raise ValueError("Cuenta bloqueada temporalmente durante 15 minutos")
            raise ValueError("Credenciales inválidas")

        #Contraseña correcta
        self.repositorio.actualizar_intentos_login(
            usuario.id_usuario,
            0,
            None,
        )
        return{
            "id_usuario":usuario.id_usuario,
            "nombre":usuario.nombre,
            "email":usuario.email,
            "rol":usuario.rol,
        }
