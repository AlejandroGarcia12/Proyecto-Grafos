from igraph import *
#creacion del grafo
def grafo_sudoku():
    g = Graph()
    g.add_vertices(81)
    cuadro=1
    #los vertices tienen 2 atributos: casilla [a,b] y cuadro de 3x3 al que pertenecen
    lcuadro=[]
    lcasilla=[]

    for i in range(9):
        for j in range(9):
            lcasilla.append([i,j])
            lcuadro.append(cuadro)
        cuadro+=1

    g.vs["casilla"]=lcasilla
    g.vs["cuadrante"]=lcuadro


    for i in range(81):
            for j in range(81):
                if i!=j:
                    if g.vs[i]["casilla"][1]==g.vs[j]["casilla"][1] or g.vs[i]["casilla"][0]==g.vs[j]["casilla"][0]:#estan en la misma fila o columna
                        g.add_edges([(i,j)])
                    if g.vs[i]["cuadrante"]==g.vs[j]["cuadrante"]:#estan en el mismo cuadro 3x3
                        g.add_edges([(i,j)])
    return g

sudoku=grafo_sudoku()
plot(sudoku)










                

