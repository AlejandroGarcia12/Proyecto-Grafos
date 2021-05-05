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
    
    
    for i in range(3):
        cont=1
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1
    
    for i in range(3):
        cont=4
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1

    for i in range(3):
        cont=7
        for j in range(3):
            for i in range(3):
                lcuadro.append(cont)
            cont+=1
    

    g.vs["casilla"]=lcasilla
    g.vs["cuadrante"]=lcuadro
    g.vs["numero"]=numeros

    #for i in range(81):
        #print(g.vs[i])

    for i in range(81):
        for j in range(81):
            if i!=j:
                tipo={}
                if g.vs[i]["casilla"][1]==g.vs[j]["casilla"][1] or g.vs[i]["casilla"][0]==g.vs[j]["casilla"][0]:#estan en la misma fila o columna
                    if len(g.es.select(_within=[i,j]))==0:
                        tipo["tipo"]=1
                        g.add_edges([(i,j)], attributes=tipo)
                if g.vs[i]["cuadrante"]==g.vs[j]["cuadrante"]:#estan en el mismo cuadro 3x3
                    if len(g.es.select(_within=[i,j]))==0:
                        tipo["tipo"]=0
                        g.add_edges([(i,j)],attributes=tipo)
                if (g.vs[i]["casilla"][1]==g.vs[j]["casilla"][1] or g.vs[i]["casilla"][0]==g.vs[j]["casilla"][0]) and g.vs[i]["cuadrante"]==g.vs[j]["cuadrante"]:
                    if len(g.es.select(_within=[i,j]))==1:
                        tipo["tipo"]=0
                        g.add_edges([(i,j)],attributes=tipo)
    return g


#lista con los numeros del sudoku
numeros=[5,3,0,0,7,0,0,0,0,
        6,0,0,1,9,5,0,0,0,
        0,9,8,0,0,0,0,6,0,
        8,0,0,0,6,0,0,0,3,
        4,0,0,8,0,3,0,0,1,
        7,0,0,0,2,0,0,0,6,
        0,6,0,0,0,0,2,8,0,
        0,0,0,4,1,9,0,0,5,
        0,0,0,0,8,0,0,7,9]

def solve_sudoku(sudoku):
    pass


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

sudoku.es["label"] = sudoku.es["tipo"]
print(sudoku.degree())
layout = sudoku.layout_grid()
color_dict = {0: "white", 1: "pink",2:"green",3:"yellow",4:"red",5:"purple",6:"orange",7:"light blue",8:"dark green",9:"brown"}
sudoku.vs["color"] = [color_dict[number] for number in sudoku.vs["numero"]]
plot(sudoku, layout=layout)










                

