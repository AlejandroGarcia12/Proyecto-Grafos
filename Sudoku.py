from operator import pos
from typing import SupportsComplex
from igraph import *
#creacion del grafo

n=3
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
        cont=1
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1    

    for l in range(3):
        cont=4
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1    
    for l in range(3):
        cont=7
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

def itr(listolist, lista):
    
    inter=[]
    for i in lista:
        cont=0
        for listas in listolist:
            if i in listas:
                cont+=1
                if cont==len(listolist):
                    inter.append(i)
                
    return inter

#lista con los numeros del sudoku
numeros=[0,0,0,0,1,0,0,0,0,
 0,2,0,0,0,0,0,9,5,
 0,7,0,0,5,0,0,0,3,
 0,0,2,3,0,0,7,0,1,
 0,0,0,7,0,0,4,0,0,
 4,3,0,8,0,0,0,0,0,
 6,5,0,4,0,0,0,0,0,
 0,0,0,0,6,2,0,0,0,
 0,9,0,0,0,0,0,7,0]


def solve_sudoku(sudoku):
    incompleto=True
    cambio=1
    while incompleto:
        cambio=0
        
        for i in range(81):
            posible=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]
            if sudoku.vs[i]["color"]=="white":
                for j in range(81):
                    if sudoku.vs[j]["color"]!="white" and len(sudoku.es.select(_within=[i,j]))!=0:
                        if sudoku.vs[j]["color"] in posible:
                            posible.remove(sudoku.vs[j]["color"])
                #print(len(posible))
                if len(posible)==1:
                    print("A1",sudoku.vs[i]["casilla"],posible)
                    sudoku.vs[i]["color"]=posible[0]
                    cambio+=1
                    
#crear el diccionario con la lista de colores que no pueden ir en los vertices no coloreados
        coloresdic={}
        for k in range(81):
            listaC=[]
            for kk in range(81):
                if len(sudoku.es.select(_within=[k,kk]))!=0 and sudoku.vs[k]["color"]=="white":
                    for aris in sudoku.es.select(_within=[k,kk]):
                        if aris["tipo"]==0:
                            if sudoku.vs[kk]["color"] not in listaC:
                                listaC.append(sudoku.vs[kk]["color"])
                                coloresdic[k]=listaC
                    #print(coloresdic)
#encontrar los posibles colores para el vertice o
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
                #if o==4:
                    #print(listaC,"##",posible)
                intersec=itr(listaC,posible)
                if len(intersec)==1:
                    cambio+=1
                    print("A2",sudoku.vs[o]["casilla"],intersec)
                    sudoku.vs[o]["color"]=intersec[0]
#revisamos si esta resuelto el sudoku
        for i in range(81):
            if sudoku.vs[i]["color"]!="white":
                incompleto=False
            else:
                incompleto=True
                break


        if cambio==0:
            break
    
    lcolores=[]
    for i in range(81):
        lcolores.append(sudoku.vs[i]["color"])

    print(incompleto)
    return sudoku,lcolores
                    
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
color_dict = {0: "white", 1: "pink",2:"green",3:"yellow",4:"red",5:"purple",6:"orange",7:"light blue",8:"dark green",9:"Cadet Blue"}
sudoku.vs["color"] = [color_dict[number] for number in sudoku.vs["numero"]]
colores=["pink","green","yellow","red","purple","orange","light blue","dark green","Cadet Blue"]

sudoku,listaSol=solve_sudoku(sudoku)
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
  

plot(sudoku, layout=layout)






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
"""
