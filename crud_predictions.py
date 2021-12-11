import conexion

db = conexion.conexion()
class crud_predictions:
    def votos_intervalo(self, id, fecha_inicio, fecha_fin):
        try:
            cursor = db.conn.cursor(dictionary=True)
            sql = "SELECT candidatos.Id_Candidato, candidatos.Nombre, COUNT(votaciones.Id_Votacion) AS Votos FROM candidatos, votaciones WHERE candidatos.Id_Candidato = votaciones.Id_Candidato AND votaciones.Hora BETWEEN %s AND %s AND votaciones.Id_Candidato = %s GROUP BY candidatos.Id_Candidato"
            val = (fecha_inicio, fecha_fin, id)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudieron encontrar los votos', 'code': str(e), 'votos':{}}