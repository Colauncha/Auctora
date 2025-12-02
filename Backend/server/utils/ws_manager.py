from fastapi import WebSocket
from functools import lru_cache
from pydantic import BaseModel
from fastapi import WebSocket, WebSocketException, status


class WSManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.chatroom: dict[str, dict[str, dict[str, str] | WebSocket]] = {}

    async def connect(self, auction_id: str, websocket: WebSocket):
        await websocket.accept()
        if auction_id not in self.active_connections:
            self.active_connections[auction_id] = []
        self.active_connections[auction_id].append(websocket)
        await self.count(auction_id)

    async def create_chatroom(
        self,
        chat_id: str,
        buyer_id: str,
        seller_id: str
    ):
        if chat_id in self.chatroom:
            return self.chatroom[chat_id]
        self.chatroom[chat_id] = {
            'allowed_users': {'buyer_id': buyer_id, 'seller_id': seller_id},
            buyer_id: None,
            seller_id: None
        }
        return self.chatroom[chat_id]

    async def enter_chatroom(
        self,
        chat_id: str,
        user_id: str,
        soc: WebSocket,
    ):
        if chat_id not in self.chatroom:
            await soc.send_json({"error": "Chat room doesn't exist"})
            raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)

        allowed_users = self.chatroom[chat_id]['allowed_users'].values()

        if user_id not in allowed_users:
            await soc.send_json({"error": "You are not registered for this chat room"})
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        self.chatroom[chat_id][user_id] = soc
        return self.chatroom[chat_id]

    async def leave_chatroom(
        self,
        chat_id: str,
        user_id: str,
    ):
        if chat_id not in self.chatroom:
            raise WebSocketException(
                code=status.WS_1003_UNSUPPORTED_DATA,
                reason="Chat room doesn't exist"
            )

        if user_id not in self.chatroom[chat_id]:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="You are not registered for this chat room"
            )

        self.chatroom[chat_id][user_id] = None
        return self.chatroom[chat_id]


    async def message_chatroom(
        self,
        chat_id,
        user_id,
        message,
        type = 'new_message'
    ):
        chatroom = self.chatroom.get(chat_id, {})
        payload = message.model_dump() if isinstance(message, BaseModel) else message
        sender_socket = chatroom.get(user_id)
        try:
            for key, socket in chatroom.items():
                if key == 'allowed_users' or key == user_id:
                    continue
                if socket is None:
                    return
                
                await socket.send_json({
                    'type': type,
                    'payload': payload
                })
        except Exception as e:
            await sender_socket.send_json({'notice': 'Message not Delivered'})
            print(e)
        
        if sender_socket is not None:
            try:
                await sender_socket.send_json({'notice': 'Message Delivered'})
            except Exception as e:
                await sender_socket.send_json({'notice': 'Message not Delivered'})
                print(e)

    async def disconnect(self, auction_id: str, websocket: WebSocket):
        self.active_connections[auction_id].remove(websocket)
        if len(self.active_connections[auction_id]) <= 0:
            del self.active_connections[auction_id]
        else:
            await self.count(auction_id)

    async def count(self, id: str):
        count = len(self.active_connections[id])
        await self.broadcast(id, {"type": "count", "Watchers": count})

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_data(self, data: dict | list, websocket: WebSocket):
        await websocket.send_json({'type': 'bids', 'payload': data})

    async def broadcast(self, auction_id: str, data: any):
        for connection in self.active_connections[auction_id]:
            await connection.send_json(data)



@lru_cache(maxsize=1)
def get_wsmanager():
    return WSManager()