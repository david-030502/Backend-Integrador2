from sqlalchemy import select, update

from app.core.database import obtener_sesion
from app.entidades.Usuario import Usuario


class UsuarioRepositorio:
    def guardar(self, usuario):
        with obtener_sesion() as sesion:
            sesion.add(usuario)
            sesion.flush()
        return usuario

    def eliminar(self, id_usuario):
        with obtener_sesion() as sesion:
            usuario = sesion.get(Usuario, id_usuario)
            if not usuario:
                return False
            sesion.delete(usuario)
            return True
        
    def obtener_byemail(self, email):
        with obtener_sesion() as sesion:
            resultado = sesion.execute(
                select(Usuario).where(Usuario.email == email)
            )
            return resultado.scalar_one_or_none()

    def actualizar_contrasena(self, id_usuario, contrasena):
        with obtener_sesion() as sesion:
            sesion.execute(
                update(Usuario)
                .where(Usuario.id_usuario == id_usuario)
                .values(contrasena=contrasena)
            )

    def actualizar_intentos_login(self, id_usuario, intentos_fallidos, bloqueado_hasta,):
        with obtener_sesion() as sesion:
            sesion.execute(
                update(Usuario)
                .where(Usuario.id_usuario == id_usuario)
                .values(
                    intentos_fallidos = intentos_fallidos,
                    bloqueado_hasta = bloqueado_hasta,
                )
            )

    def actualizar_usuario(self, id_usuario, nombre, email, contrasena, rol):
        with obtener_sesion() as sesion:
            usuario = sesion.get(Usuario, id_usuario)
            if not usuario:
                return False
            usuario.nombre = nombre
            usuario.email = email
            usuario.rol = rol
            if contrasena is not None:
                usuario.contrasena = contrasena
            return True

    def obtener_byid(self, id_usuario):
        with obtener_sesion() as sesion:
            return sesion.get(Usuario, id_usuario)

    def listar_usuarios(self):
        with obtener_sesion() as sesion:
            resultado = sesion.execute(select(Usuario).order_by(Usuario.id_usuario))
            return resultado.scalars().all()
