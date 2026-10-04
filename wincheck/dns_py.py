import socket
print(socket.gethostbyname("example.com"))
try:
    socket.gethostbyname("abc.nowhere-not-exist.com")
except socket.gaierror as e:
    print("gaierror:", e)
