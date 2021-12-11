import conexion

db = conexion.conexion()
class crud_candidatos:
    def administrar_candidatos(self, candidato): # Administrar candidatos
        try:
            id = None
            if candidato['action'] == 'insertar':
                sql = "INSERT INTO candidatos (Id_Candidato, Nombre, Partido, Correo, Telefono, Fecha_Nacimiento, Img_Src) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                id = db.crear_id('candidatos')
                val = (id, candidato['name'], candidato['partido'], candidato['email'], candidato['telefono'], candidato['fecha_nacimiento'], 'candidates/candidate'+str(id)+'.jpg')
            elif candidato['action'] == 'actualizar':
                sql = "UPDATE candidatos SET Nombre = %s, Partido = %s, Correo = %s, Telefono = %s, Fecha_Nacimiento = %s, Img_Src = %s WHERE Id_Candidato = %s"
                id = candidato['id']
                val = (candidato['name'], candidato['partido'], candidato['email'], candidato['telefono'], candidato['fecha_nacimiento'], 'candidates/candidate'+str(candidato['id'])+'.jpg', candidato['id'])
            elif candidato['action'] == 'eliminar':
                sql = "DELETE FROM candidatos WHERE Id_Candidato = %s"
                val = (candidato['id'],)
            else:
                print('Accion no valida')
            return db.ejecutar_sql(sql, val, id)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

    def mostrar_candidatos(self): # Mostrar candidatos
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT candidatos.Id_Candidato, candidatos.Nombre, partidos.Nombre As Nombre_Partido, partidos.Id_Partido As Id_Partido, candidatos.Correo, candidatos.Telefono, candidatos.Fecha_Nacimiento, candidatos.Img_Src FROM candidatos, partidos WHERE candidatos.Partido = partidos.Id_Partido"
            cursor.execute(sql)
            result = cursor.fetchall()
            for candidato in result:
                candidato['Fecha_Nacimiento'] = candidato['Fecha_Nacimiento'].strftime('%d/%m/%Y')
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudieron encontrar candidatos', 'code': str(e)}