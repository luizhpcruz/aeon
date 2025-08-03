import asyncio
import json
import websockets
from datetime import datetime
from typing import Dict, List, Set
import uuid

class AEONChatServer:
    def __init__(self):
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.rooms: Dict[str, Set[str]] = {}
        self.user_profiles: Dict[str, dict] = {}
        self.message_history: List[dict] = []
        
    async def register_client(self, websocket, user_data):
        """Registra um novo cliente/funcionário"""
        user_id = user_data.get("govbr_id", str(uuid.uuid4()))
        self.clients[user_id] = websocket
        self.user_profiles[user_id] = {
            "name": user_data.get("name", "Funcionário"),
            "department": user_data.get("department", "Geral"),
            "role": user_data.get("role", "Operador"),
            "online": True,
            "last_seen": datetime.now().isoformat()
        }
        
        # Notifica outros usuários que alguém entrou online
        await self.broadcast_user_status(user_id, "online")
        print(f"✅ Usuário {self.user_profiles[user_id]['name']} conectado")
        
    async def unregister_client(self, user_id):
        """Remove cliente quando desconecta"""
        if user_id in self.clients:
            del self.clients[user_id]
        if user_id in self.user_profiles:
            self.user_profiles[user_id]["online"] = False
            self.user_profiles[user_id]["last_seen"] = datetime.now().isoformat()
        await self.broadcast_user_status(user_id, "offline")
        
    async def create_room(self, room_name: str, creator_id: str, room_type: str = "group"):
        """Cria sala/grupo de conversa"""
        room_id = f"{room_type}_{uuid.uuid4().hex[:8]}"
        self.rooms[room_id] = {creator_id}
        
        room_info = {
            "id": room_id,
            "name": room_name,
            "type": room_type,  # "group", "emergency", "ssma", "department"
            "creator": creator_id,
            "created_at": datetime.now().isoformat(),
            "members": [creator_id]
        }
        
        # Salva informação da sala
        await self.broadcast_to_room(room_id, {
            "type": "room_created",
            "room": room_info
        })
        
        return room_id
        
    async def join_room(self, room_id: str, user_id: str):
        """Adiciona usuário a uma sala"""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(user_id)
        
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "user_name": self.user_profiles.get(user_id, {}).get("name", "Usuário"),
            "timestamp": datetime.now().isoformat()
        })
        
    async def send_message(self, message_data: dict):
        """Envia mensagem para usuário ou grupo"""
        message = {
            "id": str(uuid.uuid4()),
            "from_user": message_data["from_user"],
            "from_name": self.user_profiles.get(message_data["from_user"], {}).get("name", "Usuário"),
            "content": message_data["content"],
            "message_type": message_data.get("type", "text"),  # text, image, document, alert, emergency
            "timestamp": datetime.now().isoformat(),
            "priority": message_data.get("priority", "normal")  # normal, high, emergency
        }
        
        # Adiciona informações especiais para mensagens SSMA
        if message_data.get("ssma_context"):
            message["ssma_context"] = message_data["ssma_context"]
            message["document_ref"] = message_data.get("document_ref")
            
        self.message_history.append(message)
        
        # Envia para destinatário específico ou grupo
        if "to_user" in message_data:
            await self.send_direct_message(message, message_data["to_user"])
        elif "to_room" in message_data:
            await self.broadcast_to_room(message_data["to_room"], {
                "type": "message",
                "message": message
            })
            
    async def send_direct_message(self, message: dict, to_user: str):
        """Envia mensagem direta entre dois usuários"""
        if to_user in self.clients:
            await self.clients[to_user].send(json.dumps({
                "type": "direct_message",
                "message": message
            }))
            
    async def broadcast_to_room(self, room_id: str, data: dict):
        """Envia mensagem para todos os membros de uma sala"""
        if room_id in self.rooms:
            for user_id in self.rooms[room_id]:
                if user_id in self.clients:
                    await self.clients[user_id].send(json.dumps(data))
                    
    async def broadcast_user_status(self, user_id: str, status: str):
        """Notifica mudança de status do usuário"""
        status_message = {
            "type": "user_status",
            "user_id": user_id,
            "status": status,
            "user_profile": self.user_profiles.get(user_id, {}),
            "timestamp": datetime.now().isoformat()
        }
        
        # Envia para todos os clientes conectados
        for client in self.clients.values():
            await client.send(json.dumps(status_message))
            
    async def send_emergency_alert(self, alert_data: dict):
        """Envia alerta de emergência para todos os usuários"""
        emergency_message = {
            "type": "emergency_alert",
            "alert": {
                "id": str(uuid.uuid4()),
                "title": alert_data["title"],
                "description": alert_data["description"],
                "location": alert_data.get("location", "Não especificado"),
                "severity": alert_data.get("severity", "high"),  # low, medium, high, critical
                "sender": alert_data["sender"],
                "timestamp": datetime.now().isoformat(),
                "requires_acknowledgment": alert_data.get("requires_ack", True)
            }
        }
        
        # Envia para todos os usuários conectados
        for client in self.clients.values():
            await client.send(json.dumps(emergency_message))
            
    async def handle_client_message(self, websocket, message: str):
        """Processa mensagens recebidas dos clientes"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "register":
                await self.register_client(websocket, data["user_data"])
            elif message_type == "send_message":
                await self.send_message(data["message_data"])
            elif message_type == "create_room":
                room_id = await self.create_room(
                    data["room_name"], 
                    data["creator_id"], 
                    data.get("room_type", "group")
                )
                await websocket.send(json.dumps({
                    "type": "room_created",
                    "room_id": room_id
                }))
            elif message_type == "join_room":
                await self.join_room(data["room_id"], data["user_id"])
            elif message_type == "emergency_alert":
                await self.send_emergency_alert(data["alert_data"])
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Formato de mensagem inválido"
            }))

# Servidor WebSocket para comunicação em tempo real
chat_server = AEONChatServer()

async def handle_websocket(websocket, path):
    """Gerencia conexões WebSocket"""
    user_id = None
    try:
        async for message in websocket:
            await chat_server.handle_client_message(websocket, message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if user_id:
            await chat_server.unregister_client(user_id)

def start_chat_server(host="0.0.0.0", port=8765):
    """Inicia o servidor de chat"""
    print(f"🚀 AEON Chat Server iniciado em ws://{host}:{port}")
    return websockets.serve(handle_websocket, host, port)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_chat_server())
    asyncio.get_event_loop().run_forever()
