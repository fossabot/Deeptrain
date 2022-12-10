import json
from typing import List, Any, Union
import jwt.exceptions
from dwebsocket.backends.default import websocket
from DjangoWebsite.settings import CODING
from controller import webtoken_validate
from user.models import User, Profile, identities


class AbstractSocket(object):
    group: "AbstractGroup"

    def __init__(self, sock: websocket.DefaultWebSocket, group: "AbstractGroup", _start: bool = False):
        self.__sock = sock
        self.group = group
        self.connectEvent()
        if _start:
            self.listen()

    def get_socket(self) -> websocket.DefaultWebSocket:
        return self.__sock

    def read(self) -> Union[str, None]:  # inherit
        _read = self.__sock.read()
        return _read.decode(CODING).strip() if isinstance(_read, bytes) else None

    def is_alive(self) -> bool:
        return not self.__sock.is_closed()

    def listen(self):
        while self.is_alive():
            _read = self.read()
            if _read is not None:
                self.receiveEvent(_read)
        self.disconnectEvent()
        return self

    def send(self, string: str) -> None:
        if self.is_alive():
            return self.__sock.send(string)

    def receiveEvent(self, string) -> None:
        pass

    def disconnectEvent(self) -> None:
        self.group.remove_client(self)

    def connectEvent(self) -> None:
        pass

    def close(self) -> None:
        self.__sock.close()
        self.disconnectEvent()

    __del__ = close


class AbstractGroup(object):
    client_type = AbstractSocket
    #  sockets: List[client_type]

    def __init__(self):
        self.sockets = []

    def add_client(self, request) -> client_type:
        sock = self.client_type(request.websocket, self, _start=False)
        self.sockets.append(sock)
        return sock.listen()

    def remove_client(self, sock: client_type):
        if sock in self.sockets:
            if sock.is_alive():
                sock.close()
            self.sockets.remove(sock)
            return True
        return False

    def get_sockets(self) -> List[client_type]:
        return self.sockets

    def get_available_clients(self) -> List[client_type]:
        return list(filter(lambda sock: sock.is_alive(), self.get_sockets()))

    def get_available_clients_length(self) -> int:
        return len(self.get_available_clients())

    def group_send(self, data):
        for sock in self.get_available_clients():
            sock.send(data)

    def close(self):
        for sock in self.get_available_clients():
            sock.close()

    __del__ = close


class JSONSocket(AbstractSocket):
    group: "JSONGroup"

    def send(self, data: Any) -> None:
        super().send(json.dumps(data))

    def read(self) -> Union[Any, None]:
        _read = super().read()
        return json.loads(_read) if _read else None

    def receiveEvent(self, obj) -> None:
        pass


class JSONGroup(AbstractGroup):
    client_type = JSONSocket

    def __init__(self):
        super().__init__()


class WebClient(JSONSocket):
    group: "WebClientGroup"

    def __init__(self, sock: websocket.DefaultWebSocket, user_obj: User, group: "AbstractGroup", _start: bool = False):
        super().__init__(sock, group, _start)
        self.user: User = user_obj
        self.profile: Profile = self.user.profile
        self.id: int = user_obj.id
        self.username = user_obj.username
        self.admin: bool = self.profile.is_admin()
        self.identity: str = identities.get(self.profile.identity)


class WebClientGroup(JSONGroup):
    client_type = WebClient

    def __init__(self):
        super().__init__()

    def add_client(self, request, token: str = "") -> Union[WebClient, bool]:
        try:
            _validate, username = webtoken_validate(token)
            if _validate:
                user = User.objects.get(username=username)
                sock = self.client_type(request.websocket, user, self, _start=False)
                self.sockets.append(sock)
                self.joinEvent(sock)
                return sock.listen()
            return False
        except jwt.exceptions.DecodeError:
            return False

    def remove_client(self, sock: WebClient) -> bool:
        if super(WebClientGroup, self).remove_client(sock):
            self.leaveEvent(sock)
            return True
        return False

    def joinEvent(self, sock: WebClient) -> None:
        pass

    def leaveEvent(self, sock: WebClient) -> None:
        pass
