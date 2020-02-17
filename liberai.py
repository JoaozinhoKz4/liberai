import face_recognition #importa o módulo face_recognition
import cv2 #importa o módulo cv2
from datetime import datetime, timedelta #importa do módulo datetime as libs datetime e timedelta
import numpy as np #importa o módulo numpy como np
import platform #importa o módulo platform
import pickle #importa o módulo pickle

know_face_encodings = []
know_face_metadata= []

def carregar_faces_conhecidas(): # Define a função que carrega da base de dados a codificação facial e os metadados faciais
    global know_face_encodings, know_face_metadata

    try: # tenta abrir o arquivo
        with open("faces_conhecidas.dat", "rb") as face_data_file:
            know_face_encodings, know_face_metadata = pickle.load(face_data_file)
            print("Sucesso ao importar dados.")
    except FileNotFoundError as e:
        print("Não foi possível encontrar o arquivo com dados, iniciando com um arquivo vazio.")
        pass

def lookup_known_face(face_encoding):
    
    metadata = None

    if len(know_face_encodings) == 0:
        return metadata

    face_distances = face_recognition.face_distance(
        know_face_encodings, 
        face_encoding
    )

    best_match_index = np.argmin(face_distances)

    if face_distances[best_match_index] < 0.55:
        metadata = know_face_metadata[best_match_index]

    return metadata