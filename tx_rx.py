# Transmitting and Receiving Functions
# These functions are common between both the client and the server

import socket, struct, hashlib

page_size = 1024 # bytes

dbg = False # is we debugging?

def tx(s, data): # (socket instance), (byte array of data to send)
    s.send(struct.pack("q", len(data)))
    if dbg: print('tl:', len(data))

    spos = 0 # sent position (basically a bookmark)

    while spos < len(data):
        page = data[spos : spos + page_size]
        plen = struct.pack("q", len(page)) # tells receiver how long page is supposed to be
        pchk = hashlib.md5(page).hexdigest().encode() # checksum hash for page
        s.sendall(plen + pchk + page)

        if dbg: print('tx hash:', hashlib.md5(page).hexdigest())
        # if dbg: print('tx page:', page)

        conf = struct.unpack("q", s.recv(8))[0]
        if conf == 1: # receiver will send back 1 if it is happy with the page it has received
            spos += page_size

        elif dbg: print('resending') # receiver not satisfied, on next iteration of while, same page will be sent

    if dbg: print()

def rx(s):
    tlen = struct.unpack("q", s.recv(8))[0]
    if dbg: print('tl:', tlen)

    data = bytearray()

    while len(data) < tlen:
        plen = struct.unpack("q", s.recv(8))[0] # page length
        pchk = (s.recv(32)).decode() # page checksum
        page = s.recv(plen) # page data

        if dbg: print('rx hash:', pchk)
        if dbg: print('calc hash:', hashlib.md5(page).hexdigest())

        if len(page) == plen and hashlib.md5(page).hexdigest() == pchk:
            s.send(struct.pack("q", 1)) # tell server transmission was fine
            data.extend(page)

        else:
            if dbg: print(len(page) == plen, len(page), plen)
            if dbg: print(hashlib.md5(page).hexdigest() == pchk)
            s.send(struct.pack("q", 0)) # ask for retransmission

            # want a loop here to clear socket buffer, asking for retransmission always fails

    if dbg: print(len(data) == tlen)
    if dbg: print()

    return s, data