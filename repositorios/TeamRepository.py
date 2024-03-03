from repositorios.BdRepository import BaseRepository
from validators.EmailVerification import verifyMailexistence
from validators.TeamVerifation import verifyTeamExistence
from services.TaskService import TaskService

#creamos una instancia de BD repository
bdRepository = BaseRepository()
taskService = TaskService()
class TeamRepository:
    def get_teams(self):
        results = bdRepository.select_all("equipo")

        if results is not None:
            teams_data = [{"id": row[0], "name": row[1]} for row in results]
            return teams_data
        else:
            error_message = "Error al obtener los equipos. Los resultados son None."
            return {"message": error_message, "data": []}
    def createTeam(self, name_team):
        try:
            # Verifica si el equipo ya existe
            existing_team = bdRepository.selectByCondition("equipo", f"nombre_equipo = '{name_team}'")

            if existing_team:
                raise ValueError("El equipo ya existe")
            
            data_insert = {"nombre_equipo": name_team}
            bdRepository.insertData("equipo", data_insert)
            new_team_id = bdRepository.selectByCondition("equipo", f"nombre_equipo = '{name_team}'")[0][0]

            return {"id": new_team_id, "name":name_team}
        except Exception as e:
            ValueError("hubo un error al crear los equipos")
            
    def addMemberTeam(self,correo,idTeam):
        idTeam = int(idTeam)
        if not verifyMailexistence(correo):
            return "el correo no existe en la base de datos"
        if not verifyTeamExistence(idTeam):
            return "el equipo no existe en la base de datos"
        
        idUser = bdRepository.selectByCondition("personas", f"correo = '{correo}'", ["id_persona"])[0][0]#consulta hacia cadena
        nameTeam = bdRepository.selectByCondition("equipo",f"id_equipo = {idTeam}",["nombre_equipo"])[0][0]#consulta hacia numero
        #procedemos con la insercion
        msg = bdRepository.insertData("equipo_personas",{"id_equipo":idTeam,"id_persona":idUser})
        if not msg:
            return "ese usuario ya esta en ese equipo"
        return f"el usuario con correo: {correo} se ha añadido al equipo: {nameTeam}"
    
    
    def deleteMemberTeam(self, correo, idTeam):
        try:
            idTeam = int(idTeam)

            # Verifica si el equipo existe
            if not verifyTeamExistence(idTeam):
                return "El equipo no existe en la base de datos"

            # Verifica si el usuario existe en la base de datos
            if not verifyMailexistence(correo):
                return "El correo no existe en la base de datos"

            # Obtiene el ID del usuario y el nombre del equipo
            idUser = bdRepository.selectByCondition("personas", f"correo = '{correo}'", ["id_persona"])[0][0]
            nameTeam = bdRepository.selectByCondition("equipo", f"id_equipo = {idTeam}", ["nombre_equipo"])[0][0]

            if not idUser or not nameTeam:
                return "Error al obtener información del usuario o del equipo"

            # Procede con la eliminación
            condition = f"id_equipo = {idTeam} AND id_persona = {idUser}"
            deleted_rows = bdRepository.deleteData("equipo_personas", condition)

            if deleted_rows > 0:
                return {"message":f"El usuario con correo {correo} ha sido eliminado del equipo {nameTeam}"}
            else:
                return {"message":"El usuario no estaba en el equipo o hubo un problema al eliminarlo"}

        except Exception as e:
            return {"message":f"Error al eliminar el usuario del equipo: {str(e)}"}
        
    def createTaskTeam(self,name,descripcion,estatus,idTeam):
        #verifamos que el equipo exista antes de poder crear la tareas
        if not verifyTeamExistence(idTeam):
           return "El equipo no existe en la base de datos"
            
        #creamos la task
        idTask = taskService.createTask(name,descripcion,estatus)[0]
        dataToBd = {"id_equipo": idTeam, "id_tarea":idTask}
        print(dataToBd)
        respuesta = bdRepository.insertData("equipo_tareas",dataToBd)
        
        return "tarea insertada correctamente en el equipo" if respuesta else "error al insertar la tarea"
    
    def deleteTaskTeam(self, id_task, id_team):
        try:
            # Elimina la tarea del equipo
            condition = f"id_tarea = {id_task} AND id_equipo = {id_team}"
            deleted_rows = bdRepository.deleteData("equipo_tareas", condition)

            if deleted_rows > 0:
                return {"message": f"Se eliminó exitosamente la tarea con ID {id_task} del equipo con ID {id_team}"}
            else:
                return {"message":f"No se encontró la tarea con ID {id_task} en el equipo con ID {id_team}"}

        except Exception as e:
            return {"message":f"Error al eliminar la tarea del equipo: {e}"}
    
    
    def updateTaskTeam(self, task_id, updated_task, team_id):
        try:
            # Verifica si la tarea existe en el equipo
            condition = f"id_tarea = {task_id} AND id_equipo = {team_id}"
            existing_task = bdRepository.selectByCondition("equipo_tareas", condition)

            if not existing_task:
                return {"message": f"No se encontró la tarea con ID {task_id} en el equipo con ID {team_id}"}

            # Actualiza la tarea del equipo
            data_update = {**updated_task}
            bdRepository.updateData("tareas", data_update, f"id_tarea = {task_id}")

            return {"message": f"Se actualizó exitosamente la tarea con ID {task_id} en el equipo con ID {team_id}"}

        except Exception as e:
            return {"message": f"error: {e}"}
        
    def getTeam(self, team_id):
      
        try:
            condition = f"id_equipo = {team_id}"
            team = bdRepository.selectByCondition("equipo", condition)
            #destructuramos
            id_equipo, nombre_equipo  = team[0]
            if team:
                return {"id":id_equipo,"name":nombre_equipo}
            else:
                ValueError("equipo no encontrado")

        except Exception as e:
            ValueError("Error en la aplicacion")
            
    def getMembersTeam(self, id_team):
        personas = []
        query = f"""
        SELECT personas.*
        FROM personas
        JOIN equipo_personas ON personas.id_persona = equipo_personas.id_persona
        WHERE equipo_personas.id_equipo = {id_team}"""
        data = bdRepository.myQuerySelect(query)
        if not data:
            return []
         
        for row in data:
            print("row")
            print(row)
            persona_dict = {
            "id_persona": row[0],
            "nombre_persona": row[1],
            "correo": row[2],
            "password": row[3],
            }
            personas.append(persona_dict)
            
       
        return personas
    
    def getTasksTeam(self, id_team):
        query = f"""
        SELECT tareas.*
        FROM tareas
        JOIN equipo_tareas ON tareas.id_tarea = equipo_tareas.id_tarea
        WHERE equipo_tareas.id_equipo = {id_team}
    """
        data = bdRepository.myQuerySelect(query)
        tasks = []
        for row in data:
            task_dict = {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "status": row[3],
             }
            tasks.append(task_dict)
             
        return tasks

     
        
       
        
        
        