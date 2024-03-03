#funcion que verifica que un correo exista en la base de datos
from repositorios.BdRepository import BaseRepository

bdRepository = BaseRepository()
def verifyTeamExistence(id_team):
   
    data = bdRepository.selectByCondition("equipo", f"id_equipo  = '{id_team}'")
    return  True  if data else False #si existe manda true