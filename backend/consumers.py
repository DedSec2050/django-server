from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CentralServerConsumer(AsyncWebsocketConsumer):
    connected_clients = {}  # Store connected clients

    async def connect(self):
        self.client_ip = self.scope["client"][0]
        self.client_type = self.scope["path"]  # Identify Next.js or Golang
        await self.accept()
        
        # Store connection based on type
        if "/ws/server/" in self.client_type:  # Golang Clients
            self.connected_clients[self.channel_name] = {"ip": self.client_ip, "type": "golang"}
        elif "/ws/frontend/" in self.client_type:  # Next.js Clients
            self.connected_clients[self.channel_name] = {"ip": self.client_ip, "type": "frontend"}

        await self.broadcast_clients()

    async def disconnect(self, close_code):
        if self.channel_name in self.connected_clients:
            del self.connected_clients[self.channel_name]
        await self.broadcast_clients()

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Broadcast data to all Next.js frontend clients
        for channel, info in self.connected_clients.items():
            if info["type"] == "frontend":
                await self.channel_layer.send(channel, {
                    "type": "send_data",
                    "message": data
                })

    async def send_data(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def broadcast_clients(self):
        """Notify Next.js UI about connected clients."""
        clients_info = {"clients": list(self.connected_clients.values())}
        for channel, info in self.connected_clients.items():
            if info["type"] == "frontend":
                await self.channel_layer.send(channel, {
                    "type": "send_data",
                    "message": clients_info
                })
