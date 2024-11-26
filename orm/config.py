#El engine permite configurar la conexion a la BD
from sqlalchemy import create_engine
#El sesion maker permite crear sesiones para hacaer consultas
#Por cada consulta se abre y se cierra 
from sqlalchemy.orm import sessionmaker
#declarative_base permite definir la clase base para mapear las tablas de la BD
from sqlalchemy.ext.declarative import declarative_base

#1. Configurar la conexión BD
#Nombre del servidor, usuario, pasword@url y el puerto
#Crear la URL de la BD -> servidorBD://usuario:password@url:puerto/nombreBD
URL_BASE_DATOS = "postgresql://usuario-ejemplo:estelary21013009@localhost:5432/base-ejemplo"
# Conectarnos mediante el esquema(schema) app, se usa el schema para fragmentar la base de datos 
engine = create_engine(URL_BASE_DATOS,connect_args={"options": "-csearch_path=app"})
#2. Obtener la clase que nos permite crear objetos tipo sesion
SesionClass = sessionmaker(engine) #Esta clase nos permite objeter objetos de tipo sesison
#Crear una funcion para obtener objetos de la clase SesionClass
def generador_sesion():
    sesion = SesionClass()
    try:
        #Equivalente a return sesion pero de manera segura 
        yield sesion 
    finally:
        sesion.close()
#3.Obtener la clase base para mapear tablas 
BaseClass = declarative_base()
