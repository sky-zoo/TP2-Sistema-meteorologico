# importar librerias
import numpy as np
import cv2


def menu_ciudades(ciudades):
    """ Muestra menú con nombres de las ciudades con radar enumeradas y pide al usuario que eliga una
        Parámetro: diccionario con nombre de las ciudades a elegir como claves
        Devuelve: cadena con el nombre de la ciudad elegida en minúsculas o '0' si se elige volver """
    opcion = input("Ciudades con radar:\n1.Neuquén\n2.Bahía Blanca\n3.Santa Rosa\n4.Mar del Plata\n5.CABA\n6.Pergamino\n7.Santa Fe\n8.Cordoba\n9.Volver\n")
    while opcion.isnumeric() is False or int(opcion) < 1 or int(opcion) > 9:
        opcion = input("Ingrese un número del menú: ")

    ciudad = "0"
    contador = 0
    if opcion != "9":
        for clave in ciudades.keys():
            contador += 1
            if contador == int(opcion):
                ciudad = clave

    return ciudad


def recortar_imagen(imagen, x, y):
    """ Parámetros: imagen a recortar (matriz), coordenadas (x,y) del centro del recorte resultante
        Devuelve: imagen recortada: una matriz de 160 x 160 """
    diametro = 160
    x -= (diametro//2)
    y -= (diametro//2)
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


def identificar_color(matriz):
    """ Busca cantidad de valores distintos a 0 en una matriz
        Parametro: recive la matriz que se quiere analizar
        Devuelve: True si encuentra más de 3 elementos sino False"""
    bandera = False
    contador = 0
    for fila in range(len(matriz)):
        for elemento in matriz[fila]:
            if elemento != 0:
                contador += 1

    if contador > 3:
        bandera = True
    return bandera


def identificar_alerta(imagen, colores):
    """ Busca rangos de colores en una imagen y devuelve el tipo de alerta encontrada
        Parametros: imagena que se desea analizar (matriz) y diccionario con los rangos de colores
        Devuelve: string con el mensaje del tipo de alerta"""
    rangos = ["celeste-verde", "amarillo-naranja", "rojo1", "rojo2", "magenta"]
    contador = 0

    alerta = identificar_color(crear_mascara(imagen, colores["celeste-verde"]))
    while alerta is True and contador < 5:
        contador += 1
        if contador != 5:
            if contador == 2:
                alerta = identificar_color(crear_mascara(imagen, colores[rangos[contador]], colores[rangos[contador+1]]))
                contador += 1
            else:
                alerta = identificar_color(crear_mascara(imagen, colores[rangos[contador]]))

    if contador == 0:
        mensaje = "Sin alerta próxima"
    elif contador == 1:
        mensaje = "Nubosidad variada"
    elif contador == 3:
        mensaje = "Lluvias débiles"
    elif contador == 4:
        mensaje = "Tormenta moderada con mucha lluvia"
    else:
        mensaje = "Tormenta fuerte con posibilidad de granizo"

    return mensaje


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
            ciudad = menu_ciudades(coor_ciudad)

            while ciudad != "0":
                radar = cv2.imread("imagen_radar.png")
                recorte = recortar_imagen(radar, coor_ciudad[ciudad][0], coor_ciudad[ciudad][1])
                print(identificar_alerta(recorte, rango_colores), "\n")
                ciudad = menu_ciudades(coor_ciudad)


main()
