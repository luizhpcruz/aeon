from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: dict = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Processa diferentes tipos de mensagem
            if message_data["type"] == "chat_message":
                # Mensagem de chat normal
                formatted_message = json.dumps({
                    "type": "chat_message",
                    "from": user_id,
                    "content": message_data["content"],
                    "timestamp": message_data.get("timestamp")
                })
                await manager.broadcast(formatted_message)
                
            elif message_data["type"] == "ssma_alert":
                # Alerta SSMA prioritário
                alert_message = json.dumps({
                    "type": "ssma_alert",
                    "from": user_id,
                    "alert_level": message_data["alert_level"],
                    "location": message_data["location"],
                    "description": message_data["description"],
                    "timestamp": message_data.get("timestamp")
                })
                await manager.broadcast(alert_message)
                
            elif message_data["type"] == "document_share":
                # Compartilhamento de documento APR/IT/PT
                doc_message = json.dumps({
                    "type": "document_share",
                    "from": user_id,
                    "document_id": message_data["document_id"],
                    "document_type": message_data["document_type"],
                    "title": message_data["title"],
                    "timestamp": message_data.get("timestamp")
                })
                await manager.broadcast(doc_message)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        disconnect_message = json.dumps({
            "type": "user_disconnect",
            "user_id": user_id
        })
        await manager.broadcast(disconnect_message)

@router.get("/online_users")
async def get_online_users():
    """Retorna lista de usuários conectados"""
    return {"online_users": list(manager.user_connections.keys())}

@router.post("/send_notification")
async def send_notification(notification_data: dict):
    """Envia notificação para todos os usuários"""
    message = json.dumps({
        "type": "notification",
        "title": notification_data["title"],
        "content": notification_data["content"],
        "priority": notification_data.get("priority", "normal")
    })
    await manager.broadcast(message)
    return {"status": "notification_sent"}
