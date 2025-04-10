from fastapi import FastAPI, Request                                                          
from strawberry.fastapi import GraphQLRouter                                                  
from contextlib import asynccontextmanager                                                    
from mock_spotify_rest_api_client.client import Client                                        
from api.schema import schema                                                                 
                                                                                              
                                                                                              
@asynccontextmanager                                                                          
async def lifespan(app: FastAPI):                                                             
    """Async context manager for managing the application lifecycle.                          
                                                                                              
    Handles setup and teardown of the Spotify API client connection.                          
                                                                                              
    Args:                                                                                     
        app: The FastAPI application instance                                                 
                                                                                              
    Yields:                                                                                   
        dict: Context containing the initialized Spotify client                               
    """                                                                                       
    async with Client(                                                                        
        base_url="https://spotify-demo-api-fe224840a08c.herokuapp.com/v1"                     
    ) as client:                                                                              
        yield {"spotify_client": client}                                                      
                                                                                              
                                                                                              
async def context_getter(request: Request) -> dict:                                           
    """Retrieves the execution context for GraphQL operations.                                
                                                                                              
    Provides the Spotify client to GraphQL resolvers via the request context.                 
                                                                                              
    Args:                                                                                     
        request: The incoming FastAPI request                                                 
                                                                                              
    Returns:                                                                                  
        dict: Context dictionary containing the Spotify client                                
    """                                                                                       
    spotify_client = request.state.spotify_client                                             
    return {"spotify_client": spotify_client}                                                 
                                                                                              
                                                                                              
# Initialize FastAPI application with lifespan management                                     
app = FastAPI(                                                                                
    lifespan=lifespan,                                                                        
    title="Spotify GraphQL API",                                                              
    description="GraphQL wrapper for the Spotify REST API",                                   
    version="1.0.0"                                                                           
)                                                                                             
                                                                                              
# Configure GraphQL router                                                                    
graphql_router = GraphQLRouter(                                                               
    schema,                                                                                   
    path="/",                                                                                 
    graphql_ide="apollo-sandbox",  # Enables Apollo Sandbox for development                   
    context_getter=context_getter                                                             
)                                                                                             
                                                                                              
# Mount the GraphQL endpoint                                                                  
app.include_router(graphql_router)
