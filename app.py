# main.py
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from schemas import allDefs
import uvicorn
from resolvers import allResolvers


schema = make_executable_schema(allDefs,allResolvers)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)