from ariadne import gql

WhDefs = gql("""
    type webhook{
        id:ID
        url:String
        eventos:[String]
    }
    
    input WebhookInput{
        url:String
        eventos:[String]
    }
    
   extend type Query{
       getWebhookUrlsByEvent(evento: String!): [String] 
   }
   
   extend  type Mutation{
       createWebhook(webHook:WebhookInput):String
   }
     
""")