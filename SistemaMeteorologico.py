import csv
import matplotlib.pyplot as plt
import numpy as np


RUTA = 'weatherdata--389-603.csv'

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
    print("1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico\n4. Datos históricos\n5. Tormetas por radar\n6. Salir")


def imprimir_menu_csv():
    """
    Imprime el menu para el archivo histórico.
    """
    print("\n---------- Datos históricos ----------")
    print("Datos de los últimos 5 años de:\n1. Promedio temperaturas\n2. Promedio humedad\n3. Milímetros máximos de lluvia\n4. Temperatura máxima\n5. Salir")


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


def main():
    #definir variables
    opcion_menu = "0"

    while opcion_menu != "6":
        imprimir_menu()
        opcion_menu = input("\nIngrese la opción que desea: ")
        while opcion_menu.isnumeric() is False or int(opcion_menu) <= 0 or int(opcion_menu) > 6:
            opcion_menu = input("Por favor, ingrese un número válido: ")

        if opcion_menu == "1":
            print("---------- Alertas por geolocalización ----------")

        elif opcion_menu == "2":
            print("---------- Alertas a nivel nacional ----------")

        elif opcion_menu == "3":
            print("---------- Pronóstico extendido ----------")

        elif opcion_menu == "4":
            menu_csv()

        elif opcion_menu == "5":
            print("\n---------- Análisis de imagen ----------")


main()


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


def porcentaje_color(matriz):
    """ Busca cantidad de valores distintos a 0 en una matriz y calcula su porcentaje
        Parametro: recive la matriz que se quiere analizar
        Devuelve: float con el porcentaje de elementos encontrados con respecto a la cantidad de la matriz """
    contador = 0
    cant_elementos = 0
    for fila in range(len(matriz)):
        for elemento in matriz[fila]:
            cant_elementos += 1
            if elemento != 0:
                contador += 1

    return (contador * 100) / cant_elementos


def identificar_color(imagen, colores):
    """ Busca rangos de colores en una imagen y devuelve el tipo de alerta encontrada
        Parametros: imagen que se desea analizar (matriz) y diccionario con los rangos de colores
        Devuelve: entero con el color encontrado: 0 = ninguno, 1 = celeste-verde, 3 = amarillo-naranja, 4 = rojo, 5 = magenta """
    rangos = ["celeste-verde", "amarillo-naranja", "rojo1", "rojo2", "magenta"]
    contador = 0

    mascara = crear_mascara(imagen, colores["celeste-verde"])
    porcentaje = porcentaje_color(mascara)
    while porcentaje != 0 and contador < 5:
        if contador == 1:
            mascara = crear_mascara(imagen, colores[rangos[contador + 1]], colores[rangos[contador + 2]])
            contador += 1
        elif contador != 4:
            mascara = crear_mascara(imagen, colores[rangos[contador + 1]])

        porcentaje = porcentaje_color(mascara)
        contador += 1

    return contador


def identificar_alerta(imagen, colores, diametro):
    """ Analiza y muestra por pantalla el tipo de alerta, donde se ocaciona y las probabilidades de que ocurra
        Parámetros: imagen para analizar (matriz), diccionario con rangos de colores formato hsv y diámetro del radar """
    color_encontrado = identificar_color(imagen, colores)

    print("Tipo de alerta para la ciudad elegida:")
    if color_encontrado != 0:
        if color_encontrado == 1:
            print("---Nubosidad variada---")
            mascara = crear_mascara(imagen, colores["celeste-verde"])
        elif color_encontrado == 3:
            print("---Lluvias débiles---")
            mascara = crear_mascara(imagen, colores["amarillo-naranja"])
        elif color_encontrado == 4:
            print("---Tormenta moderada con mucha lluvia---")
            mascara = crear_mascara(imagen, colores["rojo1"], colores["rojo2"])
        else:
            print("---Tormenta fuerte con posibilidad de granizo---")
            mascara = crear_mascara(imagen, colores["magenta"])

        if color_encontrado != 0:
            cuad_1 = recortar_imagen(mascara, diametro // 4, diametro // 4, diametro // 2)
            cuad_2 = recortar_imagen(mascara, (diametro * 3) // 4, diametro // 4, diametro // 2)
            cuad_3 = recortar_imagen(mascara, diametro // 4, (diametro * 3) // 4, diametro // 2)
            cuad_4 = recortar_imagen(mascara, (diametro * 3) // 4, (diametro * 3) // 4, diametro // 2)

            cuadrantes = {"Noroeste": cuad_1, "Noreste": cuad_2, "Suroeste": cuad_3, "Sureste": cuad_4}

            print("Probabilidades:")
            for clave, valor in cuadrantes.items():
                porcentaje = porcentaje_color(valor)
                if porcentaje != 0:
                    if porcentaje < 10:
                        print(f"Bajas al {clave} de la ciudad")
                    elif porcentaje > 70:
                        print(f"Altas al {clave} de la ciudad")
                    else:
                        print(f"Medias al {clave} de la ciudad")

    else:
        print("Sin alerta próxima")


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
    # definir variables
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

    opcion = "0"
    while opcion != "6":
        opcion = input("1. Alertas (geolocalización)\n2. Alertas (nacional)\n3. Pronóstico\n4. Datos históricos\n5. Tormetas por radar\n6. Salir\n")
        while opcion.isnumeric() is False or int(opcion) <= 0 or int(opcion) > 6:
            opcion = input("Ingrese un número del menú: ")

        if opcion == "1":
            print("Alertas por geolocalización")
        elif opcion == "2":
            print("Alertas a nivel nacional")
        elif opcion == "3":
            print("Pronóstico extendido")
        elif opcion == "4":
            menu_csv()
        elif opcion == "5":
            seguir = "s"
            while seguir != "n":
                ciudad = menu_ciudades()
                radar = cv2.imread("imagen_radar.png")
                recorte = recortar_imagen(radar, coor_ciudad[ciudad][0], coor_ciudad[ciudad][1], diametro_radar)
                identificar_alerta(recorte, rango_colores, diametro_radar)
                seguir = input("\n¿Desea ver datos de otra ciudad? (s/n): ").lower()


main()
