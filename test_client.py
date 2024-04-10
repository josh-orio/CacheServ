# Test Client

import socket, json, time, struct
from tx_rx import *

host = ''
port = 8080

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# tx(s, json.dumps({'op': 'ls', 'dir': ''}).encode())
# s, data = rx(s)
# s.close()
# print(data.decode())


# t = time.time()
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# tx(s, json.dumps({'op': 'read', 'fn': 'ct.bin'}).encode())
# s, data = rx(s)
# s.close()
# print(len(data))
# print(time.time() - t)

# this doesn't qualify as extensive testing...
