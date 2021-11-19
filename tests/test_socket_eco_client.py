import socket

def main():
    print("Cliente de eco. El servidor responde con el mensaje invertido.",
            "Escribir \"stop\" para parar el servidor, \"end\" para terminar el cliente.",
            sep='\n')
    while True:
        msg = input("-> ")
        if msg == "end":
            break
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 1234))
        s.send(msg.encode())
        print("<-", s.recv(1024).decode())
        s.close()
    exit()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 1234))
    msg = "hola"
    s.send(msg.encode())
    print("->", s.recv(1024).decode())
    msg = "stop"
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 1234))
    s.send(msg.encode())
    print("->", s.recv(1024).decode())
    s.close()

if __name__ == "__main__":
    main()
