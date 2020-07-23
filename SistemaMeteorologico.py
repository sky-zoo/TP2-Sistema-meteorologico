import csv
import matplotlib.pyplot as plt
import numpy as np
import requests
import cv2

RUTA = 'weatherdata--389-603.csv'
RUTA_IMAGEN = r"C:\Users\desktop\Documents\FIUBA\Algoritmos I\TP_2\imagenes-radar\COMP_CEN_ZH_CMAX_20200630_215000Z.png"


def leer_archivo_historico():
    """
    Precondición: Realiza la lectura del archivo histórico csv.
    Postcondición: Retorna una lista con los datos del archivo histórico.
    """
    lista_historico = []

    with open(RUTA) as csvfile:
        archivo = csv.DictReader(csvfile)

        for dato in archivo:
            reg = {"fecha": dato['Date'], "temp_max": dato['Max Temperature'], "temp_min": dato['Min Temperature'],
                   "precipitacion": dato['Precipitation'], "humedad_relativa": dato['Relative Humidity']}

            lista_historico.append(reg)

    return lista_historico


def obtener_lista_año_temperatura(lista_historico):
    """
    Precondición: Obtiene temperatura promedio (promedio de temp máx y temp min) por cada registro. Recibe la lista del archivo historico.
    Postcondición: Retorna lista con los datos año y temperatura promedio.
    """
    # Obtiene temperatura promedio por cada fecha del archivo. y los guarda en una lista con su año correspondiente.

    lista_año_temperatura = []

    for dato in lista_historico:
        fecha_temperatura = dato['fecha']
        año_temperatura = fecha_temperatura[-4::]

        temperatura = (float(dato['temp_max']) + float(dato['temp_min'])) / 2
        temperatura = round(temperatura, 1)
        reg_año_temperatura = {"año": año_temperatura, "temperatura": temperatura}

        lista_año_temperatura.append(reg_año_temperatura)

    return lista_año_temperatura


def obtener_lista_año_humedad(lista_historico):
    """
    Precondición: Obtiene porcentaje promedio de humedad por cada registro. Recibe la lista del archivo historico.
    Postcondición: Retorna lista con los datos año y porcentaje humedad.
    """
    lista_año_humedad = []

    for dato in lista_historico:
        fecha_humedad = dato['fecha']
        año_humedad = fecha_humedad[-4::]

        humedad_relativa = float(dato['humedad_relativa'])
        humedad_porcentaje = round(humedad_relativa * 100)

        reg_año_humedad = {"año": año_humedad, "humedad": humedad_porcentaje}
        lista_año_humedad.append(reg_año_humedad)

    return lista_año_humedad


def obtener_listas_años_temperaturas(lista_año_temperatura):
    """
    Precondición: Obtiene temperatura promedio (temperatura promedio del año). Recibe lista de datos año, temperatura.
    Postcondición: Retorna dos listas, una con los años y otra con las temperaturas promedios por cada año.
    """

    año_anterior = ''
    acum_temperatura = 0
    cont_temperatura = 0
    lista_años = []
    lista_temperaturas = []

    for i in range(len(lista_año_temperatura)):
        if i == 0:
            año_anterior = lista_año_temperatura[i]['año']

        if lista_año_temperatura[i]['año'] == año_anterior:
            acum_temperatura += lista_año_temperatura[i]['temperatura']
            cont_temperatura += 1
        else:
            promedio_año_temperatura = round(acum_temperatura / cont_temperatura)
            lista_años.append(año_anterior)
            lista_temperaturas.append(promedio_año_temperatura)
            año_anterior = lista_año_temperatura[i]['año']

    promedio_año_temperatura = round(acum_temperatura / cont_temperatura)
    lista_años.append(año_anterior)
    lista_temperaturas.append(promedio_año_temperatura)
    año_anterior = lista_año_temperatura[i]['año']

    return lista_años, lista_temperaturas


def obtener_listas_años_humedades(lista_año_humedad):
    """
    Precondición: Obtiene humedad promedio (promedio del año). Recibe lista de datos año, humedad.
    Postcondición: Retorna dos listas, una con los años y otra con las humedades promedios por cada año.
    """

    año_anterior = ''
    acum_humedad = 0
    cont_humedad = 0
    lista_años = []
    lista_humedades = []

    for i in range(len(lista_año_humedad)):
        if i == 0:
            año_anterior = lista_año_humedad[i]['año']

        if lista_año_humedad[i]['año'] == año_anterior:
            acum_humedad += lista_año_humedad[i]['humedad']
            cont_humedad += 1
        else:
            promedio_año_humedad = round(acum_humedad / cont_humedad)
            lista_años.append(año_anterior)
            lista_humedades.append(promedio_año_humedad)
            año_anterior = lista_año_humedad[i]['año']

    promedio_año_humedad = round(acum_humedad / cont_humedad)
    lista_años.append(año_anterior)
    lista_humedades.append(promedio_año_humedad)
    año_anterior = lista_año_humedad[i]['año']

    return lista_años, lista_humedades


def obtener_datos_grafico_temperaturas(lista_historico):
    """
    Precondición: Obtiene los datos para realizar el grafico de temperaturas promedio por año.
    Postcondición: Retorna la listas para graficar.
    """

    lista_año_temperatura = obtener_lista_año_temperatura(lista_historico)
    lista_años, lista_temperaturas = obtener_listas_años_temperaturas(lista_año_temperatura)

    return lista_años, lista_temperaturas


def obtener_datos_grafico_humedades(lista_historico):
    """
    Precondición: Obtiene los datos para realizar el grafico de humedades promedio por año.
    Postcondición: Retorna la listas para graficar.
    """

    lista_año_humedad = obtener_lista_año_humedad(lista_historico)
    lista_años, lista_humedades = obtener_listas_años_humedades(lista_año_humedad)

    return lista_años, lista_humedades


def imprimir_grafico_temperaturas(datos_graficos_temperaturas):
    """
    Imprime el grafico de temperaturas promedio por año.
    """

    lista_años, lista_temperaturas = datos_graficos_temperaturas

    años = np.array(lista_años)
    temperaturas = np.array(lista_temperaturas)

    plt.bar(años, temperaturas, width=0.6, color='lightblue')

    plt.title("Promedio de las temperaturas de los ultimos 5 años en Argentina")
    plt.legend(["Temperaturas"])

    plt.show()


def imprimir_grafico_humedades(datos_graficos_humedades):
    """
    Imprime el grafico de humedades promedio por año.
    """

    lista_años, lista_humedades = datos_graficos_humedades

    años = np.array(lista_años)
    humedades = np.array(lista_humedades)

    plt.bar(años, humedades, width=0.6, color='lightblue')

    plt.title("Promedio de las humedades de los ultimos 5 años en Argentina")
    plt.legend(["Humedades"])

    plt.show()


def obtener_temperatura_max(lista_historico):
    """
    Precondición: Obtiene temperatura máxima promedio del archivo histórico.
    Postcondición: Retorna la fecha en y el valor de la temperatura máxima.
    """

    max_temperatura = 0
    fecha_max_temperatura = ''

    for dato in lista_historico:
        temperatura = (float(dato['temp_max']) + float(dato['temp_min'])) / 2
        temperatura = round(temperatura, 1)

        if temperatura > max_temperatura:
            max_temperatura = temperatura
            fecha_max_temperatura = dato['fecha']

    return fecha_max_temperatura, max_temperatura


def obtener_mm_max_lluvia(lista_historico):
    """
    Precondición: Obtiene temperatura mm máximos de lluvia del archivo histórico.
    Postcondición: Retorna la fecha en y el valor de los mm máximos de lluvia.
    """

    max_mm_lluvia = 0
    fecha_max_mm_lluvia = ''

    for dato in lista_historico:
        precipitacion = float(dato['precipitacion'])
        precipitacion = round(precipitacion, 1)

        if precipitacion > max_mm_lluvia:
            max_mm_lluvia = precipitacion
            fecha_max_mm_lluvia = dato['fecha']

    return fecha_max_mm_lluvia, max_mm_lluvia


def grafico_temperaturas():
    """
    Lee el archivo histórico, obtiene los datos necesarios para graficar e imprime el gráfico de temperaturas.
    """

    arch_historico = leer_archivo_historico()
    datos_grafico_temperaturas = obtener_datos_grafico_temperaturas(arch_historico)
    imprimir_grafico_temperaturas(datos_grafico_temperaturas)


def grafico_humedades():
    """
    Lee el archivo histórico, obtiene los datos necesarios para graficar e imprime el gráfico de humedades.
    """
    arch_historico = leer_archivo_historico()
    datos_grafico_humedades = obtener_datos_grafico_humedades(arch_historico)
    imprimir_grafico_humedades(datos_grafico_humedades)


def mm_max_lluvia():
    """
    Lee el archivo histórico, obtiene los datos mm máximos de lluvia e imprime por pantalla.
    """

    arch_historico = leer_archivo_historico()
    fecha_max_mm_lluvia, max_mm_lluvia = obtener_mm_max_lluvia(arch_historico)
    print("\n------ Milimetros máximos de lluvia ------")
    print("Medición      | Precipitación")
    print(f"Valor máximo  | {max_mm_lluvia}")
    print(f"Fecha         | {fecha_max_mm_lluvia}")


def temp_max():
    """
    Lee el archivo histórico, obtiene la temperatura máxima e imprime por pantalla.
    """
    arch_historico = leer_archivo_historico()
    temperatura_max, fecha_temp_max = obtener_temperatura_max(arch_historico)
    print("\n------ Temperatura máxima ------")
    print("Medición      | Temperatura")
    print(f"Valor máximo  | {temperatura_max}")
    print(f"Fecha         | {fecha_temp_max}")


def imprimir_menu():
    """
    Imprime el menu principal de la aplicación.
    """
    print("-----------------------------------------")
    print("           T O R M E N T A               ")
    print("-----------------------------------------")
    print(
        "1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico\n4. Datos históricos\n5. Tormetas por radar\n6. Salir")


def imprimir_menu_csv():
    """
    Imprime el menu para el archivo histórico.
    """
    print("\n---------- Datos históricos ----------")
    print(
        "Datos de los últimos 5 años de:\n1. Promedio temperaturas\n2. Promedio humedad\n3. Milímetros máximos de lluvia\n4. Temperatura máxima\n5. Salir")


def menu_csv():
    opcion_csv = "0"
    while opcion_csv != "5":
        imprimir_menu_csv()
        opcion_csv = input("\nIngrese la opción que desea: ")
        while opcion_csv.isnumeric() is False or int(opcion_csv) <= 0 or int(opcion_csv) > 5:
            opcion_csv = input("Por favor, ingrese un número válido: ")

        if opcion_csv == "1":
            grafico_temperaturas()

        elif opcion_csv == "2":
            grafico_humedades()

        elif opcion_csv == "3":
            mm_max_lluvia()

        elif opcion_csv == "4":
            temp_max()


def buscar_ciudad(ciudad_ingresada, pronosticos_ciudades):  # Para el punto 5
    """
        Busca una ciudad dentro de pronosticos_ciudades.
        Precondicion: debe ingresarse una ciudad para buscar, y debe ingresarse como segundo parametro
        un objeto JSON que contenga el pronostico a 3 dias de varias ciudades.
        Postcondicion: devuelve un diccionario con los datos de la ciudad ingresada. Si no se encuentra la ciudad devuelve un diccionario vacio.
    """
    ciudad_no_existe = True
    datos_ciudad = {}
    while ciudad_no_existe:
        for ciudad in range(len(pronosticos_ciudades)):
            if ciudad_ingresada == pronosticos_ciudades[ciudad]['name'].lower():
                datos_ciudad = pronosticos_ciudades[ciudad]
        ciudad_no_existe = False

    return datos_ciudad


def obtener_url(url):  # Para el punto 3
    """
        Obtiene informacion de la url ingresada.
        Precondicion: se debe ingresar una url.
        Postcondicion: devuelve un objeto JSON.
    """
    informacion = requests.get(url).json()
    return informacion


def obtener_alertas_en_localizacion_ingresada(coordenadas, pronostico_ciudades_json):  # Para el punto 2
    """
        Obtiene las alertas en una localizacion ingresada por el usuario.
        Precondicion: debe ingresarse una lista con las coordenadas, siendo el primer indice la latitud y el segundo indice la longitud.
        Postcondicion: si se encuentra la ciudad, devuelve la ciudad con todas sus alertas. Si no se encuentra la ciudad devuelve -1.
    """
    localizacion_no_existe = True

    while localizacion_no_existe:
        for ciudad in range(len(pronostico_ciudades_json)):
            if coordenadas[0] == pronostico_ciudades_json[ciudad]['lat'] and coordenadas[1] == \
                    pronostico_ciudades_json[ciudad]['lon']:
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
    coordenadas = [0, 0]
    while ciudad_no_encontrada:
        for ciudad in range(len(pronostico_ciudades_json)):
            if ciudad_ingresada.lower() == pronostico_ciudades_json[ciudad]['name'].lower():
                coordenadas[0] = pronostico_ciudades_json[ciudad]['lat']
                coordenadas[1] = pronostico_ciudades_json[ciudad]['lon']
        ciudad_no_encontrada = False
    return coordenadas


def mostrar_alertas_nacionales(alertas_nacionales_json):  # Este es para el punto 3
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
        print(
            f"Titulo: {alertas_nacionales_json[numero_alerta]['title']}\nEstado: {alertas_nacionales_json[numero_alerta]['status']}\n")
        print(
            f"Fecha: {alertas_nacionales_json[numero_alerta]['date']}\nA la hora: {alertas_nacionales_json[numero_alerta]['hour']}\n")
        print(f"Descripcion: {alertas_nacionales_json[numero_alerta]['description']}\n")
        print(f"Actualizacion: {alertas_nacionales_json[numero_alerta]['update']}\n")
        input("Presione enter para continuar.")


def mostrar_pronostico_en_ciudad_ingresada(pronostico_ciudad_json):  # Para el punto 5
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


def mostrar_alertas_en_localizacion(pronostico_ciudad_json):  # Para el punto 2
    """
        Muestra al usuario el estado actual del pronostico en la localizacion que ingresó.
        Precondicion: debe ingresarse un objeto JSON con el pronostico actual de la ciudad que se haya ingresado.
    """
    print("-" * 80)
    print(f"Estado actual para {pronostico_ciudad_json['name']}({pronostico_ciudad_json['province']})\n")
    print(
        f"Temperatura: {pronostico_ciudad_json['weather']['temp']}ºC | Humedad: {pronostico_ciudad_json['weather']['humidity']}%",
        end=" | ")
    print(
        f"Presion: {pronostico_ciudad_json['weather']['pressure']} hPa | Visibilidad: {pronostico_ciudad_json['weather']['visibility']} km",
        end=" | ")
    print(
        f"Velocidad del viento: {pronostico_ciudad_json['weather']['wind_speed']} km/h | Direccion del viento: {pronostico_ciudad_json['weather']['wing_deg']} ")
    print(f"Descripcion: {pronostico_ciudad_json['weather']['description']}\n")
    input("Presione enter para continuar.")


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
    recorte = imagen[y: y + diametro, x: x + diametro]

    return recorte


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

    porcentaje = round((cantidad_pixeles * 100) / total_pixeles, 2)

    return porcentaje


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


def main():
    # definir variables

    URL_ALERTAS_NACIONALES = "https://ws.smn.gob.ar/alerts/type/AL"  # URL para el punto 3
    URL_INFORMES_ESPECIALES = "https://ws.smn.gob.ar/alerts/type/IE"  # URL para punto 2 o 5
    URL_PRONOSTICO_EXTENDIDO = "https://ws.smn.gob.ar/map_items/forecast/3"  # URL pronostico extendido a 3 dias
    URL_AVISOS_A_CORTO_PLAZO = "https://ws.smn.gob.ar/alerts/type/AC"  # URL para punto 2 o 5
    URL_ESTADO_ACTUAL = "https://ws.smn.gob.ar/map_items/weather"  # URL pronostico de varias ciudades, estado actual

    diametro_radar = 160

    # cordenadas en pixeles del centro de cada ciudad, "nombre": (x,y)
    coor_ciudad = {"neuquen": (236, 439), "bahia blanca": (426, 430), "santa rosa": (369, 338),
                   "mar del plata": (578, 402), "caba": (555, 264), "pergamino": (482, 232),
                   "santa fe": (484, 139), "cordoba": (360, 129)}

    # rango de colores separados por tipo de alertas en formato hsv [matiz, saturacion, brillo]
    rango_colores = {"celeste-verde": (np.array([33, 100, 20]), np.array([102, 255, 255])),
                     "amarillo-naranja": (np.array([16, 50, 25]), np.array([32, 255, 255])),
                     "rojo1": (np.array([0, 100, 100]), np.array([15, 255, 255])),
                     "rojo2": (np.array([161, 75, 20]), np.array([179, 255, 255])),
                     "magenta": (np.array([130, 50, 20]), np.array([160, 255, 255]))}

    pronosticos_actual = obtener_url(URL_ESTADO_ACTUAL)

    ciudad_usuario = input("Introduzca la ciudad donde se encuentra: ")
    coordenadas = obtener_coordenadas(ciudad_usuario, pronosticos_actual)
    if coordenadas == [0, 0]:
        ciudad_usuario = input("Por favor ingrese una ciudad valida: ")
        coordenadas = obtener_coordenadas(ciudad_usuario, pronosticos_actual)

    opcion_menu = "0"

    while opcion_menu != "6":
        imprimir_menu()
        opcion_menu = input("\nIngrese la opción que desea: ")
        while opcion_menu.isnumeric() is False or int(opcion_menu) <= 0 or int(opcion_menu) > 6:
            opcion_menu = input("Por favor, ingrese un número válido: ")

        if opcion_menu == "1":
            print("---------- Alertas por geolocalización ----------")
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

        elif opcion_menu == "2":
            print("---------- Alertas a nivel nacional ----------")
            alertas = obtener_url(URL_ALERTAS_NACIONALES)
            mostrar_alertas_nacionales(alertas)

        elif opcion_menu == "3":
            print("---------- Pronóstico extendido ----------")
            ciudad_ingresada = input("Ingrese una ciudad: ").lower()
            pronosticos = obtener_url(URL_PRONOSTICO_EXTENDIDO)
            datos_ciudad = buscar_ciudad(ciudad_ingresada, pronosticos)

            while datos_ciudad == {}:
                ciudad_ingresada = input("No se encuentra la ciudad. Intentelo nuevamente: ").lower()
                datos_ciudad = buscar_ciudad(ciudad_ingresada, pronosticos)
                mostrar_pronostico_en_ciudad_ingresada(datos_ciudad)

        elif opcion_menu == "4":
            menu_csv()

        elif opcion_menu == "5":
            print("\n---------- Análisis de imagen ----------")
            seguir = "s"
            while seguir != "n":
                ciudad = menu_ciudades()
                try:
                    radar = cv2.imread(RUTA_IMAGEN)
                    recorte = recortar_imagen(radar, coor_ciudad[ciudad][0], coor_ciudad[ciudad][1], diametro_radar)
                    identificar_alerta(recorte, rango_colores, diametro_radar)
                    seguir = input("¿Desea ver datos de otra ciudad? (s/n): ").lower()
                except TypeError:
                    print("---Error al leer la imagen, compruebe que la ruta lleve al archivo---\n")
                    seguir = "n"


main()
