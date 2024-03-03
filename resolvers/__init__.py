from .TeamResolver import teamResolver
from .UserResolver import userResolver
from .WebHookResolver import webHookResolver

#allResolvers manda todos lo resolver disponibles
allResolvers = teamResolver  + userResolver + webHookResolver