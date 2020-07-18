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
