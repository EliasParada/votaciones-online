import conexion

db = conexion.conexion()
class crud_partidos:
    def administrar_partidos(self, partido): # Administrar partidos
        try:
            if partido['action'] == 'insertar':
                sql = "INSERT INTO partidos (Id_Partido, Nombre, Siglas) VALUES (%s, %s, %s)"
                val = (db.crear_id('partidos'), partido['name'], partido['siglas'])
            elif partido['action'] == 'actualizar':
                sql = "UPDATE partidos SET Nombre = %s, Siglas = %s WHERE Id_Partido = %s"
                val = (partido['name'], partido['siglas'], partido['id'])
            elif partido['action'] == 'eliminar':
                sql = "DELETE FROM partidos WHERE Id_Partido = %s"
                val = (partido['id'],)
            else:
                print('Accion no valida')
            return db.ejecutar_sql(sql, val, None)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

    def mostrar_partidos(self): # Mostrar partidos
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT * FROM partidos"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudieron encontrar los partidos', 'code': str(e)}