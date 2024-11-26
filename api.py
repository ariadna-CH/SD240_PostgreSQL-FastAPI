from fastapi import FastAPI, UploadFile, File, Form, Depends
from typing import Optional
from pydantic import BaseModel
import shutil
import os
import uuid

from sqlalchemy.orm import Session
from orm.config import generador_sesion #generador de sesiones
#Funciones para hacer las consultas a la BD
import orm.repo as repo #El as repo es un alias 

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    edad:int
    domicilio:str    
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]


# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }

    return compra
#-------------------------------------------------------------------------------------------------------
#CONSULTAS
#Usuario
@app.get("/usuarios/{id}")
#SE HACE LA CONSULTA A LA BASE DE DATOS
#Es obligatorio que el usuario mande el id pero no las sesiones ya que las esta creando el servidor
def usuario_por_id(id: int, sesion:Session=Depends(generador_sesion)): 
    print("Api consultando usuario por id")
    return repo.usuario_por_id(sesion, id) #manda el objeto usuario pero lo convierte a .json
#def usuario_por_id(id: int):
    #print("buscando usuario por id:", id)
    # simulamos consulta a la base:
    #return usuarios[id]
#Compra
@app.get("/compras/{id}")
#SE HACE LA CONSULTA A LA BASE DE DATOS
#Es obligatorio que el usuario mande el id pero no las sesiones ya que las esta creando el servidor
def compra_por_id(id: int, sesion:Session=Depends(generador_sesion)): 
    print("Api consultando compra por id")
    return repo.compra_por_id(sesion, id) #manda el objeto compra pero lo convierte a .json
#Foto
@app.get("/fotos/{id}")
#SE HACE LA CONSULTA A LA BASE DE DATOS
#Es obligatorio que el usuario mande el id pero no las sesiones ya que las esta creando el servidor
def foto_por_id(id: int, sesion:Session=Depends(generador_sesion)): 
    print("Api consultando foto por id")
    return repo.foto_por_id(sesion, id) #manda el objeto foto pero lo convierte a .json
#-----------------------------------------------------------------------------------------------------------

@app.get("/usuarios")
def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
    print("lote:",lote, " pag:", pag, " orden:", orden)
    #simulamos la consulta
    return usuarios

@app.post("/usuarios")
def guardar_usuario(usuario:UsuarioBase, parametro1:str):
    print("usuario a guardar:", usuario, ", parametro1:", parametro1)
    #simulamos guardado en la base.
    
    usr_nuevo = {}
    usr_nuevo["id"] = len(usuarios)
    usr_nuevo["nombre"] = usuario.nombre
    usr_nuevo["edad"] = usuario.edad
    usr_nuevo["domicilio"] = usuario.domicilio

    usuarios.append(usuario)

    return usr_nuevo

@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int):
    #simulamos una consulta
    if id>=0 and id< len(usuarios):
        usuario = usuarios[id]
    else:
        usuario = None
    
    if usuario is not None:
        usuarios.remove(usuario)
    
    return {"status_borrado", "ok"}

@app.post("/fotos")
async def guardar_foto(titulo:str=Form(None), descripcion:str=Form(...), foto:UploadFile=File(...)):
    print("titulo:", titulo)
    print("descripcion:", descripcion)

    home_usuario=os.path.expanduser("~")
    nombre_archivo=uuid.uuid4().hex  #generamos nombre único en formato hexadecimal
    extension = os.path.splitext(foto.filename)[1]
    ruta_imagen=f'{home_usuario}/fotos-ejemplo/{nombre_archivo}{extension}'
    print("guardando imagen en ruta:", ruta_imagen)

    with open(ruta_imagen,"wb") as imagen:
        contenido = await foto.read() #read funciona de manera asyncrona
        imagen.write(contenido)

    return {"titulo":titulo, "descripcion":descripcion, "foto":foto.filename}
