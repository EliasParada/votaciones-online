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
    
    def agregar_usuario(self, dui, nombre, telefono, correo, contra, src):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO usuarios (Id_Usuario, DUI, Nombre, Telefono, Correo, Contrasegna, Img_Src) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (self.crear_id('usuarios'), dui, nombre, telefono, correo, contra, src)
            cursor.execute(sql, val)
            self.conn.commit()
            return {'status': 'ok', 'msg': 'Registro exitoso'}
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se ha podido registrar el usuario', 'code': str(err)}

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

    def agregar_candidato(self, nombre, partido, correo, telefono, fecha_nacimiento, src):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO candidatos (Id_Candidato, Nombre, Partido, Correo, Telefono, Fecha_Nacimiento, Img_Src) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (self.crear_id('candidatos'), nombre, partido, correo, telefono, fecha_nacimiento, src)
            cursor.execute(sql, val)
            self.conn.commit()
            return {'status': 'ok', 'msg': 'Registro exitoso'}
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se ha podido registrar el candidato', 'code': str(err)}

    def agregar_partido(self, name, siglas):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO partidos (Id_Partido, Nombre, Siglas) VALUES (%s, %s, %s)"
            val = (self.crear_id('partidos'), name, siglas)
            cursor.execute(sql, val)
            self.conn.commit()
            return {'status': 'ok', 'msg': 'Registro exitoso'}
        except mysql.connector.Error as err:
            return {'status':'error', 'msg': 'No se ha podido registrar el partido', 'code': str(err)}

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

    def do_POST(self):
        if self.path == '/registrar':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)

            response = curd.agregar_usuario(data['dui'], data['name'], data['tel'], data['email'], data['password'], data['foto'])
            print(response)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(dict(response)).encode('utf-8'))

        elif self.path == '/ingresar':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)

            result = curd.ingresar(data['dui'], data['name'], data['password'])
            if result['status'] == 'ok':
                self.user = data['name']
            
        elif self.path == '/guardarFoto':
            #Guardar la foto en la carpeta profile
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

        elif self.path == '/agregar_candidato':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            response = curd.agregar_candidato(data['name'], data['partido'], data['email'], data['telefono'], data['fecha_nacimiento'], data['foto'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/agregar_partido':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            response = curd.agregar_partido(data['name'], data['siglas'])
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/agregar_usuario':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')
            data = parse.unquote(data)
            data = json.loads(data)
            print(data)
            response = curd.agregar_usuario(data['dui'], data['name'], data['telefono'], data['correo'], data['password'], data['foto'])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))


        elif self.path == '/logout':
            self.user = None
            response = {'status': 'ok', 'msg': 'Sesión cerrada'}
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(dict(response)).encode('utf-8'))

        elif self.path == '/mostrar_usuario':
            response = curd.mostrar_usuario(self.user)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(dict(response)).encode('utf-8'))

        elif self.path == '/mostrar_partido':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            data = data.decode('utf-8')

        elif self.path == '/eliminar_candidato':
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)


print('Servidor iniciado')
httpd = HTTPServer(('localhost', 8000), Handler)
httpd.serve_forever()