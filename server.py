#Importar mysql-connector
import mysql.connector
import json

from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

class crud():
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', port='3307', user='root',password='', database='elecciones')
        if self.conn.is_connected():
            print('Conectado a la base de datos')
        else:
            print('No se pudo conectar a la base de datos')

    #FUNCION PARA EJECUTAR SQL
    def ejecutar_sql(self, sql, value):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, value)
            self.conn.commit()
            return {'status': 'ok', 'msg': 'Se han realizado los cambios correctamente'}
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se pudo realizar la consulta', 'code': str(err)}

    #FUNCION PARA ADMINISTRAR CANDIDATOS
    def administrar_candidatos(self, candidato):
        try:
            print(candidato)
            if candidato['action'] == 'insertar':
                sql = "INSERT INTO candidatos (Id_Candidato, Nombre, Partido, Correo, Telefono, Fecha_Nacimiento, Img_Src) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (self.crear_id('candidatos'), candidato['name'], candidato['partido'], candidato['email'], candidato['telefono'], candidato['fecha_nacimiento'], candidato['foto'])
            elif candidato['action'] == 'actualizar':
                sql = "UPDATE candidatos SET Nombre = %s, Partido = %s, Correo = %s, Telefono = %s, Fecha_Nacimiento = %s, Img_Src = %s WHERE Id_Candidato = %s"
                val = (candidato['name'], candidato['partido'], candidato['email'], candidato['telefono'], candidato['fecha_nacimiento'], candidato['foto'], candidato['id'])
            elif candidato['action'] == 'eliminar':
                sql = "DELETE FROM candidatos WHERE Id_Candidato = %s"
                val = (candidato['id'],)
            else:
                print('Accion no valida')
            return self.ejecutar_sql(sql, val)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}
    
    #FUNCION PARA ADMINISTRAR PARTIDOS
    def administrar_partidos(self, partido):
        try:
            if partido['action'] == 'insertar':
                sql = "INSERT INTO partidos (Id_Partido, Nombre, Siglas) VALUES (%s, %s, %s)"
                val = (self.crear_id('partidos'), partido['name'], partido['siglas'])
            elif partido['action'] == 'actualizar':
                sql = "UPDATE partidos SET Nombre = %s, Siglas = %s WHERE Id_Partido = %s"
                val = (partido['name'], partido['siglas'], partido['id'])
            elif partido['action'] == 'eliminar':
                sql = "DELETE FROM partidos WHERE Id_Partido = %s"
                val = (partido['id'],)
            else:
                print('Accion no valida')
            return self.ejecutar_sql(sql, val)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

    #CONSULTA PARA ADMINISTRAR USUARIOS
    def administrar_usuarios(self, usuario):
        try:
            if usuario['action'] == 'insertar':
                sql = "INSERT INTO usuarios (Id_Usuario, DUI, Nombre, Telefono, Correo, Contrasegna, Img_Src) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (self.crear_id('usuarios'), usuario['dui'], usuario['name'], usuario['telefono'], usuario['correo'], usuario['password'], usuario['foto'])
            elif usuario['action'] == 'actualizar':
                sql = "UPDATE usuarios SET DUI = %s, Nombre = %s, Telefono = %s, Correo = %s, Contrasegna = %s, Img_Src = %s WHERE Id_Usuario = %s"
                val = (usuario['dui'], usuario['name'], usuario['telefono'], usuario['correo'], usuario['password'], usuario['foto'], usuario['id'])
            elif usuario['action'] == 'eliminar':
                sql = "DELETE FROM usuarios WHERE Id_Usuario = %s"
                val = (usuario['id'],)
            else:
                print('Accion no valida')
            return self.ejecutar_sql(sql, val)
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

    def mostrar_perfil(self, dui):
        try:
            sql = "SELECT (Nombre, Telefono, Correo, Img_Src) FROM usuarios WHERE DUI = %s"
            val = (dui,)
            cursor = self.conn.cursor()
            cursor.execute(sql, val)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return {'status':'error', 'msg': 'No se pudo realizar la consulta', 'code': str(e)}

    def mostrar_partidos(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = "SELECT * FROM partidos"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se pudieron encontrar los partidos', 'code': str(err)}

    def mostrar_candidatos(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = "SELECT candidatos.Id_Candidato, candidatos.Nombre, partidos.Nombre As Nombre_Partido, candidatos.Correo, candidatos.Telefono, candidatos.Fecha_Nacimiento, candidatos.Img_Src FROM candidatos, partidos WHERE candidatos.Partido = partidos.Id_Partido"
            cursor.execute(sql)
            result = cursor.fetchall()
            for candidato in result:
                candidato['Fecha_Nacimiento'] = candidato['Fecha_Nacimiento'].strftime('%d/%m/%Y')
            return result
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se pudieron encontrar candidatos', 'code': str(err)}

    def mostrar_usuarios(self):
        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se pudieron encontrar los usuarios', 'code': str(err)}

    def ingresar(self, dui, nombre, contra):
        try:
            cursor = self.conn.cursor()
            sql = "SELECT * FROM usuarios WHERE DUI = %s AND Nombre = %s AND Contrasegna = %s"
            val = (dui, nombre, contra)
            cursor.execute(sql, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return {'status': 'ok', 'msg': 'Inicio de sesión exitosa'}
            else:
                return {'status': 'error', 'msg': 'No se ha encontrado el usuario'}
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se ha podido iniciar sesión', 'code': str(err)}

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

curd = crud()

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/login.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/index':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/admin':
            self.path = '/admin.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/candidatos':
            self.path = '/candidatos.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/partidos':
            self.path = '/partidos.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/user':
            self.path = '/user.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/admincandidato':
            self.path = '/admincandidato.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/adminpartido':
            self.path = '/adminpartido.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/adminusuario':
            self.path = '/adminusuario.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/mostrar_partidos':
            response = curd.mostrar_partidos()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        
        elif self.path == '/mostrar_candidatos':
            response = curd.mostrar_candidatos()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/mostrar_usuarios':
            response = curd.mostrar_usuarios()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        
        elif self.path == '/perfil':
            response = curd.mostrar_perfil(self.user)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

    def do_POST(self):
        if self.path == '/ingresar':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)

            result = curd.ingresar(data['dui'], data['name'], data['password'])
            print(result)
            if result['status'] == 'ok':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict(response=result)).encode('utf-8'))
            
        elif self.path == '/guardarFoto':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            with open('profile/' + data['name'], 'wb') as f:
                f.write(data['foto'].encode('utf-8'))
            response = {'status': 'ok', 'msg': 'Foto guardada'}
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(dict(response)).encode('utf-8'))

        elif self.path == '/logout':
            self.user = None
            response = {'status': 'ok', 'msg': 'Sesión cerrada'}
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(dict(response)).encode('utf-8'))

        #CONSULTAS PARA CANDIDATOS
        elif self.path == '/administrar_candidatos':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            response = curd.administrar_candidatos(data)
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        #CONSULTAS PARA PARTIDOS
        elif self.path == '/administrar_partidos':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            print(data)
            response = curd.administrar_partidos(data)
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        
        #CONSULTAS PARA USUARIOS
        elif self.path == '/administrar_usuarios':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            response = curd.administrar_usuarios(data)
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))


print('Servidor iniciado')
httpd = HTTPServer(('localhost', 8000), Handler)
httpd.serve_forever()