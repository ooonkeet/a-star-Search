import pygame
import math
from queue import PriorityQueue

pygame.init()
pygame.font.init()

WIDTH = 700

# set up a window display by dimensions width by width and set the header or caption by A* path finding algorithm
WIN = pygame.display.set_mode((WIDTH,WIDTH))

pygame.display.set_caption("A* path finding algorithm")

# if u write till here and run this you can see a window popping up and disappearing - which means the code is correct

# color code necessaries
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE=(255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

    # WHITE color says that the path is unvisited 
    # RED color says that we already visited that grid box
    # BLACK color says that this block is a barrier, it needs to be avoided by the algorithm
    # ORANGE means the start node
    # TURQUOISE means the end node
    # PURPLE is the path followed by A*
    # GREEN checks on the Open Set - which determines the path, consider it to be a backtracked set containing the path information from starting to ending node

class Spot: 
    #keep track of color of all of the spots and know what location its in
    def __init__(self,row,col,width,total_rows):
        # constructors to initialize
        self.row=row
        self.col=col
        self.x = col * width
        self.y = row * width
        self.color=WHITE #INITIALLY ALL CUBES ARE WHITE
        self.neighbors=[]
        self.width=width
        self.total_rows=total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED 

    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color=BLACK

    def make_end(self):
        self.color=TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self, grid): #form a graph with adj neighbours
        self.neighbors = []
        r, c = self.row, self.col #variated technique

        # straight directions (cost = 1)
        if r < self.total_rows - 1 and not grid[r+1][c].is_barrier():
            self.neighbors.append((grid[r+1][c], 1))
        if r > 0 and not grid[r-1][c].is_barrier():
            self.neighbors.append((grid[r-1][c], 1))
        if c < self.total_rows - 1 and not grid[r][c+1].is_barrier():
            self.neighbors.append((grid[r][c+1], 1))
        if c > 0 and not grid[r][c-1].is_barrier():
            self.neighbors.append((grid[r][c-1], 1))

        # diagonal directions (cost = sqrt(2))
        if r > 0 and c > 0 and not grid[r-1][c].is_barrier() and not grid[r][c-1].is_barrier():
            if not grid[r-1][c-1].is_barrier():
                self.neighbors.append((grid[r-1][c-1], math.sqrt(2)))

        if r > 0 and c < self.total_rows-1 and not grid[r-1][c].is_barrier() and not grid[r][c+1].is_barrier():
            if not grid[r-1][c+1].is_barrier():
                self.neighbors.append((grid[r-1][c+1], math.sqrt(2)))

        if r < self.total_rows-1 and c > 0 and not grid[r+1][c].is_barrier() and not grid[r][c-1].is_barrier():
            if not grid[r+1][c-1].is_barrier():
                self.neighbors.append((grid[r+1][c-1], math.sqrt(2)))

        if r < self.total_rows-1 and c < self.total_rows-1 and not grid[r+1][c].is_barrier() and not grid[r][c+1].is_barrier():
            if not grid[r+1][c+1].is_barrier():
                self.neighbors.append((grid[r+1][c+1], math.sqrt(2)))

    def __lt__(self,other):
        return (self.row, self.col) < (other.row, other.col)
    # lt handles less than - here it means 'other' node is greater than 'self' node

def h(p1,p2):
    # heuristic function having two points p1 and p2, it uses octile distance - admissible and optimal for diagonal grids
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)+(math.sqrt(2)-2)*min(abs(x1-x2),abs(y1-y2)) #diagonal distance

def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()

def algorithm(draw,grid,start,end):
    count = 0 #put a track in case of tie in distance
    open_set=PriorityQueue() #beneficial in getting smalles value/distance
    open_set.put((0,count,start))
    came_from ={} #tracks the history of nodes
    g_score={spot: float("inf") for row in grid for spot in row} #current shortest distance initialised to infinity
    g_score[start]=0
    f_score={spot: float("inf") for row in grid for spot in row} #heuristic distance
    f_score[start]=h(start.get_pos(),end.get_pos()) 
    open_set_hash={start} #check if anything inside priority queue/open set
    while not open_set.empty():
        # if open set is empty it has 2 possibilities:-
        # (i) we have considered every single possible node
        # (ii) path does not exist
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2] #index 2 as it will store -> f score, count and node
        open_set_hash.remove(current) #we take whatever node that we popped out of priority queue and sync it with the open set hash by just removing it from that to make sure we don't have any duplicates or anything out of sync and messing us up
        if current == end:
            #make the shortest path
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True 
        for neighbor,cost in current.neighbors:
            temp_g_score=g_score[current]+cost 
            #little tweak as I add cost instead of 1 important for diagonal
            if temp_g_score<g_score[neighbor]:
                # if we found a better way to reach this neighbor than before update this path and keep track of it
                came_from[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    # if neighbour is not present in open set we add to it
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current!=start:
            # if the current traversed node is not start, mark it red and it wont be considered again as it is in open set
            current.make_closed()
    return False
def make_grid(rows,width): 
    #adjust the grid rows and columns according to width
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=Spot(i,j,gap,rows)
            grid[i].append(spot)

    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        # CAREFULLY WATCH THIS BUSINESS LOGIC

        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))

        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    # first fill the grids with white
    draw_grid(win,rows,width)
    # then draw whatever you want
    pygame.display.update()
    # then update the display

def draw_popup(win, text, width):
    # semi-transparent background overlay
    overlay = pygame.Surface((width, width))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))

    # popup box description
    box_width, box_height = 350, 120
    box_x = (width - box_width) // 2
    box_y = (width - box_height) // 2

    pygame.draw.rect(win, (255, 255, 255),
        (box_x, box_y, box_width, box_height),
        border_radius=10)
    pygame.draw.rect(win, (255, 0, 0),
        (box_x, box_y, box_width, box_height),
         3, border_radius=10)

    # text printup
    font = pygame.font.SysFont("arial", 28, bold=True)
    text_render = font.render(text, True, (255, 0, 0))
    text_rect = text_render.get_rect(center=(width // 2, box_y + 60))
    win.blit(text_render, text_rect)

    pygame.display.update()



def get_clicked_pos(pos,rows,width):
    # click to know where we are
    gap=width//rows
    x,y=pos
    row=y//gap
    col=x//gap
    return row,col

def main(win,width):
    ROWS = 50 #YOU CAN MANUALLY SET BY CHANGING THE GRID NUMBER

    grid = make_grid(ROWS,width)
    start=None
    end=None
    run = True
    while run:
        # loop through all events happened
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            
            if pygame.mouse.get_pressed()[0]: #left click
                pos=pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                if not start and spot!=end:
                    start=spot
                    start.make_start()
                elif not end and spot!=start:
                    end=spot
                    end.make_end()

                elif spot!=end and spot!=start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]: #right click
                pos=pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not start and not end:
                        draw_popup(win, "PLACE START AND END", width)
                        pygame.time.delay(2000)
                        continue
                    if not start:
                        draw_popup(win, "START POINT MISSING", width)
                        pygame.time.delay(2000)
                        continue
                    if not end:
                        draw_popup(win, "END POINT MISSING", width)
                        pygame.time.delay(2000)
                        continue
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    found=algorithm(lambda:draw(win,grid,ROWS,width),grid,start,end)
                    
                    if not found: #if no path exists between start and ending node
                        draw_popup(win,"NO PATH EXISTS",width)
                        pygame.time.delay(5000)

                if event.key==pygame.K_BACKSPACE:
                    start = None
                    end=None
                    grid = make_grid(ROWS,width)
    pygame.quit()

main(WIN,WIDTH)
