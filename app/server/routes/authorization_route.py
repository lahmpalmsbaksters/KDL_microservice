# from server.security.auth import (check_api_data, signJWT, signupJWT)
# from server.models.apikey import (
#     ErrorResponseModel,
#     ResponseModel,
#     ApikeySchema,
#     UserLoginSchema
# )
# from server.database import (
#     retrieve_apikeys,
#     add_apikey,
#     add_log,
#     check_userdata,
#     check_access_service
# )
# from server.security.auth_bearer import JWTBearer
from fastapi import APIRouter, Body, Header, Request, Depends
# from fastapi.encoders import jsonable_encoder
# from datetime import datetime
# from decouple import config

router = APIRouter()


@router.get('/')
async def test():
    return "test"
# @router.post("/user/signup", dependencies=[Depends(JWTBearer())], tags=["OAuth"])
# async def create_user(user: ApikeySchema = Body(...)):
#     apikey = jsonable_encoder(user)
#     new_api = await add_apikey(apikey)
#     return signupJWT(user)
