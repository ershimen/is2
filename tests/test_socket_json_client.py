import pickle, socket

# Test 1: envio y recepcion de un diccionaro vacio
print("Test 1: envio y recepcion de un diccionaro vacio")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 1234))
msg = {}
s.send(pickle.dumps(msg))
print("Mensaje enviado:", msg)
print("Mensaje recibido:", pickle.loads(s.recv(1024)))
s.close()

# Test 2: envio y recepcion de diccionaro no vacio
print("Test 2: envio y recepcion de diccionaro no vacio")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 1234))
msg = {"a":1, "b":2, "c": 3}
s.send(pickle.dumps(msg))
print("Mensaje enviado:", msg)
print("Mensaje recibido:", pickle.loads(s.recv(1024)))
s.close()
