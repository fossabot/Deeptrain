import time
from typing import List
from controller import get_user_from_name
from dwebsocket import require_websocket
import websocket

user_image = "/static/images/chat_user.png"
host_image = "https://cdn-icons-png.flaticon.com/128/6908/6908194.png"


class IMClient(websocket.WebClient):
    group: "IMServerClientGroup"

    def __init__(self, *args, **kwargs):
        super(IMClient, self).__init__(*args, **kwargs)

    def receiveEvent(self, obj: dict) -> None:
        if isinstance(obj, dict):
            message = str(obj.get("message", "")).strip()[:500]
            if message:
                self.group.group_send(self, message)

    def send(self, username="", message="", uid=0, image="", is_html: bool = False, identity: str = "User") -> None:
        super(IMClient, self).send({
            'username': username,
            'id': uid,
            'image_path': image,
            'content': message,
            'self': uid == self.id,
            'is_html': is_html,
            'identity': identity,
            'time': int(time.time()),
        })

    def disconnectEvent(self) -> None:
        super(IMClient, self).disconnectEvent()


class IMServerClientGroup(websocket.WebClientGroup):
    _socks: List[IMClient]
    _client_type = IMClient

    def host_send(self, message=""):
        for client in self.get_available_clients():
            client: IMClient
            client.send("host", message, -1, host_image, False, "ServerHost")

    def group_send(self, sender: IMClient, message="", image=user_image):
        for client in self.get_available_clients():
            client: IMClient
            client.send(sender.username, message, client.id, image, client.admin, client.identity)

    def leaveEvent(self, client: IMClient):
        self.host_send(f"{client.username} 离开了, 当前人数 {self.get_available_clients_length()}.")

    def joinEvent(self, client: IMClient):
        self.host_send(f"{client.username} 加入服务器, 当前人数 {self.get_available_clients_length()}.")


group = IMServerClientGroup()


@require_websocket
def chat(request, token) -> None:
    ws = group.add_client(request, token)
