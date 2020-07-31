import requests

def buscar_ciudad(ciudad_ingresada, pronosticos_ciudades): # Para el punto 5
    """
        Busca una ciudad dentro de pronosticos_ciudades.
        Precondicion: debe ingresarse una ciudad para buscar, y debe ingresarse como segundo parametro
        un objeto JSON que contenga el pronostico a 3 dias de varias ciudades.
        Postcondicion: devuelve un diccionario con los datos de la ciudad ingresada. Si no se encuentra la ciudad devuelve un diccionario vacio.
    """
    # ciudad_no_existe = True
    datos_ciudad = {}
    # while ciudad_no_existe:
    for ciudad in range(len(pronosticos_ciudades)):
        if ciudad_ingresada == pronosticos_ciudades[ciudad]['name'].lower():
            datos_ciudad = pronosticos_ciudades[ciudad]
            return datos_ciudad
        # ciudad_no_existe = False

    return datos_ciudad

def obtener_url(url): # Para el punto 3
    """
        Obtiene informacion de la url ingresada.
        Precondicion: se debe ingresar una url.
        Postcondicion: devuelve un objeto JSON.
    """
    # return requests.get(url).json()

    try:
        informacion = requests.get(url).json()
    except ConnectionError as e:
        print(f"Error: {e} ")
    return informacion


def obtener_alertas_en_localizacion_ingresada(provincia, alertas): # Para el punto 2
    """
        Obtiene las alertas en una localizacion ingresada por el usuario.
        Precondicion: debe ingresarse una lista con los datos del usuario, la clave que se utiliza del JSON es 'state', que esta dentro de la clave 'address'.
        Postcondicion: si se encuentra la ciudad, devuelve una lista con todas sus alertas. Si no se encuentra la ciudad devuelve una lista vacia.
    """
    # localizacion_no_existe = True
    alertas_ciudad = []
    # while localizacion_no_existe:
    for ciudad in range(len(alertas)):
        for zona in range(len(alertas[ciudad]['zones'])):
            if provincia['address']['state'].replace(" Province", "") in alertas[ciudad]['zones'][str(zona)]:
                alertas_ciudad.append(alertas[ciudad]['description'])
                return alertas_ciudad
        # localizacion_no_existe = False
    return alertas_ciudad

def obtener_localizacion_usuario(token, coordenadas):
    """
        Obtiene la ubicacion del usuario.
        Precondicion: debe ingresarse una tokende locationIQ y una lista, donde el primer indice indica la latitud y el segundo la longitud.
        Postcondicion: devuelve las coordenadas del usuario.
    """
    URL = f"https://us1.locationiq.com/v1/reverse.php?key={token}&lat={coordenadas[0]}&lon={coordenadas[1]}&format=json"
    datos_coordenadas = obtener_url(URL)
    
    return datos_coordenadas

def obtener_coordenadas(ciudad_ingresada, pronostico_ciudades_json):
    """
        Obtiene las coordenadas del usuario dependiendo de la ciudad que escriba.
        Precondicion: debe ingresarse un string, la cual tiene que indicar el nombre de la ciudad en la que esta el usuario.
        y un objeto JSON que contenga la informacion del clima de varias ciudades.
        Postcondicion: devuelve las coordenadas en forma de lista, asi: [latitud, longitud]. Si no encuentra la ciudad, devuelve [0,0]
    """
    # ciudad_no_encontrada = True
    coordenadas = [0,0]
    # while ciudad_no_encontrada:
    for ciudad in range(len(pronostico_ciudades_json)):
        if ciudad_ingresada.lower() == pronostico_ciudades_json[ciudad]['name'].lower():
            coordenadas[0] = pronostico_ciudades_json[ciudad]['lat']
            coordenadas[1] = pronostico_ciudades_json[ciudad]['lon']
            return coordenadas
    # ciudad_no_encontrada = False
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

def mostrar_pronostico_en_ciudad_ingresada(pronostico_ciudad_json, alertas): # Para el punto 5
    """
        Muestra al usuario el pronostico extendido a 3 dias en la ciudad que ingresó.
        Precondicion: se debe ingresar una lista con dos espacios, el primer espacio es la latitud y
        la segunda, la longitud.
    """
    print("-" * 40 + "PRONOSTICO EXTENDIDO" + "-" * 40)
    print(f"Pronostico extendido a 3 dias para {pronostico_ciudad_json['name']}, {pronostico_ciudad_json['province']} ")
    print(f"Temperatura por la mañana: {pronostico_ciudad_json['weather']['morning_temp']}ºC", end=", ")
    print(f"temperatura por la tarde: {pronostico_ciudad_json['weather']['afternoon_temp']}ºC\n")
    print(f"Descripcion por la mañana: {pronostico_ciudad_json['weather']['morning_desc']}")
    print(f"Descripcion por la tarde: {pronostico_ciudad_json['weather']['afternoon_desc']}")
    for alerta in range(len(alertas)):
        for zona in range(len(alertas[alerta]['zones'])):
            if pronostico_ciudad_json['province'] in alertas[alerta]['zones'][str(zona)]:
                print("-" * 40 + "ALERTAS" + "-" * 40)
                print(f"Alerta Nº{alerta+1} en {pronostico_ciudad_json['province']}: {alertas[alerta]['description']}\n")

def mostrar_alertas_en_localizacion(alertas, datos_usuario): # Para el punto 2
    """
        Muestra al usuario el estado actual del pronostico en la localizacion que ingresó.
        Precondicion: debe ingresarse dos objetos JSON, el primer parametro debe ser una lista con alertas en una ciudad, y el segundo parametro, un JSON con datos de localizacion del usuario.
    """
    print("-" * 40 + "ALERTAS" + "-"*40)
    for numero_alerta in range(len(alertas)):
        print(f"Alerta Nº{numero_alerta+1} en {datos_usuario['address']['state']}: {alertas[numero_alerta]}\n")

def main():
    TOKEN = "8a245ccf3615f5"

    URL_ALERTAS_NACIONALES = "https://ws.smn.gob.ar/alerts/type/AL" # URL para el punto 3
    URL_PRONOSTICO_EXTENDIDO = "https://ws.smn.gob.ar/map_items/forecast/3" # URL pronostico extendido a 3 dias
    URL_ESTADO_ACTUAL = "https://ws.smn.gob.ar/map_items/weather" # URL pronostico de varias ciudades, estado actual

    pronosticos = obtener_url(URL_ESTADO_ACTUAL)
    alertas_nacionales = obtener_url(URL_ALERTAS_NACIONALES)

    # CREAR UNA VARIABLE QUE ALMACENE EL VALOR DE LA LOCALIZACION ACTUAL DEL USUARIO 
    lat_lon = input("Introduzca su latitud y longitud(separados por coma): ").split(",")
    datos_localizacion_usuario = obtener_localizacion_usuario(TOKEN, lat_lon)

    opcion = "0"
    while opcion != "6":
        opcion = input("1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico extendido\n4. Datos históricos\n5. Tormetas por radar\n6. Salir\nOpcion: ")
        while opcion.isnumeric() is False or int(opcion) <= 0 or int(opcion) > 6:
            opcion = input("Ingrese un número del menú: ")

        if opcion == "1":
            print("a)Alertas en geolocalizacion ingresada\nb)Alertas en geolocalizacion actual")
            opcion = input("Opcion: ")

            if opcion == "a":
                # ACA USARIA OTRA VARIABLE QUE ALMACENE LA LOCALIZACION INGRESADA POR EL USUARIO
                lat_lon = input("Introduzca latitud y longitud, separados por coma: ").split(",")
                datos_localizacion_usuario = obtener_localizacion_usuario(TOKEN, lat_lon)
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(datos_localizacion_usuario, alertas_nacionales)
                mostrar_alertas_en_localizacion(alertas_en_localizacion, datos_localizacion_usuario)

            elif opcion == "b":
                #  ACA USARIA LA VARIABLE DE LA LOCALIZACION ACTUAL
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(datos_localizacion_usuario, alertas_nacionales)
                mostrar_alertas_en_localizacion(alertas_en_localizacion, datos_localizacion_usuario)

        elif opcion == "2":
            mostrar_alertas_nacionales(alertas_nacionales)

        elif opcion == "3":
            ciudad_ingresada = input("Ingrese una ciudad: ").lower()
            pronosticos = obtener_url(URL_PRONOSTICO_EXTENDIDO)
            datos_ciudad = buscar_ciudad(ciudad_ingresada, pronosticos)

            while datos_ciudad == {}:
                ciudad_ingresada = input("No se encuentra la ciudad. Intentelo nuevamente: ").lower()
                datos_ciudad = buscar_ciudad(ciudad_ingresada, pronosticos)
            mostrar_pronostico_en_ciudad_ingresada(datos_ciudad, alertas_nacionales)
            # mostrar_alertas_en_localizacion(alertas_nacionales, datos_ciudad)
            #mostrar alertas en la zona del usuario tmb

        elif opcion == "4":
            menu_csv()
        elif opcion == "5":
            print("Análisis de imagen")


main()
