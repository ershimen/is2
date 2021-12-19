# Grupo 35
# Servidor de la aplicacion de taxis
import socket, pickle, datetime, json, math, random
from os.path import exists

# Escribe mensaje de log en fichero de log
def write_log(log_file, msg):
    log_file.write("[" + datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S") +
                    "]: " + msg + "\n")
    print(msg)

# Distancia en km entre dos puntos dadas sus coordenadas en grados
def distancia(latd_o, lond_o, latd_d, lond_d):
    lat_o, lon_o, lat_d, lon_d = map(math.radians, [latd_o, lond_o, latd_d, lond_d])
    aux = ( math.sin((lat_d - lat_o) / 2) ** 2 + math.cos(lat_o) * math.cos(lat_d) *
            math.sin((lon_d - lon_o) / 2) ** 2)
    return 6373.0 * (2 * math.atan2(math.sqrt(aux), math.sqrt(1 - aux)))

# Selecciona el taxi mas cercano
def select_taxi(taxi, lat, lon):
    min_distance_taxi = None
    min_distance = 99999999999
    for t in taxi:
        if taxi[t]["status"] == "libre":
            if min_distance_taxi is None:
                min_distance_taxi = t
                min_distance = distancia(lat, lon, taxi[t]["latitude"],
                                            taxi[t]["longitude"])
            else:
                tentative_distance = distancia(lat, lon, taxi[t]["latitude"],
                                                taxi[t]["longitude"])
                if tentative_distance < min_distance:
                    min_distance = tentative_distance
                    min_distance_taxi = t
    return (min_distance_taxi, min_distance)

def main():
    # Logs
    log_dir = "..\\logs\\"
    log_file = None
    id_log = 1
    # Buscar nombre de log disponible
    while True:
        log_name = log_dir + "serverlog-" + datetime.datetime.now().strftime("%Y-%m-%d") + \
                    "_" + str(id_log) + ".log"
        if exists(log_name):
            id_log += 1
        else:
            log_file = open(log_name, "w")
            break

    write_log(log_file, "Starting database...")
    # Datos del servicio
    # Taxis
    taxi_file_path = "..\\data\\taxi.json"
    taxi_file = open(taxi_file_path, "r")
    taxi = json.load(taxi_file)
    # Usuarios
    user_file_path = "..\\data\\user.json"
    user_file = open(user_file_path, "r")
    user = json.load(user_file)
    user_file.close()
    taxi_file.close()

    # Precio
    PRECIO = 0.5 # €/km

    # Servidor
    # Socket
    write_log(log_file, "Starting server...")
    write_log(log_file, "Initializing socket...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 1234))
    s.listen(1)
    write_log(log_file, "Socket initialized.")
    write_log(log_file, "Server started. Listening...")
    msg = None
    end = False
    status_petitions = {} # peticiones de viajes
    while not end:
        # Escuchar nueva peticion
        conn, addr = s.accept()
        msg = pickle.loads(conn.recv(1024))
        write_log(log_file, "New message from " + addr[0] + ":" + str(addr[1]) +
                            ", type=" + msg["type"])
        #print("msg:", msg)
        response = {}
        # Peticion stop de server
        if msg["type"] == "stop":
            end = True
            response["data"] = "OK"
        # Peticion login
        elif msg["type"] == "login":
            # Comprobar usuario y contrasena
            if msg["mail"] in user and user[msg["mail"]]["pwd"] == msg["pwd"]:
                response["data"] = True
                write_log(log_file, "Logged as \"" + msg["mail"] + "\".")
            else:
                response["data"] = False
                write_log(log_file, "Invalid credentials for user \"" + msg["mail"] + "\".")
        # Peticion registro
        elif msg["type"] == "registro":
            # Comprobar si el usuario existe
            if msg["mail"] in user:
                response["data"] = False
                write_log(log_file, "User \"" + msg["mail"] + "\" already exists.")
            else:
                user[msg["mail"]] = {"nombre": msg["nombre"],
                                        "tlf": msg["tlf"],
                                        "pago": msg["pago"],
                                        "pwd": msg["pwd"]}
                write_log(log_file, "Created user \"" + msg["mail"] + "\".")
                response["data"] = True
        # Modificacion de datos de usuario
        elif msg["type"] == "cambio":
            user[msg["mail"]] = {"nombre": msg["nombre"],
                                    "tlf": msg["tlf"],
                                    "pago": msg["pago"],
                                    "pwd": msg["pwd"]}
            write_log(log_file, "Modified user \"" + msg["mail"] + "\".")
            response["data"] = True
        # Peticion listado de taxis
        elif msg["type"] == "list_taxi":
            # devolver listado de taxis
            response["data"] = taxi
        # Peticion solicitud de viaje
        elif msg["type"] == "viaje":
            # calcular (latitud, longitud) a partid del nombre
            random.seed(msg["location"])
            # seleccionar un taxi
            selected_taxi, distance_selected = select_taxi(taxi,
                                                            random.uniform(40.0, 41.0),
                                                            random.uniform(-3.2, -4.4))
            if select_taxi is None:
                response["data"] = None
                write_log(log_file, "No taxis aviable.")
            else:
                precio = distance_selected * PRECIO
                response["data"] = {"id_taxi": selected_taxi, "precio": precio,
                                    "distancia": distance_selected}
                write_log(log_file, "Taxi \"" + selected_taxi + "\" is now reserved (" +
                                        msg["date"] + "-" + msg["hour"] + ").")
                status_petitions[selected_taxi] = {"status": "pending",
                                                    "taxi_id": selected_taxi,
                                                    "origin": msg["location"],
                                                    "destination": msg["destination"],
                                                    "distance": distance_selected,
                                                    "price": precio,
                                                    "date": msg["date"],
                                                    "hour": msg["hour"]}
                taxi[selected_taxi]["status"] = "reservado"
        # Peticion estado de la peticion de viaje
        elif msg["type"] == "status":
            write_log(log_file, "Asking for petition status (" + msg["taxi"] + ")")
            if status_petitions[msg["taxi"]]["status"] == "pending":
                response["data"] = "pending"
            else:
                response["data"] = status_petitions[msg["taxi"]]["status"]
                status_petitions.pop(msg["taxi"])
                write_log(log_file, "Taxi petition completed (" + msg["taxi"] + ") -> " +
                                        response["data"])
        # Peticion cambio de estado de una peticion de viaje
        elif msg["type"] == "status_update":
            if msg["taxi"] in status_petitions:
                status_petitions[msg["taxi"]]["status"] = msg["status"]
                write_log(log_file, "Admin completed a petition (" + msg["taxi"] + "): " +
                                        msg["status"])
                response["data"] = "ok"
                if msg["status"] == "accept":
                    taxi[msg["taxi"]]["status"] = "ocupado"
                else:
                    taxi[msg["taxi"]]["status"] = "libre"
            else: # nunca ocurrira
                response["data"] = "nop"
        # Peticion listado de peticiones
        elif msg["type"] == "get_status":
            response["data"] = {}
            for p in status_petitions:
                info_petition = status_petitions[p]
                if info_petition["status"] == "pending":
                    response["data"][p] = info_petition
        # Enviar respuesta
        conn.send(pickle.dumps(response))
        conn.close()

    # Parar servicio
    write_log(log_file, "Stopping server...")
    write_log(log_file, "Closing socket...")
    s.close()
    write_log(log_file, "Saving database...")
    # Guardar estado de taxis y usuarios
    user_file = open(user_file_path, "w")
    taxi_file = open(taxi_file_path, "w")
    json.dump(user, user_file, indent=4)
    json.dump(taxi, taxi_file, indent=4)
    write_log(log_file, "Closing files...")
    user_file.close()
    taxi_file.close()
    write_log(log_file, "Server stopped.")
    log_file.close()

if __name__ == "__main__":
    main()
