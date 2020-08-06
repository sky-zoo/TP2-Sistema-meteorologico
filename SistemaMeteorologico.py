import requests

def buscar_ciudad(ciudad_ingresada, pronosticos_ciudades): # Para el punto 5
    """
        Busca una ciudad dentro de pronosticos_ciudades.
        Precondicion: debe ingresarse una ciudad para buscar, y debe ingresarse como segundo parametro
        un objeto JSON que contenga el pronostico a 3 dias de varias ciudades.
        Postcondicion: devuelve un diccionario con los datos de la ciudad ingresada. Si no se encuentra la ciudad devuelve un diccionario vacio.
    """
    datos_ciudad = {}
    for ciudad in range(len(pronosticos_ciudades)):
        if ciudad_ingresada == pronosticos_ciudades[ciudad]['name'].lower():
            datos_ciudad = pronosticos_ciudades[ciudad]
            return datos_ciudad

    return datos_ciudad

def obtener_url(url): # Para el punto 3
    """
        Obtiene informacion de la url ingresada.
        Precondicion: se debe ingresar una url.
        Postcondicion: devuelve un objeto JSON si se pudo obtener la informacion de la url. De lo contrario devuelve un diccionario vacio.
    """

    try:
        informacion = requests.get(url)
    except ConnectionError as e:
        print(f"Error de conexion: {e} ")
        informacion = dict()
        return informacion
    if "Cannot GET" in informacion.text or "ERROR" in informacion.text:
        informacion = dict()
        return informacion
    return informacion.json()


def obtener_alertas_en_localizacion_ingresada(provincia, alertas): # Para el punto 2
    """
        Obtiene las alertas en una localizacion ingresada por el usuario.
        Precondicion: debe ingresarse una lista con los datos del usuario, la clave que se utiliza del JSON es 'state', que esta dentro de la clave 'address' y un JSON con alertas nacionales.
        Postcondicion: si se encuentra la ciudad, devuelve una lista con todas sus alertas. Si no se encuentra la ciudad devuelve una lista vacia.
    """
    alertas_ciudad = []
    for ciudad in range(len(alertas)):
        for zona in range(len(alertas[ciudad]['zones'])):
            if provincia['address']['state'].replace(" Province", "") in alertas[ciudad]['zones'][str(zona)]:
                alertas_ciudad.append(alertas[ciudad]['description'])
                return alertas_ciudad
    return alertas_ciudad

def obtener_localizacion_usuario(token, coordenadas):
    """
        Obtiene la ubicacion del usuario.
        Precondicion: debe ingresarse una token de locationIQ y una lista, donde el primer indice indica la latitud y el segundo la longitud.
        Postcondicion: devuelve un diccionario con los datos de la ubicacion del usuario.
    """
    URL = f"https://us1.locationiq.com/v1/reverse.php?key={token}&lat={coordenadas[0]}&lon={coordenadas[1]}&format=json"
    datos_coordenadas = obtener_url(URL)
    
    return datos_coordenadas

def mostrar_alertas_nacionales(alertas_nacionales_json): # Este es para el punto 3
    """
        Muestra en consola todas las alertas nacionales.
        Precondicion: debe ingresarse un diccionario con las alertas nacionales.
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

def mostrar_pronostico_en_ciudad_ingresada(pronostico_ciudad_json, alertas): # Para el punto 5
    """
        Muestra al usuario el pronostico extendido a 3 dias en la ciudad que ingresó y si hay alertas, las muestra.
        Precondicion: se debe ingresar una lista con dos espacios, el primer espacio es la latitud y
        la segunda, la longitud. Tambien debe ingresarse un JSON con alertas nacionales.
    """
    provincia_ingresada = pronostico_ciudad_json['province'].split(",")[0]

    print("-" * 40 + "PRONOSTICO EXTENDIDO" + "-" * 40)
    print(f"Pronostico extendido a 3 dias para {pronostico_ciudad_json['name']}, {pronostico_ciudad_json['province']} ")
    print(f"Temperatura por la mañana: {pronostico_ciudad_json['weather']['morning_temp']}ºC", end=", ")
    print(f"temperatura por la tarde: {pronostico_ciudad_json['weather']['afternoon_temp']}ºC\n")
    print(f"Descripcion por la mañana: {pronostico_ciudad_json['weather']['morning_desc']}")
    print(f"Descripcion por la tarde: {pronostico_ciudad_json['weather']['afternoon_desc']}\n")

    for alerta in range(len(alertas)):
        for zona in range(len(alertas[alerta]['zones'])):
            if provincia_ingresada in alertas[alerta]['zones'][str(zona)]:
                print("-" * 40 + "ALERTAS" + "-" * 40)
                print(f"Alerta Nº{alerta+1}, ubicado en {provincia_ingresada}: {alertas[alerta]['description']}\n")
                     
def mostrar_alertas_en_localizacion(alertas, datos_usuario): # Para el punto 2
    """
        Muestra al usuario las alertas en la localizacion que ingresó.
        Precondicion: debe ingresarse dos objetos JSON, el primer parametro debe ser una lista con alertas en una ciudad, y el segundo parametro, un JSON con datos de localizacion del usuario.
    """
    print("-" * 40 + "ALERTAS" + "-"*40)
    if len(alertas) > 0:
        for numero_alerta in range(len(alertas)):
            print(f"Alerta Nº{numero_alerta+1} en {datos_usuario['address']['state']}: {alertas[numero_alerta]}\n")
    else:
        print(f"No hay alertas en {datos_usuario['address']['state']}\n")

def verificar_y_obtener_pais(TOKEN):
    """
        Pide al usuario latitud y longitud y verifica que las coordenadas ingresadas por el usuario sea Argentina y que sean validas.
        Precondicion: debe ingresarse un TOKEN para utilizar la API de locationIQ y una lista con 2 indices, el primer indice debe ser la latitud, el segundo la longitud.
        Postcondicion: devuelve un diccionario con los datos de la ubicacion ingresada.
    """

    lat_lon = input("Introduzca su latitud y longitud(separados por coma): ").split(",")
    while len(lat_lon) != 2 or lat_lon[0].isalpha() or lat_lon[1].isalpha():
        lat_lon = input("Introduzca una latitud y longitud valida(separados por coma): ").split(",")

    datos_usuario = obtener_localizacion_usuario(TOKEN,lat_lon)
    while 'error' in datos_usuario or datos_usuario['address']['country_code'] != "ar" or len(lat_lon) != 2 or lat_lon[0].isalpha() or lat_lon[1].isalpha() or (float(lat_lon[0]) <= -90 or float(lat_lon[0]) >= 90) or (float(lat_lon[1]) <= -180 or float(lat_lon[1]) >= 80):
        lat_lon = input("Introduzca una latitud y longitud valida y dentro de Argentina(separados por coma, latitud entre -90 y 90, longitud entre -180 y 80): ").split(",")
        if len(lat_lon) == 2:
            datos_usuario = obtener_localizacion_usuario(TOKEN, lat_lon)

    return datos_usuario


def main():
    TOKEN = "8a245ccf3615f5"

    URL_ALERTAS_NACIONALES = "https://ws.smn.gob.ar/alerts/type/AL" # URL para el punto 3
    URL_PRONOSTICO_EXTENDIDO = "https://ws.smn.gob.ar/map_items/forecast/3" # URL pronostico extendido a 3 dias

    alertas_nacionales = obtener_url(URL_ALERTAS_NACIONALES)
    pronostico_extendido = obtener_url(URL_PRONOSTICO_EXTENDIDO)
    if alertas_nacionales != {} or pronostico_extendido != {}:
        datos_localizacion_usuario = verificar_y_obtener_pais(TOKEN)
    if alertas_nacionales == {}:
            print("-"*30 + "ERROR" + "-"*30)
            print("Error al obtener las alertas nacionales. Las opciones 1, 2, y 3 no estan disponibles\n")

    opcion = "0"
    while opcion != "6":
        opcion = input("1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico extendido\n4. Datos históricos\n5. Tormetas por radar\n6. Salir\nOpcion: ")
        while opcion.isnumeric() is False or int(opcion) <= 0 or int(opcion) > 6:
            opcion = input("Ingrese un número del menú: ")
        if opcion == "1" and alertas_nacionales != {}:
            print("a)Alertas en geolocalizacion ingresada\nb)Alertas en geolocalizacion actual")
            opcion = input("Opcion: ").lower()

            if opcion == "a":
                localizacion_ingresada = verificar_y_obtener_pais(TOKEN)
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(localizacion_ingresada, alertas_nacionales)
                mostrar_alertas_en_localizacion(alertas_en_localizacion, localizacion_ingresada)

            elif opcion == "b":
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(datos_localizacion_usuario, alertas_nacionales)
                mostrar_alertas_en_localizacion(alertas_en_localizacion, datos_localizacion_usuario)
        
        elif opcion == "2" and alertas_nacionales != {}:
            mostrar_alertas_nacionales(alertas_nacionales)
        elif opcion == "3" and alertas_nacionales != {}:
            ciudad_ingresada = input("Ingrese una ciudad: ").lower()
            datos_ciudad = buscar_ciudad(ciudad_ingresada, pronostico_extendido)

            while datos_ciudad == {}:
                ciudad_ingresada = input("No se encuentra la ciudad. Intentelo nuevamente: ").lower()
                datos_ciudad = buscar_ciudad(ciudad_ingresada, pronostico_extendido)
            mostrar_pronostico_en_ciudad_ingresada(datos_ciudad, alertas_nacionales)


main()
