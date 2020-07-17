import csv
import matplotlib.pyplot as plt
import numpy as np

def leer_archivo_historico():
    lista_historico = []

    with open('weatherdata--389-603.csv') as csvfile:
        archivo = csv.DictReader(csvfile)

        for dato in archivo:
            reg = {"fecha": dato['Date'], "longitud": dato['Longitude'], "latitud": dato['Latitude'],
                   "elevacion": dato['Elevation'],
                   "temp_max": dato['Max Temperature'], "temp_min": dato['Min Temperature'],
                   "precipitacion": dato['Precipitation'],
                   "viento": dato['Wind'], "humedad_relativa": dato['Relative Humidity'], "solar": dato['Solar']}
            lista_historico.append(reg)

    return lista_historico

def obtener_datos_temperaturas(lista_historico):
    lista_temperaturas = []

    for dato in lista_historico:
        reg = {"fecha": dato['fecha'], "temp_max": dato['temp_max'], "temp_min": dato['temp_min']}
        lista_temperaturas.append(reg)

    return lista_temperaturas

def obtener_datos_años_temperaturas(lista_temperaturas):
    lista_año_temperatura = []

    for reg in lista_temperaturas:
        fecha_temperatura = reg['fecha']
        año_temperatura = fecha_temperatura[-4::]

        temperatura = (float(reg['temp_max']) + float(reg['temp_min'])) / 2
        temperatura = round(temperatura,1)
        reg_año_temperatura = {"año": año_temperatura, "temperatura": temperatura}

        lista_año_temperatura.append(reg_año_temperatura)

    return lista_año_temperatura

def obtener_datos_grafico_temperatura(lista_año_temperatura):
    lista_datos_grafico_temperatura = []
    acum_temperatura = 0
    cont_temperatura = 0
    año_anterior = ''

    for i in range(len(lista_año_temperatura)):
        if i == 0:
            año_anterior = lista_año_temperatura[i]['año']

        if lista_año_temperatura[i]['año'] == año_anterior:
            acum_temperatura = acum_temperatura + lista_año_temperatura[i]['temperatura']
            cont_temperatura += 1
        else:
            promedio_año_temperatura = round(acum_temperatura / cont_temperatura)
            reg_datos_temperatura = {"año": año_anterior, "temperatura": promedio_año_temperatura}
            lista_datos_grafico_temperatura.append(reg_datos_temperatura)
            año_anterior = lista_año_temperatura[i]['año']

    promedio_año_temperatura = round(acum_temperatura / cont_temperatura)
    reg_datos_temperatura = {"año": año_anterior, "temperatura": promedio_año_temperatura}
    lista_datos_grafico_temperatura.append(reg_datos_temperatura)

    return lista_datos_grafico_temperatura

def obtener_datos_grafico_temperaturas(lista_temperaturas):

    lista_año_temperatura = obtener_datos_años_temperaturas(lista_temperaturas)
    lista_datos_grafico_temperaturas = obtener_datos_grafico_temperatura(lista_año_temperatura)

    return lista_datos_grafico_temperaturas

def obtener_datos_humedades(lista_historico):
    lista_humedades = []

    for dato in lista_historico:
        reg = {"fecha": dato['fecha'], "humedad_relativa": dato['humedad_relativa']}
        lista_humedades.append(reg)

    return lista_humedades

def obtener_datos_años_humedades(lista_humedades):
    lista_año_humedad = []

    for reg in lista_humedades:
        fecha_humedad = reg['fecha']
        año_humedad = fecha_humedad[-4::]

        humedad_relativa = float(reg['humedad_relativa'])
        humedad_porcentaje = round(humedad_relativa * 100)

        reg_año_humedad = {"año": año_humedad, "humedad": humedad_porcentaje}
        lista_año_humedad.append(reg_año_humedad)

    return lista_año_humedad

def obtener_datos_grafico_humedad(lista_año_humedad):
    lista_datos_grafico_humedad = []
    acum_humedad = 0
    cont_humedad = 0
    año_anterior = ''

    for i in range(len(lista_año_humedad)):
        if i == 0:
            año_anterior = lista_año_humedad[i]['año']

        if lista_año_humedad[i]['año'] == año_anterior:
            acum_humedad = acum_humedad + lista_año_humedad[i]['humedad']
            cont_humedad += 1
        else:
            porcentaje_año_humedad = round(acum_humedad / cont_humedad)
            reg_datos_humedad = {"año": año_anterior, "porcentaje": porcentaje_año_humedad}
            lista_datos_grafico_humedad.append(reg_datos_humedad)
            año_anterior = lista_año_humedad[i]['año']

    porcentaje_año_humedad = round(acum_humedad / cont_humedad)
    reg_datos_humedad = {"año": año_anterior, "porcentaje": porcentaje_año_humedad}
    lista_datos_grafico_humedad.append(reg_datos_humedad)

    return lista_datos_grafico_humedad


def obtener_datos_grafico_humedades(lista_humedades):
    lista_año_humedad = obtener_datos_años_humedades(lista_humedades)
    lista_datos_grafico_humedad = obtener_datos_grafico_humedad(lista_año_humedad)

    return lista_datos_grafico_humedad

def imprimir_grafico_humedades(lista_datos_grafico_humedad):
    #x = np.array(['2013', '2014'])
    #y = np.array([53, 55])
    lista_años = []
    lista_humedades = []

    for reg in lista_datos_grafico_humedad:
        lista_años.append(reg['año'])
        lista_humedades.append(reg['porcentaje'])

    años = np.array(lista_años)
    humedades = np.array(lista_humedades)

    plt.bar(años, humedades, align="center")

    plt.title("Promedio de las humedades de los ultimos 5 años en Argentina")
    plt.legend(["Humedad %"])

    plt.show()

def imprimir_grafico_temperaturas(lista_datos_grafico_temperatura):
    lista_años = []
    lista_temperaturas = []

    for reg in lista_datos_grafico_temperatura:
        lista_años.append(reg['año'])
        lista_temperaturas.append(reg['temperatura'])

    años = np.array(lista_años)
    temperaturas = np.array(lista_temperaturas)

    plt.bar(años, temperaturas, align="center")

    plt.title("Promedio de las temperaturas de los ultimos 5 años en Argentina")
    plt.legend(["Temperaturas"])

    plt.show()

def main():
    arch_historico = leer_archivo_historico()
    # Punto a)
    ahis_temperaturas = obtener_datos_temperaturas(arch_historico)
    datos_grafico_temperaturas = obtener_datos_grafico_temperaturas(ahis_temperaturas)
    imprimir_grafico_temperaturas(datos_grafico_temperaturas)

    # Punto b)
    ahis_humedades = obtener_datos_humedades(arch_historico)
    datos_grafico_humedades = obtener_datos_grafico_humedades(ahis_humedades)
    imprimir_grafico_humedades(datos_grafico_humedades)

main()


