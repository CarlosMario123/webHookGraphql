from ariadne import QueryType, MutationType
from uuid import uuid4
from db.db import Database
from repositorios.RegisterRepository import ResgisterRepository
userQuery =  QueryType()
userMutation = MutationType()

registerRepository = ResgisterRepository()


@userMutation.field("register")
def register(*_,personaInput):
    nombre = personaInput.get('nombre_persona')
    correo = personaInput.get('correo')
    password = personaInput.get('password')
    return registerRepository.registerUser(nombre,correo,password)


@userMutation.field("login")
def login(*_,loginInput):
    correo = loginInput.get("correo")
    password = loginInput.get('password')
    return registerRepository.login(correo,password)

userResolver = [userQuery,userMutation]