import pickle, socket

# Test 1: recepcion y envio de un diccionaro vacio
print("Test 1: recepcion y envio de un diccionaro vacio")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1234))
s.listen(1)
print("Esperando mensaje...")
conn, addr = s.accept()
print("\tcliente:", addr)
msg = pickle.loads(conn.recv(1024))
print("\tmensaje:", msg)
for e in msg:
    msg[e] = msg[e] + 1
print("\trespuesta", msg)
conn.send(pickle.dumps(msg))
conn.close()
s.close()

# Test 2: recepcion y envio de un diccionaro no vacio
print("Test 1: recepcion y envio de un diccionaro no vacio")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1234))
s.listen(1)
print("Esperando mensaje...")
conn, addr = s.accept()
print("\tcliente:", addr)
msg = pickle.loads(conn.recv(1024))
print("\tmensaje:", msg)
for e in msg:
    msg[e] = msg[e] + 1
print("\trespuesta", msg)
conn.send(pickle.dumps(msg))
conn.close()
s.close()
