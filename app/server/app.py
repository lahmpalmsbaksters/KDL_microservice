from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.authorization_route import router as authorization_router
from decouple import config

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_endpoint = config("API_ENDPOINT")


app.include_router(authorization_router, tags=[
                   "authorization_service"], prefix=f"{api_endpoint}/authorization")
