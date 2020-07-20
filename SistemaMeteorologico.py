# importar librerias
import requests

def buscar_ciudad(ciudad_ingresada, pronosticos_ciudades): # Para el punto 5
    """
        Busca una ciudad dentro de pronosticos_ciudades.
        Precondicion: debe ingresarse una ciudad para buscar, y debe ingresarse como segundo parametro
        un objeto JSON que contenga el pronostico a 3 dias de varias ciudades.
        Postcondicion: devuelve un diccionario con los datos de la ciudad ingresada. Si no se encuentra la ciudad devuelve un diccionario vacio.
    """
    datos_ciudad = {}
    ciudad_no_existe = True

    while ciudad_no_existe:
        for ciudad in range(len(pronosticos_ciudades)):
            if ciudad_ingresada == pronosticos_ciudades[ciudad]['name'].lower():
                datos_ciudad = pronosticos_ciudades[ciudad]
        ciudad_no_existe = False

    return datos_ciudad

def obtener_url(url): # Para el punto 3
    """
        Obtiene informacion de la url ingresada.
        Precondicion: se debe ingresar una url.
        Postcondicion: devuelve un objeto JSON.
    """
    informacion = requests.get(url).json()
    return informacion

def obtener_alertas_en_localizacion_ingresada(coordenadas, pronostico_ciudades_json): # Para el punto 2
    """
        Obtiene las alertas en una localizacion ingresada por el usuario.
        Precondicion: debe ingresarse una lista con las coordenadas, siendo el primer indice la latitud y el segundo indice la longitud.
        Postcondicion: si se encuentra la ciudad, devuelve la ciudad con todas sus alertas. Si no se encuentra la ciudad devuelve -1.
    """
    alertas_ciudad = {}
    localizacion_no_existe = True

    while localizacion_no_existe:
        for ciudad in range(len(pronostico_ciudades_json)):
            if coordenadas[0] == pronostico_ciudades_json[ciudad]['lat'] and coordenadas[1] == pronostico_ciudades_json[ciudad]['lon']:
                alertas_ciudad = pronostico_ciudades_json[ciudad]
        localizacion_no_existe = False
    return alertas_ciudad

def obtener_coordenadas(ciudad_ingresada, pronostico_ciudades_json):
    """
        Obtiene las coordenadas del usuario dependiendo de la ciudad que escriba.
        Precondicion: debe ingresarse un string, la cual tiene que indicar el nombre de la ciudad en la que esta el usuario.
        y un objeto JSON que contenga la informacion del clima de varias ciudades.
        Postcondicion: devuelve las coordenadas en forma de lista, asi: [latitud, longitud]
    """
    ciudad_no_encontrada = True
    coordenadas = [0,0]
    while ciudad_no_encontrada:
        for ciudad in range(len(pronostico_ciudades_json)):
            if ciudad_ingresada.lower() == pronostico_ciudades_json[ciudad]['name'].lower():
                coordenadas[0] = pronostico_ciudades_json[ciudad]['lat']
                coordenadas[1] = pronostico_ciudades_json[ciudad]['lon']
        ciudad_no_encontrada = False
    return coordenadas

def mostrar_alertas_nacionales(alertas_nacionales_json): # Este es para el punto 3
    """
        Muestra en consola todas las alertas nacionales.
        Precondicion: debe ingresarse un objeto JSON con las alertas nacionales.
    """
    for numero_alerta in range(len(alertas_nacionales_json)):
        print("-" * 80)
        print(f"Alerta numero {numero_alerta + 1}\n")
        print("Zonas afectadas: ", end="")
        for zonas in alertas_nacionales_json[numero_alerta]['zones'].values():
            print(f"{zonas}", end=". ")
        print("\n")
        print(f"Titulo: {alertas_nacionales_json[numero_alerta]['title']}\nEstado: {alertas_nacionales_json[numero_alerta]['status']}\n")
        print(f"Fecha: {alertas_nacionales_json[numero_alerta]['date']}\nA la hora: {alertas_nacionales_json[numero_alerta]['hour']}\n")
        print(f"Descripcion: {alertas_nacionales_json[numero_alerta]['description']}\n")
        print(f"Actualizacion: {alertas_nacionales_json[numero_alerta]['update']}\n")
        input("Presione enter para continuar.")

def mostrar_pronostico_en_ciudad_ingresada(pronostico_ciudad_json): # Para el punto 5
    """
        Muestra al usuario el pronostico extendido a 3 dias en la ciudad que ingresó.
        Precondicion: se debe ingresar una lista con dos espacios, el primer espacio es la latitud y
        la segunda, la longitud.
    """
    print("-" * 80)
    print(f"Pronostico extendido a 3 dias para {pronostico_ciudad_json['name']}, {pronostico_ciudad_json['province']} ")
    print(f"Temperatura por la mañana: {pronostico_ciudad_json['weather']['morning_temp']}ºC", end=", ")
    print(f"temperatura por la tarde: {pronostico_ciudad_json['weather']['afternoon_temp']}ºC\n")
    print(f"Descripcion por la mañana: {pronostico_ciudad_json['weather']['morning_desc']}")
    print(f"Descripcion por la tarde: {pronostico_ciudad_json['weather']['afternoon_desc']}")
    input("Presione enter para continuar.\n")

def mostrar_alertas_en_localizacion(pronostico_ciudad_json): # Para el punto 2
    """
        Muestra al usuario el estado actual del pronostico en la localizacion que ingresó.
        Precondicion: debe ingresarse un objeto JSON con el pronostico actual de la ciudad que se haya ingresado.
    """
    print("-" * 80)
    print(f"Estado actual para {pronostico_ciudad_json['name']}({pronostico_ciudad_json['province']})\n")
    print(f"Temperatura: {pronostico_ciudad_json['weather']['temp']}ºC | Humedad: {pronostico_ciudad_json['weather']['humidity']}%", end=" | ")
    print(f"Presion: {pronostico_ciudad_json['weather']['pressure']} hPa | Visibilidad: {pronostico_ciudad_json['weather']['visibility']} km", end=" | ")
    print(f"Velocidad del viento: {pronostico_ciudad_json['weather']['wind_speed']} km/h | Direccion del viento: {pronostico_ciudad_json['weather']['wing_deg']} ")
    print(f"Descripcion: {pronostico_ciudad_json['weather']['description']}\n")
    input("Presione enter para continuar.")


def menu_csv():
    opcion = "0"
    while opcion != "5":
        opcion = input("Datos de los últimos 5 años de:\n1. Promedio temperaturas\n2. Promedio humedad\n3. Milímetros máximos de lluvia\n4. Temperatura máxima\n5. Salir\n")
        while opcion.isnumeric() is False or int(opcion) <= 0 or int(opcion) > 5:
            opcion = input("Ingrese un número del menú: ")

        if opcion == "1":
            print("Mostrar gráfico de temperaturas")
        elif opcion == "2":
            print("Mostrar gráfico de humedad")
        elif opcion == "3":
            print("Milímetros de lluvia")
        elif opcion == "4":
            print("Temperatura máxima")


def main():

    URL_ALERTAS_NACIONALES = "https://ws.smn.gob.ar/alerts/type/AL" # URL para el punto 3
    URL_INFORMES_ESPECIALES = "https://ws.smn.gob.ar/alerts/type/IE" # URL para punto 2 o 5
    URL_PRONOSTICO_EXTENDIDO = "https://ws.smn.gob.ar/map_items/forecast/3" # URL pronostico extendido a 3 dias
    URL_AVISOS_A_CORTO_PLAZO = "https://ws.smn.gob.ar/alerts/type/AC" # URL para punto 2 o 5
    URL_ESTADO_ACTUAL = "https://ws.smn.gob.ar/map_items/weather" # URL pronostico de varias ciudades, estado actual

    pronosticos_actual = obtener_url(URL_ESTADO_ACTUAL)

    ciudad_usuario = input("Introduzca la ciudad donde se encuentra: ")
    coordenadas = obtener_coordenadas(ciudad_usuario, pronosticos_actual)
    if coordenadas == [0,0]:
        ciudad_usuario = input("Por favor ingrese una ciudad valida: ")
        coordenadas = obtener_coordenadas(ciudad_usuario, pronosticos_actual)
    opcion = "0"
    while opcion != "6":
        opcion = input("1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico extendido\n4. Datos históricos\n5. Tormetas por radar\n6. Salir\nOpcion: ")
        while opcion.isnumeric() is False or int(opcion) <= 0 or int(opcion) > 6:
            opcion = input("Ingrese un número del menú: ")

        if opcion == "1":
            print("a)Alertas en geolocalizacion ingresada\nb)Alertas en geolocalizacion actual")
            opcion = input("Opcion: ")

            if opcion == "a":
                lat_lon = input("Introduzca latitud y longitud, separados por coma: ")
                coordenadas = lat_lon.split(",")
                pronosticos = obtener_url(URL_ESTADO_ACTUAL)
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(coordenadas, pronosticos)
                mostrar_alertas_en_localizacion(alertas_en_localizacion)
            elif opcion == "b":
                pronosticos = obtener_url(URL_ESTADO_ACTUAL)
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(coordenadas, pronosticos)
                mostrar_alertas_en_localizacion(alertas_en_localizacion)

        elif opcion == "2":
            alertas = obtener_url(URL_ALERTAS_NACIONALES)
            mostrar_alertas_nacionales(alertas)

        elif opcion == "3":
            ciudad_ingresada = input("Ingrese una ciudad: ").lower()
            pronosticos = obtener_url(URL_PRONOSTICO_EXTENDIDO)
            datos_ciudad = buscar_ciudad(ciudad_ingresada, pronosticos)

            while datos_ciudad == {}:
                ciudad_ingresada = input("No se encuentra la ciudad. Intentelo nuevamente: ").lower()
                datos_ciudad = buscar_ciudad(ciudad_ingresada, pronosticos)
            mostrar_pronostico_en_ciudad_ingresada(datos_ciudad)

        elif opcion == "4":
            menu_csv()
        elif opcion == "5":
            print("Análisis de imagen")


main()
