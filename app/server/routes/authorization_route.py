from server.security.auth import (signJWT, signupJWT)
from server.database import (add_userdata, check_userdata)
from server.security.auth_bearer import JWTBearer
from fastapi import APIRouter, Body, Header, Request, Depends
from server.models.user_model import (UserSchema, UserLoginSchema)
from fastapi.encoders import jsonable_encoder

router = APIRouter()


async def check_user(data: UserLoginSchema):
    is_valid_apikey = await check_userdata(data)
    return is_valid_apikey

@router.post("/user/signup", dependencies=[Depends(JWTBearer())])
async def register_user(user: UserSchema = Body(...)):
    user_payload = jsonable_encoder(user)
    new_userpayload = await add_userdata(user_payload)
    return signupJWT(user)


@router.post("/user/login")
async def user_login(user: UserLoginSchema = Body(...)):
    user_login = await check_user(user)
    if user_login:
        return signJWT(user_login)
    else:
        return {
            "error": "Wrong login details!"
        }
