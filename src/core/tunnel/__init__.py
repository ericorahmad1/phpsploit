"""Phpsploit remote tunnel manager.

Usage:

>>> from core import tunnel
>>> if not tunnel:
>>>     tunnel.open()
>>>     tunnel.send("a php payload")
>>> else:
>>>     tunnel.close()

"""

from core import session
import ui.input

from . import handler
from . import connector


class Tunnel:

    def __init__(self):
        self.socket = None
        self.hostname = None
        self.active = False

    def __bool__(self):
        return self.active

    def open(self):
        assert not self.active
        socket = connector.Request()
        if socket.open():
            # handler for environment reset if needed
            if self.socket:
                old_hostname = self.socket.socket.hostname
                new_hostname = socket.socket.hostname
                if old_hostname != new_hostname:
                    question = ("TARGET hostname has changed, wish "
                                "you reset environment ? (recommended)")
                    if ui.input.Expect(True)(question):
                        session.Env.clear()
                        print("[*] Environment correctly flushed")
                    else:
                        print("[-] Keeping previous environment")

            self.socket = socket
            self.hostname = socket.socket.hostname
            self.active = True
            session.Env.update(socket.environ)
            return True

        return False

    def close(self):
        self.active = False
        return True

    def send(self, raw_payload):
        assert self.active
        assert self.socket
        request = handler.Request()
        request.open(raw_payload)
        response = request.read()
        return response


# instanciate main phpsploit tunnel as core.tunnel
tunnel = Tunnel()