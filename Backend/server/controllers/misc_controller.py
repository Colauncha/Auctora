import httpx

from fastapi import Depends
from fastapi.routing import APIRouter
from server.config.app_configs import app_configs
from server.schemas import BanksQuery
from server.middlewares.exception_handler import ExcRaiser400


route = APIRouter(prefix='/misc', tags=['Miscellaneous'])


@route.get('/banks')
async def banks(query: BanksQuery = Depends()):
    paystack_url = f'{app_configs.paystack.PAYSTACK_URL}/bank'
    secret_key = 'sk_live_cff92154fddb8bfc33622a2e968882b2f078c987'# app_configs.paystack.SECRET_KEY
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    param = query.model_dump()
    async with httpx.AsyncClient() as client:
        response = await client.get(paystack_url, headers=headers, params=param)
    if response.status_code != 200:
        raise ExcRaiser400(detail=response.json())
    return response.json()


@route.get('/states')
async def states():
    states = [
        "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
        "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
        "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto",
        "Taraba", "Yobe", "Zamfara"
    ]
    return states
