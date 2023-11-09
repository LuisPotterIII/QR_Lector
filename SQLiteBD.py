import sqlite3

conexion = sqlite3.connect("Cuentas_Alumno.db")

cursor = conexion.cursor()

sentencia = """
CREATE TABLE IF NOT EXISTS UAEM_Alumnos (
    Cuenta INTEGER PRIMARY KEY,
    Nombre TEXT,
    Celular INTEGER
)
"""
cursor.execute(sentencia)

datos_alumnos = [
    (1926495, "Luis Fernando", 5587273903),
    (1926618, "Carmen", 5515825061),
]

sentencia_insert = """
INSERT INTO UAEM_Alumnos (Cuenta, Nombre, Celular) VALUES (?, ?, ?)
"""
cursor.executemany(sentencia_insert, datos_alumnos)

conexion.commit()
conexion.close()