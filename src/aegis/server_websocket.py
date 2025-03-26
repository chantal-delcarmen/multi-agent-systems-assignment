# pyright: reportMissingTypeStubs = false
import queue
import threading
import time
from typing import NamedTuple

from websocket_server import WebsocketServer


class Client(NamedTuple):
    """Represents a connected client."""

    id: int
    handler: object
    address: str


class WebSocketServer:
    """Serve a AEGIS Simulation over a websocket connection."""

    def __init__(self, wait_for_client: bool = False) -> None:
        """Initializes a new server."""
        self._host = "localhost"
        self._port = 6003
        self._wait_for_client = wait_for_client
        self._connected = False
        self._done = False
        self._server = None
        self._previous_events: list[bytes] = []
        self._incoming_events: queue.Queue[bytes] = queue.Queue()
        self._queue_thread = threading.Thread(target=self._process_queue)
        self._lock = threading.Lock()

    def _process_queue(self) -> None:
        """Events to process that are in the event queue."""
        try:
            while not self._done:
                try:
                    event = self._incoming_events.get(timeout=0.3)
                    self._process_event(event)
                except Exception:
                    pass

            while not self._incoming_events.empty():
                event = self._incoming_events.get()
                self._process_event(event)
        except Exception as e:
            print(f"Error processing queue: {e}")

    def _process_event(self, event: bytes) -> None:
        """
        Sends the events to the connected clients.
        Locks until the event is sent to all clients.

        Args:
            event: The event to send.
        """
        if self._server is not None:
            with self._lock:
                for client in self._server.clients:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                    self._server.send_message(client, event)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                self._previous_events.append(event)

    def add_event(self, event: bytes) -> None:
        """
        Add an event to be sent to client in the future.

        Args:
            event: The event to add.
        """
        if self._done:
            raise RuntimeError("Can't add event, server already finished!")
        self._incoming_events.put(event)

    def _on_open(self, client: Client, server: WebsocketServer) -> None:
        """
        Handle actions upon client connection.

        Args:
            client: The client object.
            server: The WebsocketServer currently being used.
        """
        self._connected = True
        for event in self._previous_events:
            server.send_message(client, event)  # pyright: ignore[reportUnknownMemberType]

    def start(self) -> None:
        """Run the server."""
        if not self._wait_for_client:
            return

        self._server = WebsocketServer(self._host, self._port)
        self._server.set_fn_new_client(self._on_open)  # pyright: ignore[reportUnknownMemberType]

        self._queue_thread.start()
        self._server.run_forever(threaded=True)

        print("Waiting for connection from client...")
        while not self._connected:
            time.sleep(0.3)

        print("Connection received!")

    def shutdown_gracefully(self):
        """
        Send a CLOSE handshake to all connected clients before terminating server
        """

        if self._server is None:
            return
        self._server.keep_alive = False
        self._server._disconnect_clients_gracefully(1000, bytes("", encoding="utf-8"))
        # These bottom two are flipped from regular order in websocket_server
        self._server.shutdown()
        self._server.server_close()

    def finish(self) -> None:
        """Send all queued events and shutdown the server."""
        if not self._wait_for_client:
            return
        self._done = True
        print("shutting down server...")
        try:
            self._queue_thread.join()
            self.shutdown_gracefully()
        except Exception as e:
            print(f"Error shutting down server: {e}")

    def set_wait_for_client(self, wait_for_client: bool) -> None:
        """
        Set whether to wait for the client to connect to AEGIS.

        Args:
            wait_for_client: Whether to wait for the client.
        """
        self._wait_for_client = wait_for_client
