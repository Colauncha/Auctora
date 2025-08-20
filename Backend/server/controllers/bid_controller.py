import json
from fastapi import (
    APIRouter, Depends,
    WebSocket, WebSocketDisconnect,
    WebSocketException, status,
)
from sqlalchemy.orm import Session
from server.config import get_db, redis_store
from server.middlewares.auth import (
    permissions, Permissions,
    ServiceKeys
)
from server.schemas import (
    CreateBidSchema, GetBidSchema, UpdateBidSchema,
    APIResponse, BidQuery, PagedResponse
)
from server.utils.ws_manager import WSManager
from server.services import Services, current_user


route = APIRouter(prefix='/bids', tags=['bids'])
wsmanager = WSManager()


@route.post('/')
@permissions(permission_level=Permissions.CLIENT)
async def create(
    user: current_user,
    data: CreateBidSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    data = data.model_dump()
    data["user_id"] = user.id
    data["username"] = user.username
    result = await Services.bidServices.create(db, CreateBidSchema(**data))
    return APIResponse(data=result)


@route.post('/buy_now')
@permissions(permission_level=Permissions.CLIENT)
async def buy_now(
    user: current_user,
    data: CreateBidSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    data = data.model_dump()
    data["user_id"] = user.id
    data["username"] = user.username
    result = await Services.bidServices.buy_now(db, CreateBidSchema(**data))
    return APIResponse(data=result)



@route.put('/{bid_id}')
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.BID)
async def update(
    user: current_user,
    bid_id: str,
    amount: UpdateBidSchema,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    existing_bid = await Services.bidServices.retrieve(db, bid_id)
    result = await Services.bidServices.update(
        amount.amount, exisiting_bid=existing_bid
    )
    return result


@route.get('/')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def list(
    user: current_user,
    query: BidQuery = Depends(BidQuery),
    db: Session = Depends(get_db)
) -> PagedResponse:
    result = await Services.bidServices.list(db, query.model_dump(exclude_unset=True))
    return result


@route.get('/{id}')
@permissions(permission_level=Permissions.AUTHENTICATED)
async def retrieve(
    user: current_user,
    id: str,
    db: Session = Depends(get_db)
) -> APIResponse[GetBidSchema]:
    result = await Services.bidServices.retrieve(db, id)
    return result


@route.websocket('/ws/{id}/{token}')
async def ws_create(
    id: str,
    ws: WebSocket,
    token: str,
    db: Session = Depends(get_db)
):
    _user = await Services.userServices.get_ws_user(ws, db, token)
    await wsmanager.connect(id, ws)
    redis = await redis_store.get_async_redis()
    prev_bids = await redis.get(f'auction:{id}')
    if prev_bids:
        await wsmanager.send_data(json.loads(prev_bids), ws)
    else:
        prev_bids = await Services.bidServices.list_ws(db, id)
        await wsmanager.send_data(prev_bids, ws)
    try:
        watcher = ws.client.host
        await Services.bidServices.add_watcher(db, id, watcher)
        while True:
            data = await ws.receive_json(mode="text")
            if data.get('type') != 'websocket.disconnect':
                data["user_id"] = str(_user.id)
                data["username"] = _user.username
                bids = await Services.bidServices.create_ws(db, CreateBidSchema(**data), wsmanager, ws)
                if bids:
                    await wsmanager.broadcast(id, {'type': 'new_bid', 'payload': bids})
    except WebSocketDisconnect:
        await wsmanager.disconnect(id, ws)
    except WebSocketException as wse:
        await ws.close(code=status.WS_1003_UNSUPPORTED_DATA)
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA) from wse
    except Exception as e:
        await ws.close(code=status.WS_1011_INTERNAL_ERROR)
        raise WebSocketException(code=status.WS_1011_INTERNAL_ERROR) from e
