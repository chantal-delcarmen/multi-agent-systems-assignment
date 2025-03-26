from __future__ import annotations

import io
import socket
import struct
import threading
from typing import override

from aegis.agent_control.network.agent_socket_exception import AgentSocketException


class AgentSocket:
    """A class to represent the TCP socket connection between the AEGIS server and an Agent client.

    Attributes:
        socket (socket.socket | None): The TCP socket on the AEGIS server connected to an Agent client.
        in_stream (io.BufferedReader | None): The input stream for reading messages from the Agent client.
        out_stream (io.BufferedWriter | None): The output stream for sending messages to the Agent client.
        send_cool_message (str | None): The message to send to the Agent client.
        send_success (bool): Whether the message was successfully sent to the Agent client.
        send_exception (bool): Whether an exception occurred while sending the message to the Agent client.
    """

    def __init__(self) -> None:
        self.socket: socket.socket | None = None
        self.in_stream: io.BufferedReader | None = None
        self.out_stream: io.BufferedWriter | None = None
        self.send_cool_message: str | None = None
        self.send_success: bool = False
        self.send_exception: bool = False

    def connect(self, server_socket: socket.socket) -> None:
        """Connect an agent by accepting connection on the passed server socket

        Args:
            server_socket (socket.socket): The server socket to connect to the Agent client.
        """
        try:
            self.socket = server_socket.accept()[0]
            self.in_stream = self.socket.makefile("rb")
            self.out_stream = self.socket.makefile("wb")
        except Exception as e:
            raise AgentSocketException(f"Unable to connect AEGIS to agent: {str(e)}")

    def disconnect(self):
        """Disconnect from the Agent client"""
        try:
            if (
                self.socket is not None
                and self.in_stream is not None
                and self.out_stream is not None
            ):
                self.in_stream.close()
                self.out_stream.close()
                self.socket.close()
                self.socket = None
        except Exception:
            pass

    def __del__(self):
        """Finalize the AgentSocket (attemtping same functionality as Java finalize method)"""
        self.disconnect()

    def read_message(self, timeout: int) -> str | None:
        """Read a message from the Agent client

        Args:
            timeout (int): The timeout for reading the message from the Agent client.

        Returns:
            str | None: The message read from the Agent client.
        """
        if self.socket is not None:  # only read if connected
            self.socket.settimeout(timeout)
            try:
                return self._read_message()
            finally:
                self.reset_timeout()
        return ""

    def _read_message(self) -> str | None:
        """Read a message from the Agent client

        Returns:
            str | None: The message read from the Agent client.
        """
        try:
            if self.in_stream is None:
                raise AgentSocketException("Input stream is not initialized")
            size_buffer = self.in_stream.read(4)
            if len(size_buffer) != 4:
                raise AgentSocketException("Couldn't read message length.")

            # -1 is for the null byte
            size: int = struct.unpack("I", size_buffer)[0] - 1

            message_buffer = self.in_stream.read(size)
            if len(message_buffer) < size:
                raise AgentSocketException("Message is shorter than expected.")

            _ = self.in_stream.read(1)  # read the null byte

            return message_buffer.decode("ascii").strip()
        except socket.timeout:
            return None
        except Exception as e:
            raise AgentSocketException(str(e))

    def send_message(self, message: str) -> None:
        """Send a message to the Agent client

        Args:
            message (str): The message to send to the Agent client.
        """
        if self.socket is not None:
            self.send_cool_message = message
            self.send_success = False
            self.send_exception = False

            sender = self._Sender(self)
            sender.start()

            sender.join(0.1)

            if sender.is_alive():
                sender.interrupt()

            if self.send_exception:
                self.disconnect()
                raise AgentSocketException(
                    "Unable to send message to agent due to terminal exception, disconnecting from agent."
                )
            if not self.send_success:
                self.disconnect()
                raise AgentSocketException(
                    "Unable to send message to agent due to terminal TCP buffer output stream write block, disconnecting from agent."
                )

    class _Sender(threading.Thread):
        """
        Send a message to the Agent client

        A threaded send for an agent_socket is the same as a send in the aegis_socket class.
        """

        def __init__(self, agent_socket: AgentSocket) -> None:
            threading.Thread.__init__(self)
            self.agent_socket = agent_socket
            self._stop_event = threading.Event()

        @override
        def run(self) -> None:
            try:
                if (
                    self.agent_socket.out_stream is not None
                    and self.agent_socket.send_cool_message is not None
                ):
                    size_buffer = struct.pack(
                        "I", len(self.agent_socket.send_cool_message) + 1
                    )
                    _ = self.agent_socket.out_stream.write(size_buffer)
                    _ = self.agent_socket.out_stream.write(
                        self.agent_socket.send_cool_message.encode("ascii")
                    )
                    _ = self.agent_socket.out_stream.write(b"\x00")
                    self.agent_socket.out_stream.flush()
                    self.agent_socket.send_success = True
            except Exception as e:
                print(f"error in sender thread: {e}")
                self.agent_socket.send_exception = True

        def interrupt(self) -> None:
            self._stop_event.set()

        def is_interrupted(self) -> bool:
            return self._stop_event.is_set()

    def reset_timeout(self):
        if self.socket is not None:
            self.socket.settimeout(None)
