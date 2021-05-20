from igraph import *
import Sudoku as sd

def list2dic(lista):
    count=0
    re=[]
    res=[]
    for i in lista:
        re.append(i)
        print(re,count)
        if count != 8:
            count+=1
        else:
            count=0
            res.append(re)
            re=[]
            
    return res

numeros=[0,0,0,0,4,0,0,5,0,
        5,0,4,6,0,3,8,0,0,
        0,3,0,0,0,5,0,7,0,
        0,6,2,0,0,0,0,3,0,
        8,0,3,0,0,0,7,0,9,
        0,7,0,0,0,0,6,2,0,
        0,5,0,4,0,0,0,8,0,
        0,0,6,2,0,7,5,0,3,
        0,8,0,0,5,0,0,0,0]

x=list2dic(numeros)

#Ploting del grafo
sudoku=sd.grafo_sudoku(numeros)
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

sudoku,listaSol,val= sd.solve_sudoku(sudoku)
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



print('resultado:',t_cl)