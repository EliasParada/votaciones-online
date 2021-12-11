import mysql.connector

class conexion:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', port='3307', user='root',password='', database='elecciones')
        if self.conn.is_connected():
            print('Conectado a la base de datos')
        else:
            print('No se pudo conectar a la base de datos')

    #FUNCION PARA EJECUTAR SQL
    def ejecutar_sql(self, sql, value, id):
        try:
            print(sql, value, id)
            cursor = self.conn.cursor()
            cursor.execute(sql, value)
            self.conn.commit()
            return {'status': 'ok', 'msg': 'Se han realizado los cambios correctamente'}, id
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se pudo realizar la consulta', 'code': str(err)}

    #FUNCION PARA CONSULTAR SQL
    def consultar_sql(self, sql, value):
        try:
            print(sql, value)
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, value)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return str(err)

    #CREAR ID
    def crear_id(self, table):
        try:
            print('ID para la tabla', table)
            cursor = self.conn.cursor()
            if table == 'usuarios':
                sql = "SELECT MAX(Id_Usuario) FROM usuarios"
            elif table == 'candidatos':
                sql = "SELECT MAX(Id_Candidato) FROM candidatos"
            elif table == 'partidos':
                sql = "SELECT MAX(Id_Partido) FROM partidos"
            elif table == 'votos':
                sql = "SELECT MAX(Id_Votacion) FROM votaciones"
            cursor.execute(sql)
            id = cursor.fetchone()
            print('El id maximo actual es:',id)
            if id[0] == None:
                id = 1
            else:
                id = id[0] + 1
            return id
        except mysql.connector.Error as err:
            return str(err)