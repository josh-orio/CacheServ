# Cache Server

import socket, json, os, time
from tx_rx import *

# no proper error handling
# no ssl support
# dont care

sd = os.path.expanduser('~') + '/socketry/' # serving directory
cached = [] # recently served files will be cached in this list
cms = 8 * (10 ** 9) # cache max size (8gb)

# cache structure
# [
#     {
#         "fn": str e.g. "2024-04-10.txt",
#         "data": bytearray
#     }
# ]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080)) # '' defaults to localhost

while True:
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    
    conn, data = rx(conn)

    cmd = json.loads(data.decode())

    try:
        if cmd['op'] == 'ls':
            # list directory
            rep = os.listdir(sd + cmd['dir'])
            tx(conn, str(rep).encode())

        if cmd['op'] == 'read':
            rtnd = False
            for i in range(len(cached)):
                if cached[i]['fn'] == cmd['fn']:
                    rtnd = True
                    tx(conn, cached[i]['data']) # data is read as binary so doesnt need .encode()
                    break

            if not rtnd:
                with open(sd + cmd['fn'], 'rb') as file: data = file.read()
                
                tx(conn, data)
                
                cached.append({
                    'fn': cmd['fn'],
                    'data': data
                })

                # trim cache if over cms
                cst = -1 # cache size tally (bytes)

                while cst == -1 or cst > cms:
                    cst = sum([os.path.getsize(sd + cached[i]['fn']) for i in range(len(cached))])

                    if cst > cms:
                        cached = cached[1:]

    except Exception as e:
        print(e)

    conn.close()