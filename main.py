from random import choice, randint #Importar librerias
import json
from datetime import datetime

#Actualizar informacion dentro del json
def update_data(winner,loser):
    with open("scores.json","r") as f:
        data = json.loads(f.read())

    if not(data.get(winner)):
        data[winner] = {
            'points': 1,
            'last_game' :  datetime.now().strftime('%Y-%m-%d a las %H:%M')
        }
    else:
        data[winner]['points']+=1
        data[winner]['last_game'] =  datetime.now().strftime('%Y-%m-%d a las %H:%M')    

    if not(data.get(loser)):
        data[loser] = {
            'points':0,
            'last_game': datetime.now().strftime('%Y-%m-%d a las %H:%M')
        }
    else:
        data[loser]['last_game'] = datetime.now().strftime('%Y-%m-%d a las %H:%M')

    with open("scores.json","w") as f:
        f.write(json.dumps(data))

#Obtener informacion del json y mostrarla
def show_data():
    with open("scores.json","r") as f:
        data = json.loads(f.read())

    ordered_list = list(data.keys())

    for i in range(len(ordered_list)):
        for j in range(len(ordered_list)-1):
            if data[ordered_list[j]]['points'] < data[ordered_list[j+1]]['points']:
                ordered_list[j], ordered_list[j+1] = ordered_list[j+1], ordered_list[j]


    cont = 0
    print("\n*** TABLA DE POSICIONES ***\n")
    for i in ordered_list:
        cont += 1
        info = data[i]['points']
        hour = data[i]['last_game'] 
        print(f'{cont}. {i} {info} puntos acumulados. Ultima partida en {hour}')
    print()

#Funcion para comprobar si el tablero esta lleno
def full():
    full = True
    for i in tablero[0]:
        if i == None:
            full = False
            break
    return full
    
#Funcion que toma una matriz con los valores y los grafica en un string
def get_table(t):
    tablaString = " 1234567 \n+-------+\n"
    for i in range(6):
        tablaString += "|"
        for j in range(7):
            if t[i][j]:
                tablaString += t[i][j]
            else:
                tablaString += "."
        tablaString += "|\n"
    tablaString += "+-------+\n"
    return tablaString    

#Funcion que recibe la columna del jugador con turno y comprueba que sea del tipo correcto y si en dado caso se puede poner en dicha posicion
def column_input(t,player):
    while True:
        columna = input(f"{player[0]}, indica un numero de columna o pulsa [S] para tentar la suerte:")
        #Seccion columna al azar
        if columna == "S":
            while True:
                comprobar = verificate(randint(0,6),t,player) #Generamos un numero de columna aleatoria y tratamos de ponerlo e el tablero
                if comprobar == "victoria": 
                    return "victoria" #Comprobamos si esta ficha genera victoria
                elif comprobar:
                    break
            break
        else:
            #Seccion columna especifica
            try:
                columna = int(columna) #Comprobamos si es un numero, sino, capturamos el error y pedimos un caracter valido
                if columna  >= 1 and columna <= 7: # Si es un numero debe estar entre 1 y 7, sino, lo volvemos a pedir
                    comprobar = verificate((columna-1),t,player) #Comprobamos si la ficha puede colocarse y si genera victoria
                    if comprobar == "victoria":
                        return "victoria"
                    elif comprobar:
                        break
                    else:
                        print("Esta columna está llena...") #En este caso cuando la columna esta llena no se ingresa la ficha y el jugador pierde el turno
                        print(f"El jugador {player[0]} pierde el turno")
                        break
                else:
                    print("Debes ingresar un numero entre 1 y 7") #Peticion de un numero en el rango valido
            except ValueError:
                print("Debes ingresar un numero") #Peticion de caracter valido

#Funcion para verificar si una ficha puede ingresarse en determinada posicion y si en dado caso de que si, si produce una victoria
def verificate(columna,tabla,player):
    if tabla[0][columna] != None: #Si la columna esta llena volvemos un valor False
        return False
    else:
        if tabla[5][columna] == None: #Comprobamos si la columna esta vacia
            tabla[5][columna] = player[1] #Asignamos la nueva ficha en la primera posicion de la columna
            victoria = False
            fila = 5
            cont = 0
            
            #Comprobamos si genera victoria en:

            for i in tabla[fila]: #F I L A
                if i == player[1]:
                    cont +=1
                    if cont == 4:
                        victoria = True
                        return "victoria"
                        break
                else:
                    cont = 0
            
            if victoria == False:
                cont=0
                for i in range(6): # C O L U M N A
                    if tabla[i][columna] == player[1]:
                        cont += 1
                        if cont == 4:
                            victoria = True
                            return "victoria"
                            break
                    else:
                        cont = 0

            if victoria == False:
                cont = 0
                if columna-fila < 0: #P R I M E R A   D I A G O N A L
                        vc = [fila-columna, 0]
                else:
                    vc = [0, columna-fila]
                while vc[0] < 6 and vc[1] < 7:
                    if tabla[vc[0]][vc[1]] == player[1]:
                        cont += 1
                        if cont == 4:
                            victoria = True
                            return "victoria"
                            break
                    else:
                        cont = 0
                    vc[0] += 1
                    vc[1] += 1

            if victoria == False:
                cont = 0
                if columna-(5-fila) < 0: #S E G U N D A   D I A G O N A L
                    vc = [(5-fila)-columna,0]
                else:
                    vc = [5,columna-(5-fila)]
                while vc[0] > 0 and vc[1] < 7:
                    if tabla[vc[0]][vc[1]] == player[1]:
                        cont += 1
                        if cont == 4:
                            victoria = True
                            return "victoria"
                            break
                    else:
                        cont = 0
                    vc[0] -= 1
                    vc[1] += 1
        else:
            for i in range(1, 6): # VERIFICAMOS DONDE DEBERIA IR LA FICHA
                if tabla[i][columna] != None:
                    tabla[i-1][columna] = player[1]
                    fila = i-1
                    victoria = False
                    cont = 0
                    
                    #Comprobamos si genera victoria en:

                    for i in tabla[fila]: #F I L A
                        if i == player[1]:
                            cont +=1
                            if cont == 4:
                                victoria = True
                                return "victoria"
                                break
                        else:
                            cont = 0
                    

                    if victoria == False:
                        cont=0
                        for i in range(6): #C O L U M N A
                            if tabla[i][columna] == player[1]:
                                cont += 1
                                if cont == 4:
                                    victoria = True
                                    return "victoria"
                                    break
                            else:
                                cont = 0

                    if victoria == False:
                        cont = 0
                        if columna-fila < 0:#P R I M E R A   D I A G O N A L
                                vc = [fila-columna, 0]
                        else:
                            vc = [0, columna-fila]
                        while vc[0] < 6 and vc[1] < 7:
                            if tabla[vc[0]][vc[1]] == player[1]:
                                cont += 1
                                if cont == 4:
                                    victoria = True
                                    return "victoria"
                                    break
                            else:
                                cont = 0
                            vc[0] += 1
                            vc[1] += 1



                    if victoria == False:
                        cont = 0
                        if columna-(5-fila) < 0: #S E G U N D A   D I A G O N A L
                            vc = [(5-fila)-columna,0]
                        else:
                            vc = [5,columna-(5-fila)]
                        while vc[0] > 0 and vc[1] < 7:
                            if tabla[vc[0]][vc[1]] == player[1]:
                                cont += 1
                                if cont == 4:
                                    victoria = True
                                    return "victoria"
                                    break
                            else:
                                cont = 0
                            vc[0] -= 1
                            vc[1] += 1
                    break
        return True  #SI NO DETERMINAMOS VICTORIA, LA FICHA SE COLOCA EN SU POSICION Y SE CAMBIA DE TURNO          
                

#Empezando el juego
print("* CUATRO SEGUIDAS *")

#Eligiendo el nombre y la ficha de los jugadores
p1 = []
nombre1 = input("Por favor indique el nombre del participante #1: ")
p1.append(nombre1)
while True:
    ficha1= input(f"{p1[0]}, por favor indica con qué ficha deseas jugar [X] o [O]: ")
    if ficha1 =="X" or ficha1 == "O":
        p1.append(ficha1)
        break
    print("Debes ingresar [X] o [O]")
p2 = []
nombre2 = input("Por favor indique el nombre del participante #2: ")
p2.append(nombre2)
if ficha1 == "X":
    print(f"{p2[0]} te toca jugar con la siguiente ficha: O")
    p2.append("O")
else:
    print(f"{p2[0]} te toca jugar con la siguiente ficha: X")
    p2.append("X")


tablero = []
for i in range(6):
    fila = [None]*7
    tablero.append(fila)

#Eligiendo Turno
turno = choice((p1,p2))

print("Lanzando una moneda para determinar quién inicia la partida...")
print(f"La partida la inicia {turno[0]}")

while True:
    #Imprimimos el tablero
    print(get_table(tablero))
    if column_input(tablero,turno)=="victoria": #Llamar a la funcion de recibir columna y comprobar si la nueva ficha da victoria
        print(get_table(tablero)) #Si da victoria imprimos el tablero y preguntamos si desean repetir la partida
        print(f"¡Felicidades, {turno[0]}, has ganado la partida! Se sumara un punto(1) a tu marcador")
        loser = p1[0] if turno[0] == p2[0] else p2[0]
        update_data(turno[0],loser=loser)
        show_data()
        if input("¿Desean volver a tomar la partida Si [S] No [N]?:") == "N":
            break
        else:
            print("Limpiaremos la tabla...")
            print("Seguiremos con el mismo orden de turnos:")
            tablero = []
            for i in range(6):
                fila = [None]*7
                tablero.append(fila)
    #Comprobar si el tablero esta lleno
    if not full():
        if turno == p1: #Si el tablero no esta lleno, cambiamos de turno
            turno = p2
        else:
            turno = p1
    else:
        print(get_table(tablero)) #Si el tablero esta lleno el juego termina en empate y se da la opcion de reinciar
        print("El tablero está lleno, no se pueden hacer más jugadas, tenemos un empate")
        if input("¿Desean volver a tomar la partida Si [S] No [N]?:") == "N":
            break
        else:
            print("Limpiaremos la tabla...")
            print("Seguiremos con el mismo orden de turnos: ")
            tablero = []
            for i in range(6):
                fila = [None]*7
                tablero.append(fila)