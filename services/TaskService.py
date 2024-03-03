from datetime import datetime  # Asegúrate de importar cualquier módulo necesario
from repositorios.BdRepository import BaseRepository

bdRepository = BaseRepository()


class TaskService:
    def createTask(self, nombre_tarea, descripcion, estatus):

        # Crea una nueva tarea
        nueva_tarea = {
            "nombre_tarea": nombre_tarea,
            "descripcion": descripcion,
            "estatus": estatus,
        }

        # Inserta la tarea
        respuesta = bdRepository.insertAndReturn("tareas", nueva_tarea)
        return respuesta
