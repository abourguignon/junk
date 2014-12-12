#!/usr/bin/env python
import zmq


# Config
topic = ''
address = 'tcp://127.0.0.1:12345'
file_name = 'access.log'
bufsize = 0  # unbuffered so we write directly to the file

# Connect to the binding
context = zmq.Context()
sock = context.socket(zmq.SUB)

sock.setsockopt(zmq.SUBSCRIBE, topic)
sock.connect(address)

title = 'ZMQ logger (listening on %s)' % address
print title, '\n', len(title) * '-', '\n'

# Write to file
with open(file_name, 'a', bufsize) as f:
    while True:
        message = sock.recv_multipart()
        s = ' '.join(message)
        f.writelines([s, '-----'])
        print s

f.close()
