# importar librerias


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
            print("Análisis de imagen")


main()
