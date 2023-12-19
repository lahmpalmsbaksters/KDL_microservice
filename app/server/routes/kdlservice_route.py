from server.security.auth_bearer import JWTBearer
from server.models.response_model import (ResponseModel, ErrorResponseModel)
from server.security.auth import (check_apikey_isvalid)
from server.database import (create_log)
from fastapi import APIRouter, Header, HTTPException, Request, Depends
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from decouple import config
import httpx

kdl_api_endpoint = config("KDL_API_ENDPOINT")

router = APIRouter()


@router.get("/", dependencies=[Depends(JWTBearer())], response_description="Health check KDL service")
async def health_check(request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_apikey_isvalid(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{kdl_api_endpoint}/recommender/test/")
                if response.status_code == 200:
                    log_request = {
                        "apikey": request.headers.get("apikey"),
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": response.json()
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await create_log(log_request_body)
                    return ResponseModel(response.json(), "Request to KDL service API successful")
                else:
                    log_request = {
                        "apikey": request.headers.get("apikey"),
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to KDL service API failed')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await create_log(log_request_body)
                    raise HTTPException(
                        status_code=response.status_code, detail="Request to KDL service API failed")
        except Exception:
            log_request = {
                "apikey": request.headers.get("apikey"),
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": request.url,
                "headers": str(request.headers) if request.headers else "None",
                "client": str(request.client.host) if request.client.host else "None",
                "response": str('Internal Server Error')
            }
            log_request_body = jsonable_encoder(log_request)
            await create_log(log_request_body)
            return ErrorResponseModel('error', 500, 'Internal Server Error')
