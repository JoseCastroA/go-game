from find_groups import *

board = Board(Size(5,5))
#board.fill_basic()
board.fill()
board.random_fill()

print_board(board)
groups = board.find_groups()    
cap = print_captured_groups(board, groups, board.size)
print_board(cap)
print_board(board) 

def play():
    board.fill()
    turno = 0
    while True:
        x = int(input("Fila : "))
        y = int(input("Columna : "))

        board.move(x,y,turno)
        turno = 1
        groups = board.find_groups()    
        cap = print_captured_groups(board, groups, board.size)
        print_board(board) 

                

def utilidad(board,turno):
    tur = 1 if turno ==2 else 2
    groups = board.find_groups()       
    num = get_num_capture(board,groups,board.size,tur)
    return num

def generate(board,t):
    list_child = []
    for i in range(0,board.size.w):
        for j in range(0,board.size.h):
            #print(board.stones[Point(i,j)])
            if(board.stones[Point(i,j)] == 0):
                boadr_child = board.copy() #Board(Size(5,5))
                #print("----------------------")
                #boadr_child.stones = board.stones
                #print_board(boadr_child)
                boadr_child.move(i,j,t)
                #print_board(cap)
                u = utilidad(boadr_child,t)
                boadr_child.utilidad = u

                list_child.append(boadr_child)
    
    return list_child

pasos = 0
def cutoff(board,turno,profundidad,limite):
    global pasos
    pasos += 1
    print("Paso : ",pasos)
    #groups = board.find_groups()    
    #cap = print_captured_groups(board, groups, board.size)
    #print("------------- Captura ---------------------")
    #print_board(cap)
    print("------------- Board -----------------------")
    print_board(board)
    
    if(board.es_hoja() or (profundidad >= limite)):
        return utilidad(board,turno)
    else:
        if(turno==2):
            hijos = generate(board,2)
            utilidades = []
            for i in range(0,len(hijos)):
                utilidades.append(cutoff(hijos[i],1,profundidad+1,limite))
            return max(utilidades)
        else:
            hijos = generate(board,1)
            utilidades = []
            for i in range(0,len(hijos)):
                utilidades.append(cutoff(hijos[i],2,profundidad+1,limite))
            return min(utilidades)


if __name__ == "__main__":
    valido = False
    while not valido:
        x = int(input("1. Jugar dos\n2. CutOff\n-> "))
        if(x==1):
            play()
            valido = True
        elif(x==2):
            cutoff(board,1,0,3)
            valido = True
    

#cutoff(board,1,0,3)
#play()