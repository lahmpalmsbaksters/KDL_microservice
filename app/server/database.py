import motor.motor_asyncio
from bson.objectid import ObjectId
import os
from decouple import config
from passlib.context import CryptContext
from fastapi import HTTPException


MONGO_DETAILS = config("DB_URL")
MONGO_DB = config("MONGO_DB")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client[MONGO_DB]

users_collection = database.get_collection("users_collection")
logs_collection = database.get_collection("logs_collection")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "apikey": user["apikey"],
    }


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def add_userdata(apikey_data: dict) -> dict:
    payload = {'fullname': apikey_data["fullname"], 'email': apikey_data["email"],
               'password': get_password_hash(apikey_data["password"]), 'apikey': apikey_data["apikey"]}
    user_data = await users_collection.insert_one(payload)
    new_userdata = await users_collection.find_one({"_id": user_data.inserted_id})
    return user_helper(new_userdata)


async def check_userdata(user_data: dict) -> dict:
    result = await users_collection.find_one({"email": user_data.email})

    if result:
        check = True if result["email"] == user_data.email and verify_password(
            user_data.password, result["password"]) else False
        if check:
            result_data = {
                "email": result.get("email"),
                "apikey": result.get("apikey"),
            }
            return result_data
    else:
        return False


async def check_apikey(id: str) -> dict:
    result = await users_collection.find_one({"apikey": id})
    if result:
        return True
    else:
        return False


async def create_log(log_data: dict) -> dict:
    log = await logs_collection.insert_one(log_data)
    new_log = await logs_collection.find_one({"_id": log.inserted_id})
    return (new_log)
