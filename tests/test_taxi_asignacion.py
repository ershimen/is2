import math
# Tests asignacion de taxis

def distancia(latd_o, lond_o, latd_d, lond_d):
    lat_o, lon_o, lat_d, lon_d = map(math.radians, [latd_o, lond_o, latd_d, lond_d])
    aux = ( math.sin((lat_d - lat_o) / 2) ** 2 + math.cos(lat_o) * math.cos(lat_d) * math.sin((lon_d - lon_o) / 2) ** 2)
    return 6373.0 * (2 * math.atan2(math.sqrt(aux), math.sqrt(1 - aux)))

def select_taxi(taxi, lat, lon):
    min_distance_taxi = None
    min_distance = 99999999999
    for t in taxi:
        if taxi[t]["status"] == "libre":
            if min_distance_taxi is None:
                min_distance_taxi = t
                min_distance = distancia(lat, lon, taxi[t]["latitude"], taxi[t]["longitude"])
                print("\t%s: %.5f km" % (t, min_distance))
            else:
                tentative_distance = distancia(lat, lon, taxi[t]["latitude"], taxi[t]["longitude"])
                print("\t%s: %.5f km" % (t, tentative_distance))
                if tentative_distance < min_distance:
                    min_distance = tentative_distance
                    min_distance_taxi = t
    return (min_distance_taxi, min_distance)

def load_taxi(taxi_file_path):
    taxi_file = open(taxi_file_path, "r")
    taxi = json.load(taxi_file)
    taxi_file.close()
    return taxi

def main():
    taxi_ocupados = {
            "taxi_0": {"latitude": 40.21465318958678,
                        "longitude": -3.9111906823940723,
                        "status": "ocupado"},
            "taxi_1": {"latitude": 40.59155044088502,
                        "longitude": -3.5732968759708976,
                        "status": "ocupado"},
            "taxi_2": {"latitude": 40.176025026987375,
                        "longitude": -3.9422678594922975,
                        "status": "ocupado"},
            "taxi_3": {"latitude": 40.89684762959817,
                        "longitude": -3.7718771991709477,
                        "status": "ocupado"}
                    }
    taxi_libres = {
                    "taxi_3": {"latitude": 40.89684762959817,
                                "longitude": -3.7718771991709477,
                                "status": "ocupado"},
                    "taxi_4": {"latitude": 40.358911355033776,
                                "longitude": -4.0215545084555435,
                                "status": "ocupado"},
                    "taxi_5": {"latitude": 40.6284221437227,
                                "longitude": -4.319416315749263,
                                "status": "libre"},
                    "taxi_6": {"latitude": 40.166909675036884,
                                "longitude": -3.858499858064519,
                                "status": "libre"},
                    "taxi_7": {"latitude": 40.68088956633717,
                                "longitude": -4.429496177550655,
                                "status": "libre"},
                    "taxi_8": {"latitude": 40.20624414281453,
                                "longitude": -3.7166624327336515,
                                "status": "libre"},
                    "taxi_9": {"latitude": 40.6954285468896,
                                "longitude": -3.9250534877239067,
                                "status": "ocupado"}
                    }

    # Test 1:
    print("\nTest_1: asignación del taxi más cercano, con taxis libres.")
    print("Debería seleccionarse \"taxi_7\".")
    test1_taxi, test_1_distancia = select_taxi(taxi_libres, 40.272328838216, -4.786012898049119)
    print("Se ha seleccionado el taxi", "\"" + test1_taxi + "\", con distancia", test_1_distancia)

    # Test 2:
    print("\nTest_2: asignacion de taxi cuando no hay taxis libres.")
    print("Debería devolver \"None\".")
    print("Se ha seleccionado \"" + str(select_taxi(taxi_ocupados, 40.15812882938216, -4.386012898049119)[0]) + "\".")


if __name__ == '__main__':
    main()
