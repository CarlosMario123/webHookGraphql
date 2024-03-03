#funcion que verifica que un correo exista en la base de datos
from repositorios.BdRepository import BaseRepository

bdRepository = BaseRepository()
def verifyMailexistence(email):
    # Verifica si el usuario existe en la base de datos
    user_data = bdRepository.selectByCondition("personas", f"correo = '{email}'")
    return  True  if user_data else False #si existe manda true