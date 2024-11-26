import orm.modelos as modelos #ME da acceso a todo ese archivo modelos
from sqlalchemy.orm import Session


#Esta función es llamada por apy.py
#para atender GET '/usuarios/{id}'
#select * from app.usuarios where id = id_usuario
def usuario_por_id(sesion:Session,id_usuario:int): #Mediante la Session se pueden hacer consultas
    print("select * from app.usuarios where id = ", id_usuario)
    #Que tabla quiero utilizar, y se aplica un filtro ya que solo quiero que me muestre uno y que sea por id
    return sesion.query(modelos.Usuario).filter(modelos.Usuario.id==id_usuario).first() #se devuelve un objeto de tipo usuario

#Esta función es llamada por apy.py
#para atender GET '/compras/{id}'
#select * from app.compras where id = id_compra
def compra_por_id(sesion:Session,id_compra:int): #Mediante la Session se pueden hacer consultas
    print("select * from app.compras where id = ", id_compra)
    #Que tabla quiero utilizar, y se aplica un filtro ya que solo quiero que me muestre uno y que sea por id
    return sesion.query(modelos.Compra).filter(modelos.Compra.id==id_compra).first() #se devuelve un objeto de tipo compra

#Esta función es llamada por apy.py
#para atender GET '/fotos/{id}'
#select * from app.fotos where id = id_fotos
def foto_por_id(sesion:Session,id_foto:int): #Mediante la Session se pueden hacer consultas
    print("select * from app.fotos where id = ", id_foto)
    #Que tabla quiero utilizar, y se aplica un filtro ya que solo quiero que me muestre uno y que sea por id
    return sesion.query(modelos.Foto).filter(modelos.Foto.id==id_foto).first() #se devuelve un objeto de tipo foto
