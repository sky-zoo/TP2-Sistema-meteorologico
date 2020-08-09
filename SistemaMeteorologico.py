import csv
import matplotlib.pyplot as plt
import numpy as np
import requests
import cv2

ARCHIVO_CSV = "weatherdata--389-603.csv"
IMAGEN_RADAR = "imagen_radar.png"

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
    except Exception as e:
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

def obtener_anio_limite():
    """
    Precondición: No recibe ningún parámetro.
    Postcondición: Retorna el año limite (es decir el año actual menos los ultimos 5 años),
    """
    anio_max = 0

    with open(ARCHIVO_CSV) as csvfile:
        archivo = csv.DictReader(csvfile)

        for anio in archivo:
            anio_actual = int(anio['Date'][-4::])
            if anio_actual > anio_max:
                anio_max = anio_actual

        anio_max = anio_max - 5

    return anio_max


def leer_archivo_historico():
    """
    Lectura de archivo csv.
    Precondición: No recibe ningun parametro.
    Postcondición: Retorna una lista de diccionarios con los datos del archivo histórico y una variable booleana error.
    """
    lista_historico = []
    error_bool = False

    try:
        anio_maximo = obtener_anio_limite()
        with open(ARCHIVO_CSV) as csvfile:
            
            archivo = csv.DictReader(csvfile)
            for dato in archivo:
                if anio_maximo <= int(dato['Date'][-4::]):
                    lista_historico.append(dato)

    except Exception as error:
        error_bool = True
        print("Ocurrió un error, no se puede procesar el menu historico CSV.")
        print("Descripción del error: ", error)
        

    return lista_historico, error_bool


def obtener_lista_anio_temperatura(lista_historico):
    """
    Precondición: Debe recibir una lista de diccionarios del archivo historico de temperaturas.
    Postcondición: Obtiene lista de diccionarios con el formato [{año, temperatura},...] (donde temperatura se obtiene de promediar
    temperatura maxima y minima por cada fecha).
    """

    lista_anio_temperatura = []
    for dato in lista_historico:
        anio_temperatura = dato['Date'][-4::]

        temperatura = (float(dato['Max Temperature']) + float(dato['Min Temperature'])) / 2
        temperatura = round(temperatura, 1)
        reg_anio_temperatura = {"anio": anio_temperatura, "temperatura": temperatura}

        lista_anio_temperatura.append(reg_anio_temperatura)

    return lista_anio_temperatura

def obtener_lista_anio_humedad(lista_historico):
    """
    Precondición: Debe recibir una lista de diccionarios del archivo historico de temperaturas.
    Postcondición: Obtiene lista de diccionarios con el formato [{año, humedad},...] (donde humedad se expresa en procentaje).
    """
    lista_anio_humedad = []

    for dato in lista_historico:
        fecha_humedad = dato['Date']
        anio_humedad = fecha_humedad[-4::]
        humedad_relativa = float(dato['Relative Humidity'])
        humedad_porcentaje = round(humedad_relativa * 100)

        reg_anio_humedad = {"anio": anio_humedad, "humedad": humedad_porcentaje}
        lista_anio_humedad.append(reg_anio_humedad)

    return lista_anio_humedad


def obtener_listas_anios_temperaturas(lista_anio_temperatura):
    """
    Precondición: Debe recibir una lista de diccionarios con el formato [{año, temperatura},...].
    Postcondición: Retorna dos listas, una con los años y otra con las temperaturas promedio anuales.
    """

    acum_temperatura = 0
    cont_temperatura = 0
    lista_anios = []
    lista_temperaturas = []

    for i in range(len(lista_anio_temperatura)):
        if i == 0:
            anio_anterior = lista_anio_temperatura[i]['anio']

        if lista_anio_temperatura[i]['anio'] == anio_anterior:
            acum_temperatura += lista_anio_temperatura[i]['temperatura']
            cont_temperatura += 1
        else:
            promedio_anio_temperatura = round(acum_temperatura / cont_temperatura)
            lista_anios.append(anio_anterior)
            lista_temperaturas.append(promedio_anio_temperatura)
            anio_anterior = lista_anio_temperatura[i]['anio']

    promedio_anio_temperatura = round(acum_temperatura / cont_temperatura)
    lista_anios.append(anio_anterior)
    lista_temperaturas.append(promedio_anio_temperatura)

    return lista_anios, lista_temperaturas


def obtener_listas_anios_humedades(lista_anio_humedad):
    
    """
    Precondición: Debe recibir una lista de diccionarios con el formato [{año, humedades},...].
    Postcondición: Retorna dos listas, una con los años y otra con las humedades promedio anuales.
    """
    acum_humedad = 0
    cont_humedad = 0
    lista_anios = []
    lista_humedades = []

    for i in range(len(lista_anio_humedad)):
        if i == 0:
            anio_anterior = lista_anio_humedad[i]['anio']

        if lista_anio_humedad[i]['anio'] == anio_anterior:
            acum_humedad += lista_anio_humedad[i]['humedad']
            cont_humedad += 1
        else:
            promedio_anio_humedad = round(acum_humedad / cont_humedad)
            lista_anios.append(anio_anterior)
            lista_humedades.append(promedio_anio_humedad)
            anio_anterior = lista_anio_humedad[i]['anio']

    promedio_anio_humedad = round(acum_humedad / cont_humedad)
    lista_anios.append(anio_anterior)
    lista_humedades.append(promedio_anio_humedad)

    return lista_anios, lista_humedades


def obtener_datos_grafico_temperaturas(lista_historico):
    """
    Precondición: Debe recibir una lista de diccionarios del archivo historico de temperaturas.
    Postcondición: Retorna dos listas (lista_anios, lista_temperaturas) para crear el gráfico de temperaturas promedio por año.
    """

    lista_anio_temperatura = obtener_lista_anio_temperatura(lista_historico)
    lista_anios, lista_temperaturas = obtener_listas_anios_temperaturas(lista_anio_temperatura)

    return lista_anios, lista_temperaturas


def obtener_datos_grafico_humedades(lista_historico):
    """
    Precondición: Debe recibir una lista de diccionarios del archivo historico de temperaturas.
    Postcondición: Retorna dos listas (lista_anios, lista_humedades) para crear el gráfico de humedades promedio por año.
    """

    lista_anio_humedad = obtener_lista_anio_humedad(lista_historico)
    lista_anios, lista_humedades = obtener_listas_anios_humedades(lista_anio_humedad)

    return lista_anios, lista_humedades


def imprimir_grafico_temperaturas(datos_graficos_temperaturas):
    """
    Imprime el grafico de temperaturas promedio por año.
    """
    lista_anios, lista_temperaturas = datos_graficos_temperaturas

    anios = np.array(lista_anios)
    temperaturas = np.array(lista_temperaturas)

    plt.bar(anios, temperaturas, width=0.6, color='lightblue')

    plt.title("Promedio de las temperaturas de los ultimos 5 años en Argentina")
    plt.legend(["Temperaturas"])

    plt.show()


def imprimir_grafico_humedades(datos_graficos_humedades):
    """
    Imprime el grafico de humedades promedio por año.
    """

    lista_anios, lista_humedades = datos_graficos_humedades

    anios = np.array(lista_anios)
    humedades = np.array(lista_humedades)

    plt.bar(anios, humedades, width=0.6, color='lightblue')

    plt.title("Promedio de las humedades de los ultimos 5 años en Argentina")
    plt.legend(["Humedades %"])

    plt.show()


def obtener_temperatura_max(lista_historico):
    """
    Precondición: Debe recibir una lista de diccionarios del archivo historico de temperaturas.
    Postcondición: Obtiene temperatura máxima promedio del archivo histórico. Retorna el valor y la fecha en que se obtuvo
    la temperatura máxima.
    """

    max_temperatura = 0

    for dato in lista_historico:
        temperatura = (float(dato['Max Temperature']) + float(dato['Min Temperature'])) / 2
        temperatura = round(temperatura, 1)

        if temperatura > max_temperatura:
            max_temperatura = temperatura
            fecha_max_temperatura = dato['Date']

    return fecha_max_temperatura, max_temperatura


def obtener_mm_max_lluvia(lista_historico):
    """
    Precondición: Debe recibir una lista de diccionarios del archivo historico de temperaturas.
    Postcondición: Obtiene milimetros máximos de lluvia del archivo histórico. Retorna el valor y la fecha en que se obtuvo
    los milimetros máximos de lluvia.
    """

    max_mm_lluvia = 0

    for dato in lista_historico:
        precipitacion = float(dato['Precipitation'])
        precipitacion = round(precipitacion, 1)

        if precipitacion > max_mm_lluvia:
            max_mm_lluvia = precipitacion
            fecha_max_mm_lluvia = dato['Date']

    return fecha_max_mm_lluvia, max_mm_lluvia


def grafico_temperaturas(arch_historico):
    """
    Lee archivo histórico, obtiene los datos necesarios para graficar e imprime el gráfico de temperaturas.
    """
    datos_grafico_temperaturas = obtener_datos_grafico_temperaturas(arch_historico)
    imprimir_grafico_temperaturas(datos_grafico_temperaturas)


def grafico_humedades(arch_historico):
    """
    Obtiene los datos para el grafico de humedades y lo imprime por pantalla.
    """
    datos_grafico_humedades = obtener_datos_grafico_humedades(arch_historico)
    imprimir_grafico_humedades(datos_grafico_humedades)


def mm_max_lluvia(arch_historico):
    """
    Obtiene los mm máximos de lluvia imprime por pantalla los datos.
    """

    fecha_max_mm_lluvia, max_mm_lluvia = obtener_mm_max_lluvia(arch_historico)
    print("\n------ Milimetros máximos de lluvia ------")
    print("Medición      | Precipitación")
    print(f"Valor máximo  | {max_mm_lluvia}")
    print(f"Fecha         | {fecha_max_mm_lluvia}")


def temp_max(arch_historico):
    """
    Obtiene la temperatura máxima e imprime por pantalla los datos.
    """
    fecha_temp_max, temperatura_max = obtener_temperatura_max(arch_historico)
    print("\n------ Temperatura máxima ------")
    print("Medición      | Temperatura")
    print(f"Valor máximo  | {temperatura_max}")
    print(f"Fecha         | {fecha_temp_max}")

          
def menu_ciudades():
    """ Muestra menú con nombres de las ciudades con radar enumeradas y pide al usuario que eliga una
        Devuelve: cadena con el nombre de la ciudad elegida en minúsculas """
    opcion = input("Ciudades con radar:\n1.Neuquén\n2.Bahía Blanca\n3.Santa Rosa\n4.Mar del Plata\n5.CABA\n6.Pergamino\n7.Santa Fe\n8.Cordoba\n")
    while opcion.isnumeric() is False or int(opcion) < 1 or int(opcion) > 8:
        opcion = input("Ingrese un número del menú: ")

    lista_ciudades = ["neuquen", "bahia blanca", "santa rosa", "mar del plata", "caba", "pergamino", "santa fe", "cordoba"]

    return lista_ciudades[int(opcion) - 1]  
          

def recortar_imagen(imagen, x, y, diametro):
    """ Parámetros: imagen a recortar (matriz), coordenadas (x,y) del centro del recorte resultante y largo de los lados
        Devuelve: imagen recortada: una matriz de diámetro x diámetro """
    x -= (diametro // 2)
    y -= (diametro // 2)

    return imagen[y: y + diametro, x: x + diametro]
          
          
def crear_mascara(imagen, rango1, rango2=()):
    """ Crea un filtro de la imagen con los colores ingresados en los rangos
        Parámetros: imagen a procesar (matriz) en formato BGR, tupla de dos elementos con el rango
            mínimo y máximo respectivamente de color
        Devuelve: imagen en formato hsv en forma de matriz con elementos de
            valor 0 donde no se encontro el color ingresado"""
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    mascara = cv2.inRange(imagen_hsv, rango1[0], rango1[1])

    if len(rango2) != 0:
        mascara2 = cv2.inRange(imagen_hsv, rango2[0], rango2[1])
        mascara = cv2.add(mascara, mascara2)

    return mascara
          
          
def porcentaje_color(imagen, cantidad_pixeles):
    """ Calcula porcentaje de pixeles con respecto al rango de colores identificados como tormenta
        Parametros: imagen a color en formato BGR y un entero con la cantidad de pixeles de un rango de color
        Devuelve: float con el porcentaje calculado """
    # Rango de todos los colores de las alertas
    rango_color1 = (np.array([0, 100, 100]), np.array([102, 255, 255]))
    rango_color2 = (np.array([130, 75, 20]), np.array([179, 255, 255]))

    mascara_tormentas = crear_mascara(imagen, rango_color1, rango_color2)
    total_pixeles = cv2.countNonZero(mascara_tormentas)

    return round((cantidad_pixeles * 100) / total_pixeles, 2)
          
          
def buscar_color(imagen, colores):
    """ Busca rangos de colores en una imagen y devuelve datos del color más fuerte
        Parametros: imagen que se desea analizar en formato BGR y diccionario con los rangos de colores
        Devuelve: lista con dos valores: una cadena con el nombre del color encontrado o 'ninguno' si no se encontraron
            colores y un float con el porcentaje de pixeles de ese color con respecto al total de la tormenta """
    rangos = ["magenta", "rojo1", "rojo2", "amarillo-naranja", "celeste-verde"]  # orden en el que busca los colores
    contador = 0

    mascara = crear_mascara(imagen, colores[rangos[contador]])
    cantidad_pixeles = cv2.countNonZero(mascara)
    while cantidad_pixeles == 0 and contador < 5:
        if contador == 0:
            mascara = crear_mascara(imagen, colores[rangos[contador + 1]], colores[rangos[contador + 2]])
            cantidad_pixeles = cv2.countNonZero(mascara)
            contador += 1
        elif contador != 4:
            mascara = crear_mascara(imagen, colores[rangos[contador + 1]])
            cantidad_pixeles = cv2.countNonZero(mascara)

        contador += 1

    if contador != 5:
        if contador == 2:
            color = "rojo-bordo"
        else:
            color = rangos[contador]

        porcentaje = porcentaje_color(imagen, cantidad_pixeles)

    else:
        color = "ninguno"
        porcentaje = 0.0

    return [color, porcentaje]


def identificar_alerta(imagen, colores, diametro):
    """ Separa la imagen en 4 y muestra la alerta más alta de cada cuadrante """
    cuad_1 = recortar_imagen(imagen, diametro // 4, diametro // 4, diametro // 2)
    cuad_2 = recortar_imagen(imagen, (diametro * 3) // 4, diametro // 4, diametro // 2)
    cuad_3 = recortar_imagen(imagen, diametro // 4, (diametro * 3) // 4, diametro // 2)
    cuad_4 = recortar_imagen(imagen, (diametro * 3) // 4, (diametro * 3) // 4, diametro // 2)

    cuadrantes = {"Noroeste": cuad_1, "Noreste": cuad_2, "Suroeste": cuad_3, "Sureste": cuad_4}

    for clave, valor in cuadrantes.items():
        datos = buscar_color(valor, colores)

        if datos[0] != "ninguno" and datos[0] != "celeste-verde":
            print(f"Al {clave} de la ciudad se encontró un {datos[1]}% de {datos[0]} en el area de tormenta.")
            if datos[0] == "magenta":
                mensaje = "Tormentas fuertes con posibilidad de granizo"
            elif datos[0] == "rojo-bordo":
                mensaje = "Tormentas con mucha lluvia"
            else:
                mensaje = "Tormentas débiles"

        elif datos[0] == "celeste-verde":
            print(f"Al {clave} de la ciudad solo se encontraron tonos celeste y verdes.")
            mensaje = "Sin alerta próxima"
        else:
            print(f"Al {clave} de la ciudad no se encontraron colores.")
            mensaje = "Sin alerta próxima"

        print("----", mensaje, "----\n")


def analisis_imagen(coor_ciudad, rango_colores, diametro_radar):
    """ Ejecución del analisis de imagen: muestra menu de ciudades, lee la imagen la analiza e imprime la alerta
        Parametros: Diccionario con las coordenadas en pixeles de las ciudades con radares, diccionario con los
            rangos de colores de alertas en formato HSV y entero con el diámetro del radar de cada ciudad. """
    print("\n---------- Análisis de imagen ----------")
    seguir = "s"
    while seguir != "n":
        ciudad = menu_ciudades()
        try:
            radar = cv2.imread(IMAGEN_RADAR)
            recorte = recortar_imagen(radar, coor_ciudad[ciudad][0], coor_ciudad[ciudad][1], diametro_radar)
            identificar_alerta(recorte, rango_colores, diametro_radar)
            seguir = input("¿Desea ver datos de otra ciudad? (s/n): ").lower()
        except TypeError:
            print("---Error al leer la imagen, compruebe que la imagen se encuentra en la misma carpeta.---\n")
            seguir = "n"


def imprimir_menu_csv():
    """
    Imprime el menu para el archivo histórico.
    """
    print("\n---------- Datos históricos ----------")
    print(
        "Datos de los últimos 5 años de:\n1. Promedio temperaturas\n2. Promedio humedad\n3. Milímetros máximos de lluvia\n4. Temperatura máxima\n5. Salir")


def menu_csv():
    opcion_csv = "0"
    arch_historico, error = leer_archivo_historico()
    if not error:
        while opcion_csv != "5":
            imprimir_menu_csv()
            opcion_csv = input("\nIngrese la opción que desea: ")
            while opcion_csv.isnumeric() is False or int(opcion_csv) <= 0 or int(opcion_csv) > 5:
                opcion_csv = input("Por favor, ingrese un número válido: ")

            if opcion_csv == "1":
                grafico_temperaturas(arch_historico)

            elif opcion_csv == "2":
                grafico_humedades(arch_historico)

            elif opcion_csv == "3":
                mm_max_lluvia(arch_historico)

            elif opcion_csv == "4":
                temp_max(arch_historico)
    


def imprimir_menu():
    """
    Imprime el menu principal de la aplicación.
    """
    print("-----------------------------------------")
    print("           T O R M E N T A               ")
    print("-----------------------------------------")
    print(
        "1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico\n4. Datos históricos\n5. Tormentas por radar\n6. Salir")


def main():
    TOKEN = "8a245ccf3615f5"

    URL_ALERTAS_NACIONALES = "https://ws.smn.gob.ar/alerts/type/AL"
    URL_PRONOSTICO_EXTENDIDO = "https://ws.smn.gob.ar/map_items/forecast/3"  # URL pronostico extendido a 3 dias
    
    alertas_nacionales = obtener_url(URL_ALERTAS_NACIONALES)
    pronostico_extendido = obtener_url(URL_PRONOSTICO_EXTENDIDO)

    if alertas_nacionales != {} or pronostico_extendido != {}:
        datos_localizacion_usuario = verificar_y_obtener_pais(TOKEN)
    if alertas_nacionales == {}:
            print("-"*30 + "ERROR" + "-"*30)
            print("Error al obtener las alertas nacionales. Las opciones 1, 2, y 3 no estan disponibles\n")

    diametro_radar = 160

    # cordenadas en pixeles del centro de cada ciudad, "nombre": (x,y)
    coor_ciudad = {"neuquen": (236, 439), "bahia blanca": (426, 430), "santa rosa": (369, 338),
                   "mar del plata": (578, 402), "caba": (555, 264), "pergamino": (482, 232),
                   "santa fe": (484, 139), "cordoba": (360, 129)}

    # rango de colores separados por tipo de alertas en formato HSV [matiz, saturacion, brillo]
    rango_colores = {"celeste-verde": (np.array([33, 100, 20]), np.array([102, 255, 255])),
                     "amarillo-naranja": (np.array([16, 50, 25]), np.array([32, 255, 255])),
                     "rojo1": (np.array([0, 100, 100]), np.array([15, 255, 255])),
                     "rojo2": (np.array([161, 75, 20]), np.array([179, 255, 255])),
                     "magenta": (np.array([130, 50, 20]), np.array([160, 255, 255]))}

    opcion_menu = "0"

    while opcion_menu != "6":
        imprimir_menu()
        opcion_menu = input("\nIngrese la opción que desea: ")
        while opcion_menu.isnumeric() is False or int(opcion_menu) <= 0 or int(opcion_menu) > 6:
            opcion_menu = input("Por favor, ingrese un número válido: ")

        if opcion_menu == "1" and alertas_nacionales != {}:
            print("a)Alertas en geolocalizacion ingresada\nb)Alertas en geolocalizacion actual")
            opcion_menu = input("Opcion: ").lower()

            if opcion_menu == "a":
                localizacion_ingresada = verificar_y_obtener_pais(TOKEN)
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(localizacion_ingresada, alertas_nacionales)
                mostrar_alertas_en_localizacion(alertas_en_localizacion, localizacion_ingresada)

            elif opcion_menu == "b":
                alertas_en_localizacion = obtener_alertas_en_localizacion_ingresada(datos_localizacion_usuario, alertas_nacionales)
                mostrar_alertas_en_localizacion(alertas_en_localizacion, datos_localizacion_usuario)

        elif opcion_menu == "2" and alertas_nacionales != {}:
            print("---------- Alertas a nivel nacional ----------")
            mostrar_alertas_nacionales(alertas_nacionales)

        elif opcion_menu == "3" and alertas_nacionales != {}:
            ciudad_ingresada = input("Ingrese una ciudad: ").lower()
            datos_ciudad = buscar_ciudad(ciudad_ingresada, pronostico_extendido)

            while datos_ciudad == {}:
                ciudad_ingresada = input("No se encuentra la ciudad. Intentelo nuevamente: ").lower()
                datos_ciudad = buscar_ciudad(ciudad_ingresada, pronostico_extendido)
            mostrar_pronostico_en_ciudad_ingresada(datos_ciudad, alertas_nacionales)

        elif opcion_menu == "4":
            menu_csv()

        elif opcion_menu == "5":
            analisis_imagen(coor_ciudad, rango_colores, diametro_radar)

          
main()
