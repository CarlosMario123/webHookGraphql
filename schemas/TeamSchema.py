from ariadne import gql

TeamDefs = gql(""" 
    type Team{
        id:ID!
        name:String
    }
    
      type Query{
         getTeams:[Team!]
         getTeam(id_team:Int):Team
         getMembersTeam(id_team:Int):[Persona]
         getTasksTeam(id_team:Int):[Task]
     }
     
     type TeamMsg{
         message:String
     }
     
    type Mutation {
      createTeam(name:String):Team
      addMemberTeam(correo:String,id_team:Int):String
      deleteMemberTeam(correo:String,id_team:Int):TeamMsg
      addTaskTeam(task:TaskInput,idTeam:Int):String
      deleteTaskTeam(idTask:Int,idTeam:Int): TeamMsg
      updateTaskTeam(taskId: Int, updatedTask: TaskInput,teamId:Int): TeamMsg
    }                    
""")