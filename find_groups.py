import random
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Size = namedtuple('Size', ['w', 'h'])

EMPTY = 0
BLACK = 1
WHITE = 2

BOARD_LETTERS = 'ABCDEFGHJKLMNOPQRST'


class Group:
    def __init__(self, color):
        self.color = color
        self.points = set()
        self.liberties = set()

    def get_num_liberties(self):
        return len(self.liberties)

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return '<group color={} {} points {} liberties>'.format(
            self.color, len(self.points), len(self.liberties))


class Board:
    def __init__(self, size):
        self.size = size
        self.stones = {}
        self.utilidad = 0

    def random_fill(self, seed=None):
        rand = random.Random(seed)

        for point in self.iter_points():
            color = rand.choice([EMPTY, BLACK, WHITE])
            if color != EMPTY:
                self.stones[point] = color

    def fill_basic(self):
        self.stones[Point(2,2)] = 2

    def fill(self):
        for point in self.iter_points():
            #color = rand.choice([EMPTY, BLACK, WHITE])
            #if color != EMPTY:
            self.stones[point] = EMPTY        

    def move(self,x,y,t):
        point = Point(x,y)
        self.stones[point] = WHITE if t == 1 else BLACK

    def is_inside(self, point):
        return 0 <= point.x < self.size.w and 0 <= point.y < self.size.h

    def get_color(self, point):
        return self.stones.get(point, 0)

    def get_neighbours(self, point):
        x, y = point

        points = [Point(x-1, y), Point(x+1, y), Point(x, y-1), Point(x, y+1)]
        return filter(self.is_inside, points)

    def iter_points(self):
        for x in range(self.size.w):
            for y in range(self.size.h):
                yield Point(x, y)

    def es_hoja(self):
        resp = True
        for i in range(0,self.size.w):
            for j in range(0,self.size.h):
                #print(board.stones[Point(i,j)])
                point = Point(i,j)
                if(self.stones[point] == 0):
                    resp = False
        return resp

    def find_groups(self):
        groups = []
        grouped_points = set()
        try:
            for point, color in self.stones.items():
                #assert color != EMPTY
                if point in grouped_points:
                    continue

                group = Group(color)

                todo = [point]
                while todo:
                    point = todo.pop()
                    if point not in grouped_points:
                        color = self.stones.get(point, EMPTY)
                        if color == EMPTY:
                            group.liberties.add(point)
                        elif color == group.color:
                            group.points.add(point)
                            grouped_points.add(point)
                            todo.extend(self.get_neighbours(point))

                groups.append(group)
            
        except AssertionError:
            print("Oops!  That was no valid number.  Try again...")
            #pass

        return groups

    def get_new_board(self,cap):
        
        #self.stones[point] = WHITE if t == 0 else BLACK
        for i in range(0,self.size.w):
            for j in range(0,self.size.h):
                point = Point(i,j)
                #print(cap.stones[point])

    def copy(self):
        board_new = Board(Size(5,5))
        for x in range(self.size.w):
            for y in range(self.size.h):
                point = Point(x,y)
                board_new.stones[point] = self.stones[point]
        return board_new


def print_board(board):
    color_chars = {
        # Characters that are easy to tell apart at a glance.
        EMPTY: '.',
        BLACK: '#',
        WHITE: 'o',
    }

    print()
    print('    ', ' '.join(BOARD_LETTERS[:board.size.w]))
    print()

    for y in range(board.size.h):
        line = []
        for x in reversed(range(board.size.w)):
            line.append(color_chars[board.get_color(Point(x, y))])

        rownum = board.size.h - y

        print(' {:2} '.format(rownum), ' '.join(line))
    print()


def print_captured_groups(board, groups, board_size):
    board_new = Board(board_size)
    for group in groups:
        #print(group)
        if group.get_num_liberties() == 0:
            for point in group.points:
                board_new.stones[point] = group.color
                board.stones[point] = 0
    #print_board(board)
    #print("--------------------- seccion capturas --------------------")
    #print_board(board_new)
    #print(board)
    #print("-----------------------------------------------------------")
    return board_new

def get_num_capture(board,groups,board_size,turno):
    board_new = Board(board_size)
    num = 0
    for group in groups:
        if group.get_num_liberties() == 0:
            for point in group.points:
                board_new.stones[point] = group.color
                if group.color == turno:
                    num += 1
    return num


#board = Board(Size(9, 9))
#board.random_fill(seed=13)

#print('Board:')
#print_board(board)

#groups = board.find_groups()

#print('Captured groups:')
#print_captured_groups(groups, board.size)