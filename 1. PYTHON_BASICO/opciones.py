import random
import openpyxl
import os
import pandas as pd
import matplotlib.pyplot as plt
import getpass
import pyttsx3 

def menu_principal():
    print("=" * 50)
    print(" 🎯 Bienvenidos al juego de ADIVINA EL NÚMERO 🎯")
    print("=" * 50)
    print("El juego tiene las siguientes opciones:")
    print("1.Partida modo solitario")
    print("2.Partida 2 jugadores")
    print("3.Estadistica")
    print("4.Salir")
    print("")
    
def opciones_dificultad():
    print("1.Fácil, 20 intentos.")
    print("2.Medio, 12 intentos.")
    print("3.Difícil, 5 intentos.")
    print("")
   
def numero_generado(minimo, maximo):
    numero_aleatorio= random.randint(minimo, maximo)
    return(numero_aleatorio)

def guardar_estadisticas(tipo_partida, jugador, jugador2, intentos, resultado):
    archivo = "excel_estadisticas.xlsx"
    if not os.path.exists(archivo):
        libro = openpyxl.Workbook()
        hoja = libro.active
        hoja.title = "Partidas"
        hoja.append(["Tipo de partida", "nombre1","nombre2","intentos","resultado"])
    else:
        libro = openpyxl.load_workbook(archivo)
        hoja = libro.active
    hoja.append([tipo_partida, jugador, jugador2, intentos, resultado])
    libro.save(archivo)

def mensaje(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def modo_solitario ():
    opciones_dificultad()
    while True:
        try:
            dificultad = int(input("Elige la dificultad: "))
            if dificultad not in [1, 2, 3]:
                print("❌ Has introducido mal la dificultad, prueba de nuevo.")
                continue
            break  
        except ValueError:
            print("❌ ¡Error! Debes introducir un número entero.")
    intentos = 0
    if dificultad == 1:
        max_intentos = 20
    elif dificultad == 2:
        max_intentos = 12
    elif dificultad == 3:
        max_intentos = 5
    else:
        print("❌ Has introducido mal la dificultad, prueba de nuevo.")
        return 

    numero_aleatorio = random.randint(1, 1000)
    jugador = input("¿Cual es tu nombre?")
    intentos = 0
    while intentos < max_intentos:
        try:
            numero_elegido = int(input(f"Introduce un número del 1 al 1000, {jugador}: "))
        except ValueError:
            print("❌ Error: Debes introducir un número, no texto. Inténtalo de nuevo.")
            continue
        if numero_elegido <1 or numero_elegido >1000:
            print("❌ El numero introducido no esta en el rango 1-1000, introduce un numero correcto.")
            continue
        intentos += 1
        if numero_elegido == numero_aleatorio:
            print(f"🎉 Enhorabuena, has acertado el número y ganado el juego {jugador}")
            mensaje(f"Enhorabuena, has acertado el número y ganado el juego {jugador}")
            guardar_estadisticas("Solitario", jugador, "", intentos, "GANÓ")
            break
        else:
            print("❌ Incorrecto, prueba otro número.")
            if numero_elegido < numero_aleatorio:
                print(f"{jugador}, tu numero es menor que el numero a adivinar.")
                print(f"Llevas {intentos}/{max_intentos} intentos")
            if numero_elegido > numero_aleatorio:
                print(f"{jugador}, tu numero es mayor que el numero a adivinar")
                print(f"Llevas {intentos}/{max_intentos} intentos")
        if intentos == max_intentos:
            print(f"💀 Has perdido, {jugador}. El número correcto era {numero_aleatorio}")
            mensaje (f"Has perdido, {jugador}. El número correcto era {numero_aleatorio}")
            guardar_estadisticas("Solitario", jugador, "", intentos, "PERDIÓ")
            print("") 

def partida_2jugadores (): 
    opciones_dificultad()
    while True:
        try:
            dificultad = int(input("Elige la dificultad: "))
            if dificultad not in [1, 2, 3]:
                print("⚠️ Has introducido mal la dificultad, prueba de nuevo.")
                continue
            break  
        except ValueError:
            print("❌ ¡Error! Debes introducir un número entero.")

    if dificultad == 1:
        max_intentos = 20
    elif dificultad == 2:
        max_intentos = 12
    elif dificultad == 3:
        max_intentos = 5
    else:
        print("❌ Has introducido mal la dificultad, prueba de nuevo.")
        return

    jugador1 = (input("Nombre del jugador1:"))
    jugador2 = (input("Nombre del jugador2:"))
    print(f"Bienvenidos al juego {jugador1} y {jugador2}. {jugador2}, tienes que adivinar el numero que elija {jugador1} en máximo {max_intentos} intentos.") 

    while True:
        try:
            numero_jugador1 = int(getpass.getpass(f"{jugador1}, introduce un número del 1 al 1000: "))
            if numero_jugador1 < 1 or numero_jugador1 > 1000:
                print("⚠️ El numero introducido no esta en el rango 1-1000, introduce un numero correcto.")
                continue
            break
        except ValueError:
            print("❌ Error: Debes introducir un número válido, no texto.")
    intentos = 0
    while intentos < max_intentos:
        try:
            numero_jugador2 = int(getpass.getpass(f"Introduce un número del 1 al 1000, {jugador2}: "))
        except ValueError:
            print("❌ Error: Debes introducir un número, no texto.")
            continue
    
        if numero_jugador2 <1 or numero_jugador2 >1000:
            print("⚠️ El numero introducido no esta en el rango 1-1000, introduce un numero correcto")
            continue

        intentos += 1

        if numero_jugador1 == numero_jugador2:
            print("🎉 ¡Enhorabuena, has acertado el número y ganado el juego!")
            mensaje ("¡Enhorabuena, has acertado el número y ganado el juego!")
            guardar_estadisticas("2 jugadores", jugador1, jugador2, intentos, "GANÓ")
            break
        else:
            print("❌ Incorrecto, prueba otro número.")
            if numero_jugador1 < numero_jugador2:
                print(f"{jugador2}, tu numero es mayor que el numero a acertar.")
            else:
                print(f"{jugador2}, tu numero es menor que el numero a acertar")
            print(f"Llevas {intentos}/{max_intentos} intentos")
        if intentos == max_intentos:
            print(f"💀 Has perdido. El número correcto era {numero_jugador1}")
            mensaje(f"Has perdido. El número correcto era {numero_jugador1}")
            guardar_estadisticas("2 jugadores", jugador1, jugador2, intentos, "PERDIÓ")
            print("") 

def mostrar_estadisticas():
    archivo = "excel_estadisticas.xlsx"
    print(f"\n📂 Archivo excel guardado en: {os.path.abspath(archivo)}\n")
    if not os.path.exists(archivo):
        print("\n⚠️ No hay estadísticas aún. Juega una partida primero.\n")
        return
    estadisticas = pd.read_excel("excel_estadisticas.xlsx")
    print (estadisticas.to_string(index=False))
    conteo_resultados = estadisticas['resultado'].value_counts()
    plt.bar(conteo_resultados.index.astype(str), conteo_resultados.values)
    plt.title("Resultados del juego (GANÓ vs PERDIÓ)")
    plt.xlabel("Resultado")
    plt.ylabel("Numero de partidas")
   
    plt.show()