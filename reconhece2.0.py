# -*- coding: cp1252 -*-
import face_recognition
import cv2
from google.cloud import storage
from firebase import firebase
from google.oauth2 import service_account
import os
import urllib
import numpy as np
from PIL import Image
import subprocess

#####################################################################################################
firebase = firebase.FirebaseApplication('https://chamadafacial.firebaseio.com/')
client = storage.Client.from_service_account_json('C:\Users\hp\key.json')
bucket = client.get_bucket('chamadafacial.appspot.com')

#download do firebase storage

result = []
win_cmd = 'gsutil ls -r gs://chamadafacial.appspot.com/photos**'

process = subprocess.Popen(win_cmd,
shell=True,
stdout=subprocess.PIPE,
stderr=subprocess.PIPE )
for line in process.stdout:
    result.append(line)
errcode = process.returncode

count = 0
print("Baixando imagens")
for line in result:
    file1 = line[31:]
    imgn = file1.split('/')
    imgname = imgn[0]
    file1 = "".join(file1)
    blob = bucket.blob(file1)
    url1 = blob.public_url
    url = url1 [:-6]
    req = urllib.urlopen(url)
    arr = np.asarray(bytearray(req.read()),dtype=np.uint8)
    img = cv2.imdecode(arr,-1)
    count += 1
    cv2.imwrite(imgname+str(count)+".jpg",img)

###################################################
win_cmd = 'gsutil ls -r gs://chamadafacial.appspot.com/photos**'

process = subprocess.Popen(win_cmd,
shell=True,
stdout=subprocess.PIPE,
stderr=subprocess.PIPE )
for line in process.stdout:
    result.append(line)
errcode = process.returncode

count = 0
print("Baixando imagens")
for line in result:
    file1 = line[31:]
    imgn = file1.split('/')
    imgname = imgn[0]
    file1 = "".join(file1)
    blob = bucket.blob(file1)
    url1 = blob.public_url
    url = url1 [:-6]
    req = urllib.urlopen(url)
    arr = np.asarray(bytearray(req.read()),dtype=np.uint8)
    img = cv2.imdecode(arr,-1)
    count += 1
    cv2.imwrite("test.jpg",img)



##########################################################################################################

# carrega uma imagem e aprende a reconhecer
obama_image = face_recognition.load_image_file("photos1.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# carrega uma imagem e aprende a reconhecer
biden_image = face_recognition.load_image_file("photos2.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Cria arrays de face_encodings conhecidos e seu nomes
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Jose",
    "Wellington",
    "Daniela"
]

# Inicializa variaveis
face_locations = []
face_encodings = []
face_names = []


# pega uma foto do firebase (ainda a implementar)
print("Fazendo reconhecimento")   
img = image = face_recognition.load_image_file("test.jpg")
img1 = cv2.imread('test.jpg',1)


# Encontra todas as faces e face encodings na imagem (img)
face_locations = face_recognition.face_locations(img)
face_encodings = face_recognition.face_encodings(img, face_locations)
face_names = []
    
for face_encoding in face_encodings:
    # vê se a face é um match das face(s) conhecidas
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Desconhecido(a)"

    # Se um match foi encontrado em known_face_encodings, usa a primeira.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
        
    face_names.append(name)


# Mostra os resultados
for (top, right, bottom, left), name in zip(face_locations, face_names):

    # Desenha um quadrado em volta da face
    cv2.rectangle(img1, (left, top), (right, bottom), (0, 0, 255), 2)

    # Escreve o nome abaixo
    cv2.rectangle(img1, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(img1, name, (left + 5, bottom - 5), font, 0.5, (255, 255, 255), 1)


#salva o resultado na pasta        
cv2.imwrite("resultado.jpg",img1)       

# Salvar resultados no firebase (imagem resultado já é enviada/ dados ainda precisam serem tradados)

num=1
imageBlob = bucket.blob("/")
imagePath = os.path.join("C:\Users","hp","Desktop","Reconhecimento Facial","resultado.jpg")
print("enviando resultado ao firebase")
imageBlob = bucket.blob("resultados/User"+"."+str(num))
imageBlob.upload_from_filename(imagePath)

cv2.imshow('image',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
    


