from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.server.routes.authorization_route import router as authorization_router
from app.server.routes.kdlservice_route import router as kdlservice_route
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

app.include_router(kdlservice_route, tags=[
                   "kdl_service"], prefix=f"{api_endpoint}/kdl_service")
