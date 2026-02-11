from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str) -> None:
        self.active_connections.pop(client_id, None)

    async def broadcast(self, message: str) -> None:
        for websocket in list(self.active_connections.values()):
            await websocket.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket, client_id: str = "anonymous") -> None:
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
