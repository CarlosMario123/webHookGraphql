from ariadne import gql

TaskDefs = gql("""
    type Task {
        id: ID!
        name: String
        description: String
        status: String
    }
    
    
    input TaskInput {
    nombre_tarea: String
    description: String
    status: String
}

  type outputTask{
       name: String
        description: String
        status: String
  }
""")