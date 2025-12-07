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
    user, db = await AuthServices.get_ws_user(ws)
    db.close()
    chat = await chatServices.get_chat_by_id(chat_id)
    await wsmanager.create_chatroom(
        str(chat.id), str(chat.buyer_id), str(chat.seller_id)
    )
    await wsmanager.enter_chatroom(str(chat.id), str(user.id), ws)
    try:
        if chat:
            await ws.send_json({'type': 'chat' ,'payload': chat.model_dump()})
        while True:
            data = await ws.receive_json()
            data_type = data.get('type')
            if data_type == 'send_message':
                data = ConversationSchema.model_validate(data.get('payload'))
                data.sender_id = str(user.id)
                new_convo = await chatServices.update_chat(chat_id, data)
                if new_convo:
                    data.status = "delivered"
                    await wsmanager.message_chatroom(
                        chat_id, str(user.id), data
                    )
            elif data_type == 'read_message':
                data = data.get('payload')
                chat = await chatServices.mark_read(
                    chat_id, data.get('chat_number')
                )
                await wsmanager.message_chatroom(
                    chat_id, str(user.id), chat, type='read_message'
                )
            else:
                print(data)
    except WebSocketDisconnect:
        await wsmanager.leave_chatroom(chat_id, str(user.id))

    except Exception:
        await ws.close(code=1011)
        await wsmanager.leave_chatroom(chat_id, str(user.id))

