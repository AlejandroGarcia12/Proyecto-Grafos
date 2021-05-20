from ctypes import create_string_buffer
from operator import pos
from os.path import supports_unicode_filenames
from typing import SupportsComplex
from igraph import *
#creacion del grafo


def grafo_sudoku(numeros):
    g = Graph()
    g.add_vertices(81)
    #los vertices tienen 3 atributos: casilla [a,b] y cuadro de 3x3 al que pertenecen, el numero que se encuentra en la casilla 
    lcuadro=[]
    lcasilla=[]

    for i in range(9):
        for j in range(9):
            lcasilla.append([i,j])

    for l in range(3):
        cont=0
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1    

    for l in range(3):
        cont=3
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1    
    for l in range(3):
        cont=6
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1        
    
    
    g.vs["casilla"]=lcasilla
    g.vs["cuadrante"]=lcuadro
    g.vs["numero"]=numeros


    for i in range(81):
        for j in range(81):
            if i!=j:
                atributos={}
                if g.vs[i]["cuadrante"]==g.vs[j]["cuadrante"]:#estan en el mismo cuadro 3x3
                    if len(g.es.select(_within=[i,j]))==0:
                        atributos["tipo"]=1
                        g.add_edges([(i,j)],attributes=atributos)
                if g.vs[i]["casilla"][1]==g.vs[j]["casilla"][1] or g.vs[i]["casilla"][0]==g.vs[j]["casilla"][0]:#estan en la misma fila o columna
                    if len(g.es.select(_within=[i,j]))==0 or g.vs[i]["cuadrante"]==g.vs[j]["cuadrante"]:
                        atributos["tipo"]=0
                        g.add_edges([(i,j)], attributes=atributos)
                
    return g

#funcion para encontrar los posibles colores de cada silla no coloreada
def posibles(sudoku):
    posiblesd={}
    for i in range(81):
        posible=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]
        if sudoku.vs[i]["color"]=="white":
            for j in range(81):
                if sudoku.vs[j]["color"]!="white" and len(sudoku.es.select(_within=[i,j]))!=0:
                    if sudoku.vs[j]["color"] in posible:
                        posible.remove(sudoku.vs[j]["color"])
                        posiblesd[i]=posible
    return posiblesd

def Error(sudoku):
    posiblesd=posibles(sudoku)
    #print(posiblesd)
    err=False
    for i in posiblesd.keys():
        if len(posiblesd[i])==0:
            print(i,"no tiene colores posibles")
            err=True

    return err

#verifica si el sudoku esta incompleto. Si el sudoku esta incompleto retorna verdadero
def verifica(sudoku):
    for i in range(81):
        if sudoku.vs[i]["color"]!="white":
            incompleto=False
        else:
            incompleto=True
            break
    return incompleto    

#busca los vertices sin colorear que tengan solo un color posible para colorear en esa casilla y los colorea de ese color
def algoritmo_coloracion1(sudoku,cambio,posible):
    cambio=1
    while cambio!=0:
        cambio=0
        for i in posible.keys():
            if len(posible[i])==1:
                cambio+=1
                print("A1",sudoku.vs[i]["casilla"],posible[i][0])
                sudoku.vs[i]["color"]=posible[i][0]
                posible=posibles(sudoku)
                break
    return sudoku,cambio,posible

def Algoritmo_coloracion2(sudoku,cambio,posible):
    #crear lista de colores posibles en el cuadrante del vertice i
    cambio=1
    cambiobool=False
    while cambio!=0:
        cambio=0
        for i in posible.keys():
            lcolores=[]
            for j in posible.keys():
                if sudoku.vs[i]["cuadrante"]==sudoku.vs[j]["cuadrante"] and i!=j:
                    for col in posible[j]:
                        if col not in lcolores:
                            lcolores.append(col)
        #mirar si hay un color posible de i que no esta en ninguna de las listas de lcolores
            color_i=posible[i]
            for colo in color_i:
                if colo not in lcolores:
                    print("A2",sudoku.vs[i]["casilla"],colo)
                    sudoku.vs[i]["color"]=colo
                    cambio+=1
                    cambiobool=True
                    posible=posibles(sudoku)
                    break
            if cambio!=0:
                break
    if cambiobool:
        cambio=1
    return sudoku, cambio,posible

def Algoritmo_coloracion3(sudoku,cambio,posible):
    cambio=0
    for vert in posible.keys():
        colpro=[]
        c=sudoku.vs[vert]["cuadrante"]
        for vert2 in posible.keys():
            if vert!=vert2:
                if sudoku.vs[vert]["cuadrante"]==sudoku.vs[vert2]["cuadrante"]:
                    if sudoku.vs[vert]["casilla"][1]==sudoku.vs[vert2]["casilla"][1]: #misma columna y mismo cuadrante
                        for i in posible[vert]:
                                if i in posible[vert2]:
                                    colpro.append(i)
                        for vert3 in posible.keys():
                            if sudoku.vs[vert]["cuadrante"]==sudoku.vs[vert3]["cuadrante"] and vert3!=vert and vert3!=vert2:
                                if sudoku.vs[vert3]["casilla"][1]!=sudoku.vs[vert]["casilla"][1]:
                                    for i in posible[vert3]:
                                        if i in colpro:
                                            colpro.remove(i)
        #mirar los vertices que esten en misma columna de cuadrante y de casilla
        aux=[]
        for col in colpro:
            for j in posible.keys():
                if sudoku.vs[j]["cuadrante"]!=sudoku.vs[vert]["cuadrante"] and c%3==sudoku.vs[j]["cuadrante"]%3: #estan en la misma columna de cuadrante
                    if col in posible[j] and sudoku.vs[vert]["casilla"][1]==sudoku.vs[j]["casilla"][1]:#misma columna y col esta en sus posibles colores
                        print("A3_1",sudoku.vs[j]["casilla"],posible[j],col)
                        aux=posible[j]
                        aux.remove(col)
                        posible[j]=aux
                        cambio+=1
    #lo mismo pero con las cuadrantes en la misma fila
    for vert in posible.keys():
        colpro=[]
        c=sudoku.vs[vert]["cuadrante"]
        for vert2 in posible.keys():
            if vert!=vert2:
                if sudoku.vs[vert]["cuadrante"]==sudoku.vs[vert2]["cuadrante"]:
                    if sudoku.vs[vert]["casilla"][0]==sudoku.vs[vert2]["casilla"][0]: #misma fial y mismo cuadrante
                        for i in posible[vert]:
                                if i in posible[vert2]:
                                    colpro.append(i)
                        for vert3 in posible.keys():
                            if sudoku.vs[vert]["cuadrante"]==sudoku.vs[vert3]["cuadrante"] and vert3!=vert and vert3!=vert2:
                                if sudoku.vs[vert3]["casilla"][0]!=sudoku.vs[vert]["casilla"][0]:
                                    for i in posible[vert3]:
                                        if i in colpro:
                                            colpro.remove(i)
        aux=[]
        for col in colpro:
            for j in posible.keys():
                if sudoku.vs[j]["cuadrante"]!=sudoku.vs[vert]["cuadrante"] and c//3==sudoku.vs[j]["cuadrante"]//3: #estan en la misma columna de cuadrante
                    if col in posible[j] and sudoku.vs[vert]["casilla"][0]==sudoku.vs[j]["casilla"][0]:#misma fila y col esta en sus posibles colores
                        print("A3_2",sudoku.vs[j]["casilla"],posible[j],col)
                        aux=posible[j]
                        aux.remove(col)
                        posible[j]=aux
                        cambio+=1
    return sudoku,cambio,posible

def Algoritmo_coloracion4(sudoku):
    #encontrar el primer vertice no coloreado
    
    for i in range(81):
        vertb=-1
        #print(i)
        if sudoku.vs[i]["color"]=="white":
            vertb=i
            break
    #print(vertb)
    #ningun vertice esta en blanco y el sudoku esta completo
    if vertb==-1:
        
        return True, sudoku
        
    for guess in range(1,10):
        if verificar_guess(sudoku,color_dict[guess],vertb):
            sudoku.vs[vertb]["color"]=color_dict[guess]
            print("color y vertice:",color_dict[guess],vertb)
            b,sudoku=Algoritmo_coloracion4(sudoku)
            if b:
                return True,sudoku
        sudoku.vs[vertb]["color"]="white"
    return False, sudoku

#verificar si poner el color guess en vertb es posible
def verificar_guess(sudoku,guess,vertb):
    correcto=True
    sudoku.vs[vertb]["color"]=guess
    for i in range(81):
        if len(sudoku.es.select(_within=[i,vertb]))!=0:
            if guess==sudoku.vs[i]["color"]:
                correcto=False
    return correcto      

#verifica si la solucion es valida    
def verifica_sol(sudoku):
    correcto=True
    if verifica(sudoku):
        print("sudoku incompleto")
        return False

    for i in range(81):
        for j in range(81):
            if len(sudoku.es.select(_within=[i,j]))!=0:
                if sudoku.vs[i]["color"]==sudoku.vs[j]["color"]:
                    correcto=False
    return correcto

def solve_sudoku(sudoku):
    incompleto=True
    cambio=1
    posible=posibles(sudoku)
    cont=0
    while incompleto:
        cambio=0
        sudoku,cambio,posible=algoritmo_coloracion1(sudoku,cambio,posible)
        error1=Error(sudoku)
        if error1:
            print("Algoritmo 1:",error1)
            break 
        sudoku,cambio,posible=Algoritmo_coloracion2(sudoku,cambio,posible)
        error2=Error(sudoku)
        if error2:
            print("Algoritmo 2:",error2)
            break 
    #revisamos si esta resuelto el sudoku
        incompleto=verifica(sudoku)
        if cambio==0 and incompleto:
            sudoku,cambio,posible=Algoritmo_coloracion3(sudoku,cambio,posible)
            sudoku,cambio,posible=Algoritmo_coloracion2(sudoku,cambio,posible)
            if cambio==0:
                b,sudoku=Algoritmo_coloracion4(sudoku)
                print(b)
                if b:
                    print("solucionado A4")
                break
            


    lcolores=[]
    for i in range(81):
        lcolores.append(sudoku.vs[i]["color"])
    val=verifica_sol(sudoku)
    print("solucion valida: ",val)
    return sudoku,lcolores, val

#lista con los numeros del sudoku

"""
#FACIL
numeros=[0,3,9,0,5,0,1,7,0,
        0,0,5,0,6,0,8,0,0,
        8,0,0,4,0,3,0,0,9,
        0,1,8,0,0,0,3,5,0,
        6,0,0,1,0,5,0,0,7,
        0,7,2,0,0,0,9,6,0,
        3,0,0,5,0,9,0,0,2,
        0,0,1,0,3,0,4,0,0,
        0,9,4,0,7,0,6,3,0]

#INTERMEDIO
numeros=[8,0,0,7,0,9,5,0,0,
        0,0,6,0,0,8,0,3,0,
        0,0,0,0,4,5,0,0,0,
        0,0,0,0,0,3,0,0,5,
        9,0,5,0,0,0,6,0,3,
        7,0,0,9,0,0,0,0,0,
        0,0,0,5,8,0,0,0,0,
        0,6,0,4,0,0,8,0,0,
        0,0,2,6,0,7,0,0,9]                   

#DIFICIL

numeros=[0,0,0,0,4,0,0,5,0,
        5,0,4,6,0,3,8,0,0,
        0,3,0,0,0,5,0,7,0,
        0,6,2,0,0,0,0,3,0,
        8,0,3,0,0,0,7,0,9,
        0,7,0,0,0,0,6,2,0,
        0,5,0,4,0,0,0,8,0,
        0,0,6,2,0,7,5,0,3,
        0,8,0,0,5,0,0,0,0]
"""

"""
#Ploting del grafo
sudoku=grafo_sudoku(numeros)
sudoku.vs["label"] = ['Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω', 'Ϊ', 'Ϋ',
                    'ά', 'έ', 'ή', 'ί', 'ΰ', 'α', 'β', 'γ', 'δ',
                    'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν',
                    'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'φ',
                    'χ', 'ψ', 'ω', 'ϊ', 'ϋ', 'ό', 'ύ', 'ώ', 'Ϗ',
                    'ϐ', 'ϑ', 'ϒ', 'ϓ', 'ϔ', 'ϕ', 'ϖ', 'ϗ', 'Ϙ',
                    'ϙ', 'Ϛ', 'ϛ', 'Ϝ', 'ϝ', 'Ϟ', 'ϟ', 'Ϡ', 'ϡ',
                    'Ϣ', 'ϣ', 'Ϥ', 'ϥ', 'Ϧ', 'ϧ', 'Ϩ', 'ϩ', 'Ϫ',
                    'ϫ', 'Ϭ', 'Ϯ', 'ϯ', 'ϰ', 'ϱ', 'ϲ', 'ϳ', 'ϴ']

layout = sudoku.layout_grid()
global color_dict 
color_dict= {0: "white", 1: "pink",2:"green",3:"yellow",4:"red",5:"purple",6:"orange",7:"light blue",8:"dark green",9:"Cadet Blue"}
sudoku.vs["color"] = [color_dict[number] for number in sudoku.vs["numero"]]
colores=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]

sudoku,listaSol,val=solve_sudoku(sudoku)
color_dict = {"white":0, "pink":1,"green": 2,"yellow":3,"red":4,"purple":5,"orange":6,"light blue":7,"dark green":8,"Cadet Blue":9}

t_cl= []
for i in listaSol:
  t_cl.append(color_dict.get(i))

count=0
line=0
for i in t_cl:
  print(i, end=" ")
  count+=1
  if count % 3 == 0 and count != 9:
    print('|',end=' ')
  elif count % 9 == 0:
    print()
    line+=1
    if line % 3 == 0 and line != 9:
      print('------+-------+-------')
    count=0
  
if val:
    plot(sudoku, layout=layout)
else:
    y=input("p?")
    if y=="y":
        plot(sudoku, layout=layout)





"""
"""
aristas_ij=sudoku.es.select(_within=[i,j])
            if len(aristas_ij)>0:
                if sudoku.vs[j]["color"]!="white" and sudoku.vs[i]["color"]=="white":
                        if sudoku.vs[i]["label"] in grados_color.keys():
                            grados_color[sudoku.vs[i]["label"]]+=1
                        else:
                            grados_color[sudoku.vs[i]["label"]]=1


if (g.vs[i]["casilla"][1]==g.vs[j]["casilla"][1] or g.vs[i]["casilla"][0]==g.vs[j]["casilla"][0]) and g.vs[i]["cuadrante"]==g.vs[j]["cuadrante"]:
    if len(g.es.select(_within=[i,j]))==1:
        atributos["tipo"]=0
       g.add_edges([(i,j)],attributes=atributos)

def aux(sudoku,firs,bien):
    cambio=0
    cp_sudoku=sudoku
    pos=0
    
    if b:
        for i in range(81):
            posible=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]
            if cp_sudoku.vs[i]["color"]=="white":
                for j in range(81):
                    if cp_sudoku.vs[j]["color"]!="white" and len(cp_sudoku.es.select(_within=[i,j]))!=0:
                        if cp_sudoku.vs[j]["color"] in posible:
                            posible.remove(cp_sudoku.vs[j]["color"])
                #print(len(posible))
                if len(posible)==2:
                    print("A3",cp_sudoku.vs[i]["casilla"],posible)
                    pos=i
                    break  

        cp_sudoku.vs[pos]['color']=posible[0]
        b=False
        solve_sudoku(cp_sudoku)
    
    if not b and bien:
        for i in range(81):
            posible=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]
            if cp_sudoku.vs[i]["color"]=="white":
                for j in range(81):
                    if cp_sudoku.vs[j]["color"]!="white" and len(cp_sudoku.es.select(_within=[i,j]))!=0:
                        if cp_sudoku.vs[j]["color"] in posible:
                            posible.remove(cp_sudoku.vs[j]["color"])
                #print(len(posible))
                if len(posible)==2:
                    print("A3",cp_sudoku.vs[i]["casilla"],posible)
                    pos=i
                    break  

        cp_sudoku.vs[pos]['color']=posible[0]
        b=False
        aux(cp_sudoku,b,bien)
    if not bien:
        pass

    

    if cp_bol:
        aux(cp_sudoku)

for o in range(81):
        posible=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]
        if sudoku.vs[o]["color"]=="white":
            for p in range(81):
                if sudoku.vs[p]["color"]!="white" and len(sudoku.es.select(_within=[o,p]))!=0:
                    if sudoku.vs[p]["color"] in posible:
                        posible.remove(sudoku.vs[p]["color"])
#seleccionamos las listas de colores de los vertices en el cuadrante de o
            listaC=[]
            for vert in coloresdic.keys():
                if sudoku.vs[o]["cuadrante"]==sudoku.vs[vert]["cuadrante"]:
                    if o!=vert:
                        listaC.append(coloresdic[vert])
                                
#se toma el color que que este en la interseccion de listaC y posible
            intersec=itr(listaC,posible)
            if len(intersec)==1:
                cambio+=1
                print("A2",sudoku.vs[o]["casilla"],intersec)
                sudoku.vs[o]["color"]=intersec[0]
"""
