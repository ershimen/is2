import socket

def main():
    print("Servidor de eco. Se responde al cliente con el mensaje invertido.",
            "Escribir \"stop\" en el cliente para terminar.", sep='\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 1234))
    msg = None
    s.listen(1)
    while msg != "stop":
        print("Esperando mensaje...")
        conn, addr = s.accept()
        print("\tcliente:", addr)
        msg = conn.recv(1024).decode()
        print("\tmensaje:", msg)
        conn.send(msg[::-1].encode())
        conn.close()
    s.close()

if __name__ == "__main__":
    main()
