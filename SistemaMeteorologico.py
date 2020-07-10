import requests
import json

def alertasEnLocalizacion(coordenadas):
    """
        Muestra al usuario las alertas para su localizacion.
        Precondicion: se debe ingresar una lista con dos espacios, el primer espacio es la latitud y
        la segunda, la longitud.
    """
    datos = requests.get("https://ws.smn.gob.ar/map_items/weather")
    datosJSON = datos.json()
    for x in datosJSON:
        if x['lat'] == coordenadas[0] and x['lon'] == coordenadas[1]:
            print(f"\nAlertas para: {x['name']}, {x['province']}.\nClima:")
            print(f"Humedad: {x['weather']['humidity']}\nPresion: {x['weather']['pressure']}")
            print(f"Visibilidad: {x['weather']['visibility']}\nVelocidad del viento: {x['weather']['wind_speed']}")
            print(f"Direccion del viento: {x['weather']['wing_deg']}\nTemperatura: {x['weather']['tempDesc']}")
            print(f"Para hoy: {x['weather']['description']}")

def main():
    latlon = input("Introduzca latitud y longitud actual, separados por coma: ") # latitud, longitud
    coordenadas = latlon.split(",")
    estadoMenu = True

    print(coordenadas)
    print(type(coordenadas))
    while estadoMenu:
        print("--MENU--")
        print("1)Listado de alertas en localizacion ingresada por usuario(latitud, longitud) o localizacion actual")
        print("2)Listar alertas a nivel nacional")
        opcion = input("Opcion: ")

        if opcion == "1":
            print("\na)Alertas en localizacion ingresada\nb)Alertas en localizacion actual")
            opcion = input("Opcion: ")

            if opcion == "a":
                latlon = input("Introduzca latitud y longitud, separados por coma: ")
                coordenadas = latlon.split(",")
                alertasEnLocalizacion(coordenadas)

            elif opcion == "b":
                pass
            estadoMenu = False
        elif opcion == "2":

            estadoMenu = False


main()
