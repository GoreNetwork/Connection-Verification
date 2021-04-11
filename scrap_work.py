import socket
from pprint import pprint
import ssl


# sslContext = ssl.SSLContext()


# clientSocket = socket.socket()
# secureClientSocket = sslContext.wrap_socket(
#     clientSocket, do_handshake_on_connect=False)


# secureClientSocket.connect(('www.google.com', 11443))
# # pprint(dir(secureClientSocket))
# secureClientSocket.do_handshake()

sslContext = ssl.SSLContext()
clientSocket = socket.socket()
secureClientSocket = sslContext.wrap_socket(
    clientSocket, do_handshake_on_connect=True)
pprint(dir(secureClientSocket))


secureClientSocket.settimeout(2)
secureClientSocket.connect(('www.yahoo.com', 443))
