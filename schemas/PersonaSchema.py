from ariadne import gql

UserDefs = gql("""
   type Persona {
    id_persona: ID!
    nombre_persona: String!
    correo: String!
    password: String!
}

 input PersonaInput {
    nombre_persona: String
    correo: String
    password: String
  }
""")