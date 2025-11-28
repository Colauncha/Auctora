from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect
)

from server.schemas import (
    APIResponse,
    GetChatSchema,
    ConversationSchema
)
from server.middlewares.auth import Permissions, permissions, ServiceKeys
from server.utils.ws_manager import get_wsmanager, WSManager
from server.services import (
    current_user,
    get_chat_service,
    ChatServices,
    AuthServices
)


route = APIRouter(prefix="/chats", tags=['Chats'])


@route.get("")
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.CHAT)
async def retrieve(
    user: current_user,
    chat_id: str,
    chatServices: ChatServices = Depends(get_chat_service)
) -> APIResponse[GetChatSchema]:
    chat = await chatServices.get_chat_by_id(chat_id)
    return APIResponse(data=chat)


@route.patch("/send")
@permissions(permission_level=Permissions.CLIENT, service=ServiceKeys.CHAT)
async def message(
    user: current_user,
    chat_id: str,
    data: ConversationSchema,
    chatServices: ChatServices = Depends(get_chat_service)
) -> APIResponse[GetChatSchema]:
    data.sender_id = str(user.id)
    chat = await chatServices.update_chat(
        chat_id=chat_id, chat_data=data
    )
    return APIResponse(data=chat)


@route.websocket('/ws/{chat_id}')
async def connect(
    chat_id: str,
    ws: WebSocket,
    wsmanager: WSManager = Depends(get_wsmanager),
    chatServices: ChatServices = Depends(get_chat_service)
):
    user = await AuthServices.get_ws_user(ws)
    chat = await chatServices.get_chat_by_id(chat_id)
    await wsmanager.create_chatroom(
        str(chat.id), str(chat.buyer_id), str(chat.seller_id)
    )
    await wsmanager.enter_chatroom(str(chat.id), str(user.id), ws)
    try:
        await ws.accept()
        if chat:
            await ws.send_json(chat.model_dump())
        while True:
            data = await ws.receive_json()
            if data.get('type') != 'websocket.disconnect':
                data = ConversationSchema.model_validate(data)
                data.sender_id = str(user.id)
                new_convo = await chatServices.update_chat(chat_id, data)
                if new_convo:
                    data.status = "delivered"
                    await wsmanager.message_chatroom(
                        chat_id, str(user.id), data
                    )
            else:
                print(data)
    except WebSocketDisconnect:
        await wsmanager.leave_chatroom(chat_id, str(user.id))

    except Exception:
        await ws.close(code=1011)
        await wsmanager.leave_chatroom(chat_id, str(user.id))

