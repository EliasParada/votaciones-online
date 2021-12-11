import conexion
import datetime

db = conexion.conexion()
class crud_votos:
    def administrar_votos(self, voto): # Administrar votos
        try:
            date = datetime.datetime.now().date()
            time = datetime.datetime.now().time()
            print(date)
            if voto['action'] == 'insertar':
                sql = "INSERT INTO votaciones (Id_Votacion, Id_Candidato, Id_Usuario, Fecha, Hora) VALUES (%s, %s, %s, %s, %s)"
                val = (db.crear_id('votos'), voto['candidato'], voto['idUsuario'], date, time)
            elif voto['action'] == 'actualizar':
                sql = "UPDATE votaciones SET Id_Candidato = %s, Id_Usuario = %s WHERE Id_Voto = %s"
                val = (voto['candidato'], voto['usuario'], voto['id'])
            elif voto['action'] == 'eliminar':
                sql = "DELETE FROM votaciones WHERE Id_Voto = %s"
                val = (voto['id'],)
            else:
                print('Accion no valida')
            return db.ejecutar_sql(sql, val, None)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

    def mostrar_votos(self): # Mostrar todos los votos
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT candidatos.Id_Candidato, candidatos.Nombre, COUNT(votaciones.Id_Votacion) AS Votos FROM candidatos, votaciones WHERE candidatos.Id_Candidato = votaciones.Id_Candidato GROUP BY candidatos.Id_Candidato"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudieron encontrar los votos', 'code': str(e), 'votos':{}}

    def voto_listo(self, id): # Si ya se voto o no
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT Id_Votacion FROM votaciones WHERE Id_Usuario = %s"
            val = (id,)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudieron encontrar los votos', 'code': str(e)}