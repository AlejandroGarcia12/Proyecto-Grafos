import pygame
from igraph import *
import Sudoku as sd
#import requests

WIDTH = 550
background_color = (251,247,245)
original_grid_element_color = (52, 31, 151)
buffer = 5

response = {"board":[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]}
grid = response['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def insert(win, position):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i-1][j-1] != 0):
                    return
                if(event.key == 48): #checking with 0
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    pygame.display.update()
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    win.blit(value, (position[0]*50 +15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return
        

def list2dic(lista):
    count=0
    re=[]
    res=[]
    for i in lista:
        re.append(i)
        if count != 8:
            count+=1
        else:
            count=0
            res.append(re)
            re=[]
            
    return res



def dif(win,dif):
    #FACIL
    numeros1=[0,3,9,0,5,0,1,7,0,
            0,0,5,0,6,0,8,0,0,
            8,0,0,4,0,3,0,0,9,
            0,1,8,0,0,0,3,5,0,
            6,0,0,1,0,5,0,0,7,
            0,7,2,0,0,0,9,6,0,
            3,0,0,5,0,9,0,0,2,
            0,0,1,0,3,0,4,0,0,
            0,9,4,0,7,0,6,3,0]

    #INTERMEDIO
    numeros2=[8,0,0,7,0,9,5,0,0,
            0,0,6,0,0,8,0,3,0,
            0,0,0,0,4,5,0,0,0,
            0,0,0,0,0,3,0,0,5,
            9,0,5,0,0,0,6,0,3,
            7,0,0,9,0,0,0,0,0,
            0,0,0,5,8,0,0,0,0,
            0,6,0,4,0,0,8,0,0,
            0,0,2,6,0,7,0,0,9]  

    #DIFICIL
    numeros3=[0,0,0,0,4,0,0,5,0,
            5,0,4,6,0,3,8,0,0,
            0,3,0,0,0,5,0,7,0,
            0,6,2,0,0,0,0,3,0,
            8,0,3,0,0,0,7,0,9,
            0,7,0,0,0,0,6,2,0,
            0,5,0,4,0,0,0,8,0,
            0,0,6,2,0,7,5,0,3,
            0,8,0,0,5,0,0,0,0]

    if dif =='1':
        new = {"board":list2dic(numeros1)}
    elif dif == '2':
        new = {"board":list2dic(numeros2)}
    elif dif == '3':
        new = {"board":list2dic(numeros3)}

    grid = new['board']
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 4 )
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4 )

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 2 )
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2 )
    pygame.display.update()
    
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
    pygame.display.update()

def sol(dif):
    #FACIL

    numeros1=[0,3,9,0,5,0,1,7,0,
            0,0,5,0,6,0,8,0,0,
            8,0,0,4,0,3,0,0,9,
            0,1,8,0,0,0,3,5,0,
            6,0,0,1,0,5,0,0,7,
            0,7,2,0,0,0,9,6,0,
            3,0,0,5,0,9,0,0,2,
            0,0,1,0,3,0,4,0,0,
            0,9,4,0,7,0,6,3,0]

    #INTERMEDIO
    numeros2=[8,0,0,7,0,9,5,0,0,
            0,0,6,0,0,8,0,3,0,
            0,0,0,0,4,5,0,0,0,
            0,0,0,0,0,3,0,0,5,
            9,0,5,0,0,0,6,0,3,
            7,0,0,9,0,0,0,0,0,
            0,0,0,5,8,0,0,0,0,
            0,6,0,4,0,0,8,0,0,
            0,0,2,6,0,7,0,0,9]  

    #DIFICIL
    numeros3=[0,0,0,0,4,0,0,5,0,
            5,0,4,6,0,3,8,0,0,
            0,3,0,0,0,5,0,7,0,
            0,6,2,0,0,0,0,3,0,
            8,0,3,0,0,0,7,0,9,
            0,7,0,0,0,0,6,2,0,
            0,5,0,4,0,0,0,8,0,
            0,0,6,2,0,7,5,0,3,
            0,8,0,0,5,0,0,0,0]
    print(dif)
    if dif =='1':
        solu = sd.solver_sudoku(numeros1)
    elif dif == '2':
        solu = sd.solver_sudoku(numeros2)
    elif dif == '3':
        solu = sd.solver_sudoku(numeros3)

    new = {"board":list2dic(solu)}
    grid = new['board']
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Solucion "+diff)
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 4 )
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4 )

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 2 )
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2 )
    pygame.display.update()
    print(grid)  
    cont=0
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if dif=="1":
                if numeros1[cont]==grid[i][j]:
                    #print(numeros1[cont],grid[i][j])
                    value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
                else:
                    value = myfont.render(str(grid[i][j]), True, (0,0,0))
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
            elif dif=="2":
                if numeros2[cont]==grid[i][j]:
                    value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
                else:
                    value = myfont.render(str(grid[i][j]), True, (0,0,0))
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
            elif dif=="3":
                if numeros3[cont]==grid[i][j]:
                    value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
                else:
                    value = myfont.render(str(grid[i][j]), True, (0,0,0))
                    win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
            cont+=1
    pygame.display.update()
    


def main():    
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 4 )
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4 )

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 2 )
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2 )
    pygame.display.update()
    
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
    pygame.display.update()
            
        
    while True: 
        global diff
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    diff='1' 
                    dif(win,diff)
                    print(diff)
                if event.key == pygame.K_2:
                    diff='2'
                    dif(win,diff)
                    print(diff)
                if event.key == pygame.K_3:
                    diff='3'
                    dif(win,diff)
                    print(diff)
                if event.key == pygame.K_4:
                    sol(diff)
                                
            if event.type == pygame.QUIT:
                pygame.quit()
                return
   
main()