import json
from time import sleep

from tornado.websocket import WebSocketHandler

import sickrage

clients = set()


class WebSocketUIHandler(WebSocketHandler):
    """WebSocket handler to send and receive data to and from a web client."""

    def check_origin(self, origin):
        """Allow alternate origins."""
        return True

    def open(self, *args, **kwargs):
        """Client connected to the WebSocket."""
        clients.add(self)

    def on_message(self, message):
        """Received a message from the client."""
        sickrage.app.log.debug('WebSocket received message from {}: {}'.format(self.request.remote_ip, message))

    def data_received(self, chunk):
        """Received a streamed data chunk from the client."""
        super(WebSocketUIHandler, self).data_received(chunk)

    def on_close(self):
        """Client disconnected from the WebSocket."""
        clients.remove(self)

    def __repr__(self):
        """Client representation."""
        return '<{} Client: {}>'.format(type(self).__name__, self.request.remote_ip)


class WebSocketMessage(object):
    """Represents a WebSocket message."""

    def __init__(self, message_type, data):
        """
        Construct a new WebSocket message.
        :param message_type: A string representing the type of message (e.g. notification)
        :param data: A JSON-serializable object containing the message data.
        """
        self.type = message_type
        self.data = data

    @property
    def content(self):
        """Get the message content."""
        return {
            'type': self.type,
            'data': self.data
        }

    def json(self):
        """Return the message content as a JSON-serialized string."""
        return json.dumps(self.content)

    def push(self):
        """Push the message to all connected WebSocket clients."""
        while not clients:
            sleep(0.1)

        for client in clients:
            sleep(0.1)
            sickrage.app.io_loop.add_callback(client.write_message, self.json())
