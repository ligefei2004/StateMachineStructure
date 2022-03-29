import socket
import graphviz
from graphviz import Source

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('20.211.33.233', 65432)

sock.connect(server_address)

state = [['' for x in range(3)] for y in range(25)]
count = [0 for x in range(25)]
total = 0

data = sock.recv(16).decode('utf-8')
# 65 is 'A'
previous = ord(data[0]) - 65
# print(data, end='')
changed = False
while total < 75:
    pos = (count[previous] % 3) + 1
    count[previous] = count[previous] + 1
    send = bytearray(str(pos) + "\n", 'utf-8')
    # print(send)
    sock.sendall(send)
    data = sock.recv(16).decode('utf-8')
    # print(data, end='')
    current = ord(data[0]) - 65
    if count[previous] <= 3:
        state[previous][pos - 1] = current
        total = total + 1
        changed = True
    if current == 25:
        data = sock.recv(16).decode('utf-8')
        current = ord(data[0]) - 65

    previous = current
    if previous == 0 and count[previous] >= 3:
        if changed:
            changed = False
        else:
            break
sock.close()
f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
f.attr(rankdir='LR', size='8,5')
f.attr('node', shape='doublecircle')
for i in range(25):
    if count[i] > 0:
        f.node(str(chr(i + 65)))
f.node('Z')
f.attr('node', shape='circle')
for i in range(25):
    # print(chr(65 + i) + " ")
    # print(state[i])
    previous = str(chr(i + 65))
    for j in range(3):
        if state[i][j]:
            f.edge(previous, str(chr(state[i][j] + 65)), label=str(j + 1))

s = Source(f, filename="test.gv", format="pdf")
s.view()
