import requests
import json

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
