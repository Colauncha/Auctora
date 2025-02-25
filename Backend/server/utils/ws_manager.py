from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, auction_id: str, websocket: WebSocket):
        await websocket.accept()
        if auction_id not in self.active_connections:
            self.active_connections[auction_id] = []
        self.active_connections[auction_id].append(websocket)
        await self.count(auction_id)

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
        await websocket.send_json(data)

    async def broadcast(self, auction_id: str, data: any):
        for connection in self.active_connections[auction_id]:
            await connection.send_json(data)