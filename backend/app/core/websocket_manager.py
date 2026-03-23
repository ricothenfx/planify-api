from fastapi import WebSocket
import json


class WebScoketManager:
    def __init__(self):
        # Dictionary: project_id -> list of active connections
        self.connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, project_id: str):
        await websocket.accept()
        if project_id not in self.connections:
            self.connections[project_id] = []
        self.connections[project_id].append(websocket)
    

    def disconnect(self, websocket: WebSocket, project_id: str):
        if project_id in self.connections:
            self.connections[project_id].remove(websocket)
            if not self.connections[project_id]:
                del self.connections[project_id]
    
    async def broadcast_to_project(self, project_id: str, message: dict):
        if project_id not in self.connections:
            return
        disconnected = []
        for websocket in self.connections[project_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception:
                disconnected.append(websocket)
        for websocket in disconnected:
            self.disconnect(websocket=websocket, project_id=project_id)


# Singleton - an instance used by all
ws_manager = WebScoketManager()