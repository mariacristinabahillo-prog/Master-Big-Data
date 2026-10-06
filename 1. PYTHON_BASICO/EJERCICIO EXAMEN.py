#Para la correcta ejecución de este juego es necesario instalar las librerias openpyxl, pandas, matplotlib, getpass y pyttsx3. 
#Tambien se han usado las librerias ramdon y os, pero estas vienen instaladas por defecto en jupiter.

#El programa crea un archivo excel para guardar las estadisticas llamado "excel_estadisticas.xlsx",
#no se ha guardado en la misma ubicacion pedida en la practica, pero en la funcion mostrar_estadisticas()
#que se usa al elegir la opcion 3 del juego se ha creado una funcion que muestra la ruta del archivo.      

import opciones

while True:
    opciones.menu_principal()
    while True:
        try:
            opcion_elegida = int(input("Elige tu número de opción: "))
            break 
        except ValueError:
            print("¡Error! Debes introducir un número entero.")

    if  opcion_elegida == 4:
        print("") 
        print("Saliendo del juego...")
        quit() 
    elif opcion_elegida == 1:
        opciones.modo_solitario()
    elif opcion_elegida == 2:
        opciones.partida_2jugadores()
    elif opcion_elegida == 3:
        print("ESTADISTICAS DEL JUEGO ADIVINA EL NÚMERO:")
        opciones.mostrar_estadisticas()
        input("Pulsa enter para volver al menu principal")
    else:
        print("Opción no válida, prueba otra vez.")
        input("Pulsa enter para volver al menu principal")