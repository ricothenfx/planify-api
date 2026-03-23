from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import JWTError
from app.core.websocket_manager import ws_manager
from app.core.security import decode_access_token


router = APIRouter(
    tags=["WebSocket"],
)


@router.websocket("/ws/projects/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: str,
    token: str = Query(...),
):
    # Validate token before accept connection
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=4001)
            return
    except JWTError:
        await websocket.close(code=4001)
        return
    
    await ws_manager.connect(websocket=websocket, project_id=project_id)
    try:
        await websocket.send_text(f'{{"type": "connected", "project_id": "{project_id}"}}')
        while True:
            # Keep connection alive - wait message from client
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket=websocket, project_id=project_id)