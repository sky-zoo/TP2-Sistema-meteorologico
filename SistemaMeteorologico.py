# importar librerias
import numpy as np
import cv2


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


def buscar_color(imagen, colores):
    """ Busca rangos de colores en una imagen y devuelve el tipo de alerta encontrada
        Parametros: imagen que se desea analizar (matriz) y diccionario con los rangos de colores
        Devuelve: lista con dos valores: un entero con el color encontrado (0 = magenta, 2 = rojo, 3 = amarillo-naranja,
            4 = celeste-verde, 5 = ninguno) y un float con el porcentaje de color encontrado"""
    rangos = ["magenta", "rojo1", "rojo2", "amarillo-naranja", "celeste-verde"]  # orden en el que busca los colores
    contador = 0

    mascara = crear_mascara(imagen, colores[rangos[contador]])
    porcentaje = porcentaje_color(mascara)
    while porcentaje == 0 and contador < 5:
        if contador == 0:
            mascara = crear_mascara(imagen, colores[rangos[contador + 1]], colores[rangos[contador + 2]])
            porcentaje = porcentaje_color(mascara)
            contador += 1
        elif contador != 4:
            mascara = crear_mascara(imagen, colores[rangos[contador + 1]])
            porcentaje = porcentaje_color(mascara)

        contador += 1

    return [contador, porcentaje]


def mostar_alerta(imagen, colores, diametro):
    """ Separa la imagen en 4 y muestra las probabilidades de ocurrencia de la alerta más alta en cada uno"""
    cuad_1 = recortar_imagen(imagen, diametro // 4, diametro // 4, diametro // 2)
    cuad_2 = recortar_imagen(imagen, (diametro * 3) // 4, diametro // 4, diametro // 2)
    cuad_3 = recortar_imagen(imagen, diametro // 4, (diametro * 3) // 4, diametro // 2)
    cuad_4 = recortar_imagen(imagen, (diametro * 3) // 4, (diametro * 3) // 4, diametro // 2)

    cuadrantes = {"Noroeste": cuad_1, "Noreste": cuad_2, "Suroeste": cuad_3, "Sureste": cuad_4}

    for clave, valor in cuadrantes.items():
        datos = buscar_color(valor, colores)

        print(clave, "de la ciudad: ")
        if datos[0] != 5:
            if datos[0] == 0:
                alerta = "tormentas fuertes con posibilidad de granizo"
            elif datos[0] == 2:
                alerta = "tormentas moderadas con mucha lluvia"
            elif datos[0] == 3:
                alerta = "lluvias débiles"
            else:
                alerta = "nubosidad variada"

            if datos[1] < 3:
                print("_Probabilidades bajas de", alerta, "\n")
            elif datos[1] > 6:
                print("_Probabilidades altas de", alerta, "\n")
            else:
                print("_Probabilidades medias de", alerta, "\n")

        else:
            print(f"_Sin alerta próxima\n")


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
                mostar_alerta(recorte, rango_colores, diametro_radar)
                seguir = input("¿Desea ver datos de otra ciudad? (s/n): ").lower()


main()
