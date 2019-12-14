import face_recognition #importa o módulo face_recognition
import cv2 #importa o módulo cv2
from datetime import datetime, timedelta #importa do módulo datetime as libs datetime e timedelta
import numpy as np #importa o módulo numpy como np
import platform #importa o módulo platform
import pickle #importa o módulo pickle

know_face_encodings = []
know_face_metadata= []

def salvar_faces_conhecidas():  # Define a função que salva os encodings e os metadados de cada rosto, de maneira binária, em um arquivo de dados .dat
     with open("faces_conhecidas.dat", "wb") as face_data_file: 
        face_data = [know_face_encodings, know_face_metadata] 
        pickle.dump(face_data, face_data_file) #pickle é um módulo para manipulação de binários em python
        print("Backup realizado.")

def carregar_faces_conhecidas(): # Define a função que carrega da base de dados a codificação facial e os metadados faciais
    global know_face_encodings, know_face_metadata

    try: # tenta abrir o arquivo
        with open("faces_conhecidas.dat", "rb") as face_data_file:
            know_face_encodings, know_face_metadata = pickle.load(face_data_file)
            print("Sucesso ao importar dados.")
    except FileNotFoundError as e:
        print("Não foi possível encontrar o arquivo com dados, iniciando com um arquivo vazio.")
        pass

def registrar_nova_face(face_encoding, face_image): # Adiciona nova pessoa a nossa lista de faces conhecidas
    
    know_face_encodings.append(face_encoding) #Adiciona a codificação do facial ao vetor de codificações global.

    know_face_metadata.append({
        "data_do_cadastro": datetime.now(),
        "face_image": face_image,
        "datricula": matricula,
        "nome": nome_aluno,
    })

def lookup_known_face(face_encoding):
    
    metadata = None

    if len(known_face_encodings) == 0:
        return metadata

    face_distances = face_recognition.face_distance(
        known_face_encodings, 
        face_encoding
    )

    best_match_index = np.argmin(face_distances)

    if face_distances[best_match_index] < 0.65:
        metadata = known_face_metadata[best_match_index]
        metadata["data_do_cadastro"] = datetime.now()

    return metadata

def main_loop():

    video_capture = cv2.VideoCapture(0)