import cv2
from pyzbar.pyzbar import decode
import numpy as np
from datetime import datetime
import pandas as pd
import pywhatkit
import sqlite3

conexion = sqlite3.connect("Cuentas_Alumno.db")

cursor = conexion.cursor()

cap = cv2.VideoCapture(0)
now = datetime.now()
h = now.hour
asistencia = []

while True:
    ret, frame = cap.read()

    cv2.putText(frame, 'Localiza QR', (160, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame, (170, 100), (470, 400), (0, 255, 0), 2)

    #Leer QR
    for codes in decode(frame):

        #Decodificar
        info = codes.data.decode('utf-8')
        
        #Cuenta
        codigo = info[0:]
        N_Cuenta = int(codigo)

        sentencia_seleccion = "SELECT * FROM UAEM_Alumnos WHERE Cuenta = ?"
        cursor.execute(sentencia_seleccion, (N_Cuenta,))
        datos = cursor.fetchone()
        if datos:
            Nombre = datos[1]
            Cel = datos[2]
            Celular = '+52' + str(Cel)
            Mensaje = "Alumno: " + Nombre + " ingresó al plantel"

            pts = np.array([codes.polygon], np.int32)
            xi, yi = codes.rect.left, codes.rect.top
            pts = pts.reshape((-1, 1, 2))

            #Asistencia
            if 22 >= h >= 5:
                cv2.polylines(frame, [pts], True, (255, 255, 0), 5)
                #Guardar ID
                if codigo not in asistencia:
                    #Agregar ID
                    pos = len(asistencia)
                    asistencia.append(codigo)
                    ahora = datetime.now()
                    h_a = ahora.hour
                    m_a = ahora.minute
                    #Aviso de ingreso del alumno
                    pywhatkit.sendwhatmsg(Celular, Mensaje, h_a, m_a + 1, 10, True, 1)

                # Aviso
                elif codigo in asistencia:
                    cv2.putText(frame, 'ID: ' + str(codigo),
                                (xi - 65, yi - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, 'ya ingresado.',
                                (xi - 65, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            pts = np.array([codes.polygon], np.int32)
            xi, yi = codes.rect.left, codes.rect.top
            pts = pts.reshape((-1, 1, 2))
            cv2.putText(frame, 'ID no encontrado.',
                        (xi - 65, yi - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
    cv2.imshow(" Lector QR ", frame)
    #Lectura teclado
    t = cv2.waitKey(5)
    if t == 27:
        break

conexion.close()
cv2.destroyAllWindows()
cap.release()