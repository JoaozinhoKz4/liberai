import mysql.connector
from mysql.connector import Error
import numpy as np


class database:

    #initiate connection
    def __init__(self):    
        self.Storage = {}  #Dicionario Encoding : Id e Valid
        self.encoding = []
        self.metadata = []
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                database='liberai',
                                                user='root',
                                                password='1234')
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
            
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (self.connection.is_connected()):
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is ready")

    #close connection
    def __del__(self):
        if (self.connection.is_connected()):
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")


    #Read from the image table to obtain encoding
    def read_ALL_Encoding(self):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                database='liberai',
                                                user='root',
                                                password='1234')
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT id,valid,encoding FROM Image_Reg WHERE valid IS TRUE;")
            record = self.cursor.fetchall()
            for row in record:
                #self.Storage[str(row[2])] = (row[0],1)
                self.encoding.append(np.fromstring(str(row[2]),sep='|'))
                self.metadata.append(row[0],row(1))
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (self.connection.is_connected()):
                self.cursor.close()
                self.connection.close()
        return self.Storage


    #Write at image table to save new encoding
    def write_Encoding(self, encode_A, photo, name, register):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                database='liberai',
                                                user='root',
                                                password='1234')
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
            encode = str.join("|",[str(i) for i in encode_A])
            self.cursor.execute("INSERT INTO Person (firstname,lastname,registration) VALUES ('%s','%s','%i');"%(name.split(' ',1)[0],name.replace(name.split(' ',1)[0],''),int(register)))
            self.cursor.execute("SELECT id_person FROM Person WHERE firstname='%s' AND lastname='%s' AND registration='%i';"%(name.split(' ',1)[0],name.replace(name.split(' ',1)[0],''),int(register)))
            id_person = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT IGNORE INTO Image_Reg (id,encoding,photo) VALUES ('%s','%s','%s');"%(id_person,encode,photo))
            #não utilizamos  ON DUPLICATE KEY UPDATE
            #self.Storage[str(encode)] = (register,1)
           
        except Error as e:
            print("Error while connecting to MySQL", e)
            
        finally:
            if (self.connection.is_connected()):
                self.connection.commit()
                self.cursor.close()
                self.connection.close()
            
                 
