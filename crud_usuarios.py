import conexion

db = conexion.conexion()
class crud_usuarios:
    def administrar_usuarios(self, usuario): # Administrar usuarios
        try:
            id = None
            if usuario['action'] == 'insertar':
                sql = "INSERT INTO usuarios (Id_Usuario, DUI, Nombre, Telefono, Correo, Contrasegna, Img_Src) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                id = db.crear_id('usuarios')
                val = (id, usuario['dui'], usuario['name'], usuario['telefono'], usuario['correo'], usuario['password'], 'profile/profile'+str(id)+'.jpg')
            elif usuario['action'] == 'actualizar':
                sql = "UPDATE usuarios SET DUI = %s, Nombre = %s, Telefono = %s, Correo = %s, Contrasegna = %s, Img_Src = %s WHERE Id_Usuario = %s"
                id = usuario['id']
                val = (usuario['dui'], usuario['name'], usuario['telefono'], usuario['correo'], usuario['password'], 'profile/profile'+str(usuario['id'])+'.jpg', usuario['id'])
            elif usuario['action'] == 'eliminar':
                sql = "DELETE FROM usuarios WHERE Id_Usuario = %s"
                val = (usuario['id'],)
            else:
                print('Accion no valida')
            return db.ejecutar_sql(sql, val, id)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

    def mostrar_usuarios(self): # Mostrar usuarios
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudieron encontrar los usuarios', 'code': str(e)}

    def mostrar_perfil(self, data): # Mostrar perfil en especifico
        try:
            sql = "SELECT Nombre, Correo, Telefono, Img_Src FROM usuarios WHERE Id_Usuario = %s"
            val = (data['id'],)
            cursor = db.conn.cursor(dictionary=True)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la consulta', 'code': str(e)}

    def ingresar(self, dui, nombre, contra): # Login
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT * FROM usuarios WHERE DUI = %s AND Nombre = %s AND Contrasegna = %s"
            val = (dui, nombre, contra)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return {'status': 'ok', 'msg': 'Inicio de sesión exitosa'}, result
            else:
                return {'status': 'error', 'msg': 'No se ha encontrado el usuario'}
        except Exception as e:
            return {'status':'error', 'msg': 'No se ha podido iniciar sesión', 'code': str(e)}