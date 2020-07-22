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
    ruta_imagen = r"C:\Users\desktop\Documents\FIUBA\Algoritmos I\TP_2\imagenes-radar\COMP_CEN_ZH_CMAX_20200630_215000Z.png"
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
                try:
                    radar = cv2.imread(ruta_imagen)
                    recorte = recortar_imagen(radar, coor_ciudad[ciudad][0], coor_ciudad[ciudad][1], diametro_radar)
                    identificar_alerta(recorte, rango_colores, diametro_radar)
                    seguir = input("¿Desea ver datos de otra ciudad? (s/n): ").lower()
                except TypeError:
                    print("---Error al leer la imagen, compruebe que la ruta lleve al archivo---\n")
                    seguir = "n"


main()
