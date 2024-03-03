from ariadne import QueryType, MutationType
from uuid import uuid4
from db.db import Database
from repositorios.TeamRepository import TeamRepository
from auth.Auth import verify_token
from services.webHookServices import response_to_url
import aiohttp
import asyncio
TeamQuery = QueryType()
TeamMutation = MutationType()

#creamos una instancia de teamRepository
teamRepository = TeamRepository()

#aca ira todos las query
@TeamQuery.field("getTeams")
@verify_token
def resolveGetTeams(*_):
    data = teamRepository.get_teams()
    asyncio.create_task(response_to_url("GET_TEAMS",data))
    return data

@TeamQuery.field("getTeam")
@verify_token
def getTeam(*_,id_team):
    data = teamRepository.getTeam(id_team)
    asyncio.create_task(response_to_url("GET_TEAM",data))
    return data

@TeamQuery.field("getMembersTeam")
@verify_token
def getMembersTeam(*_,id_team):
    data = teamRepository.getMembersTeam(id_team)
    asyncio.create_task(response_to_url("GET_MEMBERS_TEAM",data))
    return data

@TeamQuery.field("getTasksTeam")
@verify_token
def getTasksTeam(*_,id_team):
    data = teamRepository.getTasksTeam(id_team)
    asyncio.create_task(response_to_url("GET_TASKS_TEAM",data))
    return data
    

#aca iran todos las mutacioes
@TeamMutation.field("createTeam")
@verify_token#decorador que verifica la autenticacion
def createTeam(*_,name):
    data = teamRepository.createTeam(name)
    asyncio.create_task(response_to_url("CREATE_TEAM",data))
    return data
      
@TeamMutation.field("addMemberTeam")
@verify_token
def addMemberTeam(*_,correo,id_team):
    data = teamRepository.addMemberTeam(correo,id_team)
    asyncio.create_task(response_to_url("ADD_MEMBER_TEAM",data))
    return data

@TeamMutation.field("deleteMemberTeam")
@verify_token
def deleteMemberTeam(*_,correo,id_team):
    data = teamRepository.deleteMemberTeam(correo,id_team)
    asyncio.create_task(response_to_url("DELETE_MEMBER_TEAM",data))
    return data

@TeamMutation.field("addTaskTeam")
@verify_token
def addTaskTeam(*_,task,idTeam):
    nombre = task.get("nombre_tarea")
    descripcion = task.get("description")
    status = task.get("status")
    data = teamRepository.createTaskTeam(nombre,descripcion,status,idTeam)
    enviar = {"info":data}
    asyncio.create_task(response_to_url("ADD_TASK_TEAM",enviar))
    return  data

@TeamMutation.field("deleteTaskTeam")
@verify_token
def deleteTaskTeam(*_,idTask,idTeam):
    data = teamRepository.deleteTaskTeam(idTask,idTeam)
    asyncio.create_task(response_to_url("DELETE_TASK_TEAM",data))
    return data

@TeamMutation.field("updateTaskTeam")
@verify_token
def updateTaskTeam(*_,taskId,updatedTask,teamId):
    data = teamRepository.updateTaskTeam(taskId,updatedTask,teamId)
    asyncio.create_task(response_to_url("UPDATE_TASK_TEAM",data))
    return data
#mandar Resolver

teamResolver = [TeamQuery,TeamMutation]