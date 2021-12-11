#Importar mysql-connector
import json
import datetime
import random
import string
from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import tensorflow as tf
import pandas as pd
import numpy as np
from PIL import Image

import crud_usuarios
import crud_candidatos
import crud_partidos
import crud_votos
import crud_predictions

crud_usuarios = crud_usuarios.crud_usuarios()
crud_candidatos = crud_candidatos.crud_candidatos()
crud_partidos = crud_partidos.crud_partidos()
crud_votos = crud_votos.crud_votos()
crud_predictions = crud_predictions.crud_predictions()

#Crear un dataset de entrenamiento
dataset = pd.read_csv('predict.csv', sep=';')
dea = dataset[['de', 'a']]
prediccion_entrenamiento = dataset[['predict']]
#Crear un dataset de prueba
test_dataset = pd.read_csv('test.csv', sep=';')
dea_entrenamiento = test_dataset[['de', 'a']]
label_entrenamiento = test_dataset[['lable']]
#Combertir los datos a numpy
dea_entrenamiento = dea_entrenamiento.values
label_entrenamiento = label_entrenamiento.values
dea = dea.values
prediccion_entrenamiento = prediccion_entrenamiento.values
print(dea.shape)
#Crear el modelo
model = tf.keras.models.Sequential()
#Agregar capas
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(1))
#Compilar el modelo
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
#Entrenar el modelo
model.fit(dea, prediccion_entrenamiento, epochs=500, batch_size=32, verbose=1)
#Evaluar
model.evaluate(dea, prediccion_entrenamiento)
#Predecir
prediccion = model.predict(dea_entrenamiento)
#Convertir a json
prediccion = prediccion.tolist()
prediccion = json.dumps(prediccion)
#Convertir a json
label_entrenamiento = label_entrenamiento.tolist()
label_entrenamiento = json.dumps(label_entrenamiento)
print(prediccion)
print(label_entrenamiento)

datos = {'login':False}
llave = None

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global datos
        global llave
        print(datos['login']==True, datos, self.path)

        if self.path == '/access':
            if datos['login'] == True:
                print('Acceso permitido')
                response = {'access':True}
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
            else:
                print('Acceso denegado')
                response = {'access':False}
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/':
            self.path = '/login.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/index':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/login':
            self.path = '/login.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == '/admin':
            llave = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            # llave = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))
            print(llave)
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

        elif self.path == '/admin/'+llave:
            responses = {'status':'ok', 'msg': 'Acceso permitido'}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=responses)).encode('utf-8'))

        elif self.path == '/mostrar_partidos':
            response = crud_partidos.mostrar_partidos()
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        
        elif self.path == '/mostrar_candidatos':
            response = crud_candidatos.mostrar_candidatos()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/mostrar_usuarios':
            response = crud_usuarios.mostrar_usuarios()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        
        elif self.path == '/perfil':
            response = crud_usuarios.mostrar_perfil(datos)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

        elif self.path == '/mostrar_votos':
            response = crud_votos.mostrar_votos()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))
        
        elif self.path == '/voto_listo':
            response = crud_votos.voto_listo(datos['id'])
            print('Votos listos?',response)
            if response != []:
                result = True
            else:
                result = False
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=result)).encode('utf-8'))

        elif self.path == '/prediccion_votos':
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            hora_iniciomin = (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime("%H:%M:%S")
            hora_inicio = datetime.datetime.now() - datetime.timedelta(hours=1)
            hora_inicio = hora_inicio.strftime("%H:%M:%S")
            print(hora_actual, hora_iniciomin, hora_inicio)
            votos_totales = crud_votos.mostrar_votos()
            print(votos_totales)
            prediccion = {}
            for voto in votos_totales:
                votos = crud_predictions.votos_intervalo(voto['Id_Candidato'], hora_inicio, hora_actual)
                print(votos)
                if votos != []:
                    print('Votos en el intervalo',votos)
                    votos_totales[voto['Id_Candidato']-1]['votos_hora'] = votos[0]['Votos']
                    votos_totales[voto['Id_Candidato']-1]['votos_antiguos'] = votos_totales[voto['Id_Candidato']-1]['Votos'] - votos[0]['Votos']
                else:
                    votos_totales[voto['Id_Candidato']-1]['votos_hora'] = 0
                    votos_totales[voto['Id_Candidato']-1]['votos_antiguos'] = 0

                nombre = votos_totales[voto['Id_Candidato']-1]['Nombre'].split(' ')[0]
                prediccion[nombre+str(voto['Id_Candidato'])] = [int(votos_totales[voto['Id_Candidato']-1]['votos_hora']), int(votos_totales[voto['Id_Candidato']-1]['Votos'])]
                
                prediccion[nombre+str(voto['Id_Candidato'])] = np.array(prediccion[nombre+str(voto['Id_Candidato'])])
                prediccion[nombre+str(voto['Id_Candidato'])] = int(model.predict(prediccion[nombre+str(voto['Id_Candidato'])].reshape(1,2))[0][0])
                
            print(prediccion)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(response=prediccion)).encode('utf-8'))

        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode('utf-8')
        data = parse.unquote(data)
        data = json.loads(data)

        if self.path == '/ingresar': #INGRESAR A LA CUENTA
            result = crud_usuarios.ingresar(data['dui'], data['name'], data['password'])
            print(result[1])
            if result[0]['status'] == 'ok':
                datos['login'] = True
                datos['id'] = (result[1][0]['Id_Usuario'])
                datos['dui'] = data['dui']
                datos['pass'] = data['password']
                datos['name'] = data['name']
                self.activo = result
                response = result[0]

        #CONSULTAS PARA CANDIDATOS
        elif self.path == '/administrar_candidatos':
            response = crud_candidatos.administrar_candidatos(data)
            print('Respuesta',response)
            print('HAY FOTO?',data['actualizarFoto'] == True or data['action'] == 'insertar')
            if data['actualizarFoto'] == True or data['action'] == 'insertar':
                if response[0]['status'] == 'ok':
                    matriz = data["pixeles"]
                    matriz = [matriz[i:i+250] for i in range(0, len(matriz), 250)]
                    matriz = np.array(matriz)
                    print(matriz.shape)

                    im = Image.fromarray((matriz).astype(np.uint8))
                    print("candidates/candidate"+str(response[1])+".jpg")
                    im.save("candidates/candidate"+str(response[1])+".jpg")
                    print(matriz.shape)

        #CONSULTAS PARA PARTIDOS
        elif self.path == '/administrar_partidos':
            response = crud_partidos.administrar_partidos(data)
            print(response)
        
        #CONSULTAS PARA USUARIOS
        elif self.path == '/administrar_usuarios':
            response = crud_usuarios.administrar_usuarios(data)
            print('Respuesta',response)
            if data['actualizarFoto'] == True or data['action'] == 'insertar':
                if response[0]['status'] == 'ok':
                    if data['login'] == True:
                        datos['login'] = True
                        datos['id'] = response[1]
                        datos['dui'] = data['dui']
                        datos['pass'] = data['password']
                        datos['name'] = data['name']

                    matriz = data["pixeles"]
                    matriz = [matriz[i:i+250] for i in range(0, len(matriz), 250)]
                    matriz = np.array(matriz)
                    print(matriz.shape)

                    im = Image.fromarray((matriz).astype(np.uint8))
                    im.save("profile/profile"+str(response[1])+".jpg")
                    print(matriz.shape)

        #CONSULTAS PARA VOTOS
        elif self.path == '/administrar_votos':
            data['idUsuario'] = datos['id']
            response = crud_votos.administrar_votos(data)
            print(response)

        #SALIR
        elif self.path == '/salir':
            print('Cerrando sesion')
            datos['login'] = False
            response = {'status':'ok', 'msg':'Sesión cerrada'}

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(dict(response=response)).encode('utf-8'))

print('Servidor iniciado')
httpd = HTTPServer(('localhost', 3000), Handler)
httpd.serve_forever()