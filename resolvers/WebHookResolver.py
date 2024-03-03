from ariadne import QueryType, MutationType
from uuid import uuid4
from auth.Auth import verify_token
from repositorios.webHookRepository import getWebhookUrlsByEvent,createWebhook
WebHookQuery = QueryType()
WebHookMutation = MutationType()

@WebHookQuery.field("getWebhookUrlsByEvent")
def getWebhookUrlsByEvent1(*_,evento):
    return getWebhookUrlsByEvent(evento)

@WebHookMutation.field("createWebhook")
@verify_token
def createWebhook1(*_, webHook):   
    return createWebhook(webHook) 
    
    
webHookResolver = [WebHookQuery,WebHookMutation]    
    