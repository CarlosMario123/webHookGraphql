from ariadne import gql

RegisterDefs = gql("""
  input LoginInput{
      correo:String
       password:String
  }
  
  type AuthPayload {
    token: String
  }
  extend type Mutation {
    login(loginInput: LoginInput):AuthPayload
    register(personaInput: PersonaInput):Persona
}
    
""")