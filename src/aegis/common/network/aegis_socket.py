import io
import socket

from aegis.common.network.aegis_socket_exception import AegisSocketException


class AegisSocket:
    """Represents a socket connection to AEGIS."""

    def __init__(self) -> None:
        """Initializes a AegisSocket instance."""
        self._socket: socket.socket | None = None
        self._in_stream: io.BufferedReader | None = None
        self._out_stream: io.BufferedWriter | None = None

    def connect(self, host: str, port: int) -> None:
        """
        Connects to AEGIS at the specified host and port.

        Args:
            host: The hostname or IP address of AEGIS.
            port: The port number on which AEGIS is listening.

        Raises:
            AegisSocketException: If the connection to AEGIS fails.
        """
        try:
            self._socket = socket.create_connection((host, port))
            self._in_stream = self._socket.makefile("rb")
            self._out_stream = self._socket.makefile("wb")
        except Exception:
            raise AegisSocketException("Unable to connect to AEGIS.")

    def disconnect(self) -> None:
        """
        Disconnects from the AEGIS server and closes the socket and streams.

        The `disconnect` method ensures that the connection is properly closed, and all
        resources are released. It does nothing if the socket is already closed or not connected.
        """
        try:
            if self._socket and self._in_stream and self._out_stream:
                self._in_stream.close()
                self._out_stream.close()
                self._socket.close()
                self._socket = None
        except Exception:
            pass

    def __del__(self) -> None:
        """Ensures the connection is closed when the object is deleted."""
        self.disconnect()

    def read_message(self, timeout: int | None = None) -> str | None:
        """
        Reads a message from AEGIS with an optional timeout.

        Args:
            timeout: The timeout in seconds for reading the message. If None, the operation will
                     block indefinitely until a message is received.

        Returns:
            The message read from AEGIS. Returns None if a timeout occurs.

        Raises:
            AegisSocketException: If an error occurs while reading the message, such as an incomplete
                                 message or missing null byte.
        """
        if self._socket and self._in_stream and self._out_stream:
            self._socket.settimeout(timeout)
            try:
                size_data = self._in_stream.read(4)
                if len(size_data) < 4:
                    raise AegisSocketException("Couldn't read message length.")

                size = int.from_bytes(size_data, "little")
                size -= 1

                message_data = self._in_stream.read(size)
                if len(message_data) < size:
                    raise AegisSocketException("Message is shorter than expected.")

                null_byte = self._in_stream.read(1)
                if len(null_byte) < 1:
                    raise AegisSocketException("Null byte is missing.")

                return message_data.decode("ascii").strip()

            except socket.timeout:
                return None
            except Exception as e:
                raise AegisSocketException(str(e))
            finally:
                self._socket.settimeout(None)

    def send_message(self, message: str) -> None:
        """
        Sends a message to AEGIS.

        Args:
            message: The message to be sent to AEGIS.

        Raises:
            AegisSocketException: If an error occurs while sending the message.
        """
        try:
            if self._socket and self._out_stream:
                message_encoded = message.encode("ascii")
                size = len(message_encoded) + 1
                size_bytes = size.to_bytes(4, "little")

                _ = self._out_stream.write(size_bytes)
                _ = self._out_stream.write(message_encoded)
                _ = self._out_stream.write(b"\x00")
                _ = self._out_stream.flush()
        except Exception:
            raise AegisSocketException("Unable to send message to AEGIS.")
