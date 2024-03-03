import bcrypt
from repositorios.BdRepository import BaseRepository
from auth.Auth import generate_token

#creamos un objeto de tipos auth

bdRepository = BaseRepository()
class ResgisterRepository:
    def registerUser(self,nombre,correo,password):
        condicion = f"correo =  '{correo}'"
        userExists = bdRepository.selectByCondition("personas",condicion) #verifamos que exista el usuario
        print(userExists)
        if userExists != None:
            raise ValueError("usuario ya existente")
        
        hashPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        dataInsert = {"nombre_persona": nombre, "correo": correo, "contraseña": hashPassword}
        respuesta = bdRepository.insertData("personas",dataInsert)
        
        return {"nombre_persona": nombre, "correo": correo, "password": str(hashPassword)} if respuesta else {"mensaje": "Error en el registro"}
    
    def login(self, correo, password):
    # Verifica si el usuario existe en la base de datos
        user_data = bdRepository.selectByCondition("personas", f"correo = '{correo}'")
    
        if not user_data:
            raise ValueError("Usuario no encontrado")

    # Extrae el hash de la contraseña almacenada en la base de datos
        stored_password_hash = user_data[0][3]

    # Verifica si la contraseña proporcionada coincide con el hash almacenado
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            raise ValueError("Contraseña incorrecta")

    # Genera un token de autenticación
        user_id = user_data[0][0]  # Asumiendo que el ID del usuario está en la posición 0
        token = generate_token(user_id)

        return {"token": token}



        
        