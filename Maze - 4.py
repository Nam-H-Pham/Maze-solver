import pygame
import time
import random
import numpy as np
import sys
import math
import operator

pygame.init()

class ColourLibrary:
    def __init__(self):
        self.GREY =  (240, 240, 240)
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.RED   = (255, 100, 100)
        self.GREEN = (  0, 255,   0)
        self.BLUE  = ( 100,100, 255)
        self.SILVER= (192, 192, 192)
        self.GOLD  = (255, 215,   0)
        self.PURPLE= (128,   0, 128)
        self.ORANGE= (255, 165,   0)
        self.YELLOW= (255, 204,   0)

Colours = ColourLibrary()

def ClickedRegion(x,y,width,height):
    mx,my = pygame.mouse.get_pos()
    if mx > x and mx < x + width:
        if my > y and my < y + height:
            return True
    else:
        return False

class MazeData:
    def __init__(self):
        pass

    class UnitData:
        def __init__(self):
            self.value = 'EMPTY'
            self.colour = Colours.GREY
        
    def Initiate_Empty_Maze_Matrix(self):
        self.matrix = [[self.UnitData() for i in range(self.units_x)] for i in range(self.units_y)]
        self.matrix = np.array(self.matrix)
        
        for unit_y in range(self.units_y):
            for unit_x in range(self.units_x):
                unit = (self.matrix)[unit_y][unit_x] #returns type UnitData
                x = unit_x*self.unit_size
                y = unit_y*self.unit_size
                unit.coordinate = {'x':x,'y':y}
                unit.position = {'x':unit_x,'y':unit_y}

    def Return_Unit_From_Position(self,x,y):
        return (self.matrix)[y][x]

    def Render_Tiles(self):
        padding = self.unit_padding
        for unit_y in range(self.units_y):
            for unit_x in range(self.units_x):
                unit = self.Return_Unit_From_Position(unit_x,unit_y) #returns type UnitData
                x = unit.coordinate['x']+padding
                y = unit.coordinate['y']+padding
                pygame.draw.rect(screen, unit.colour, (x,y,self.unit_size-padding,self.unit_size-padding))

    def Return_Value_Matrix(self):
        matrix = []
        for unit_y in range(self.units_y):
            x_line = []
            for unit_x in range(self.units_x):
                unit = self.Return_Unit_From_Position(unit_x,unit_y)
                x_line.append(unit.value)
            matrix.append(x_line)
        return np.array(matrix)

    def Reevaluate_Start_End(self):
        for unit_y in range(self.units_y):
            for unit_x in range(self.units_x):
                unit = self.Return_Unit_From_Position(unit_x,unit_y) #returns type UnitData
                if unit.value == 'START':
                    self.start_position = unit.position
                if unit.value == 'END':
                    self.end_position = unit.position

    def Return_Neighbors(self,unit):
        x,y = unit.position['x'],unit.position['y']
        above_unit = self.Return_Unit_From_Position(x,y-1)
        below_unit = self.Return_Unit_From_Position(x,y+1)
        left_unit = self.Return_Unit_From_Position(x-1,y)
        right_unit = self.Return_Unit_From_Position(x+1,y)
        neighbors = {
                'above':above_unit,
                'below':below_unit,
                'left':left_unit,
                'right':right_unit,
            }
        return(neighbors)

'''
    def Return_Position_Next(self, location):
        if location = 'above':
            return (self.matrix)[start_position['y']-1][start_position['x']]
'''
        
Maze = MazeData()
Maze.unit_padding = 1

Maze.unit_size = 15
Maze.units_x = 50
Maze.units_y = 40

Maze.screen_width = Maze.unit_size*Maze.units_x
Maze.screen_height = Maze.unit_size*Maze.units_y

Maze.start_position = {'x':None,'y':None}
Maze.end_position = {'x':None,'y':None}

Maze.Initiate_Empty_Maze_Matrix()

'''
a=MazeData.UnitData()
print(a.colour)
'''

screen = pygame.display.set_mode((Maze.screen_width, Maze.screen_height), 0, 32)
pygame.display.set_caption('Maze')

pygame.display.update()

UnitDictionary = {
    'EMPTY':Colours.GREY,
    'WALL':Colours.BLACK,
    'START':Colours.GREEN,
    'END':Colours.RED,
    'SEARCH':Colours.SILVER,
    'TRUEPATH':Colours.BLUE,
}

def UserControls(action):
    if action == 'mouseleftdown':
        if pygame.mouse.get_pressed()[0]==True:
            return True
    if action == 'mouserightdown':
        if pygame.mouse.get_pressed()[2]==True:
            return True
    if action == 'mousemiddledown':
        if pygame.mouse.get_pressed()[1]==True:
            return True
                
    return False

def CreateBoundryWalls():
    #create boundry walls
    for unit_y in range(Maze.units_y):
        for unit_x in range(Maze.units_x):
            unit = Maze.Return_Unit_From_Position(unit_x,unit_y)
            x,y = unit.position['x'],unit.position['y']
            if x == 0 or y == 0:
                unit.value = 'WALL'
                unit.colour = UnitDictionary['WALL']
            if x == Maze.units_x-1 or y == Maze.units_y-1:
                unit.value = 'WALL'
                unit.colour = UnitDictionary['WALL']
    
Tree_Paths = None
end_achieved = False
CreateBoundryWalls()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    Maze.Render_Tiles()
    values_matrix = Maze.Return_Value_Matrix()#matrix of just unit values

    for unit_y in range(Maze.units_y):# apply controls (left click for wall, middle for start/end, right for clear)
        for unit_x in range(Maze.units_x):
            unit = Maze.Return_Unit_From_Position(unit_x,unit_y) #returns type UnitData
            if ClickedRegion(unit.coordinate['x'],unit.coordinate['y'],Maze.unit_size,Maze.unit_size) == True:
                if UserControls('mouseleftdown')==True:
                        unit.value = 'WALL'
                        unit.colour = UnitDictionary['WALL']
                if UserControls('mouserightdown')==True:
                        unit.value = 'EMPTY'
                        unit.colour = UnitDictionary['EMPTY']
                if UserControls('mousemiddledown')==True:
                        if 'START' not in values_matrix:
                            unit.value = 'START'
                            unit.colour = UnitDictionary['START']
                            start_position = {'x':unit_x,'y':unit_y}
                        elif 'END' not in values_matrix:
                            unit.value = 'END'
                            unit.colour = UnitDictionary['END']
                            end_position = {'x':unit_x,'y':unit_y}
                        if 'START' in values_matrix and 'END' in values_matrix:
                            Maze.Reevaluate_Start_End()
                            
    if 'START' in values_matrix and 'END' in values_matrix:
        if Tree_Paths == None:#setup beggining unit at the start unit
            Tree_Paths = ([[Maze.Return_Unit_From_Position(Maze.start_position['x'],Maze.start_position['y'])]])
            
        if Tree_Paths != None and end_achieved == False:
            New_Tree_Paths = []#begin finding neghbors and branching out the tree
            for path in Tree_Paths:
                unit = path[-1:][0]
                neighbors = Maze.Return_Neighbors(unit)
                
                neighbor_values = [neighbors['above'].value,neighbors['below'].value,neighbors['left'].value,neighbors['right'].value]

                if 'END' in neighbor_values:#actions upon finding end as neighbor
                    end_achieved = True
                    for final_path_units in path:
                        final_path_units.value = 'TRUEPATH'
                        final_path_units.colour = UnitDictionary['TRUEPATH']
                    start_unit = Maze.Return_Unit_From_Position(Maze.start_position['x'],Maze.start_position['y'])
                    start_unit.value = 'START'
                    start_unit.colour = UnitDictionary['START']
                    break
                
                for relation, neighboring_unit in neighbors.items():#record new viable neighbors in tree
                    if neighboring_unit.value == 'EMPTY':
                        newpath = np.append(path,neighboring_unit)
                        New_Tree_Paths.append(newpath)
                        
                for relation, neighboring_unit in neighbors.items():#set read units as already searched
                    if neighboring_unit.value == 'EMPTY':
                        neighboring_unit.value = 'SEARCH'
                        neighboring_unit.colour = UnitDictionary['SEARCH']
                        
            Tree_Paths = New_Tree_Paths
            '''
            Tree path visualisation
            
            [[path1],[path2],[path3]] <- path is a branch of the tree
            |
            V
            [[unit1,u2,u3],[unit1,u2,u3],[unit1,u2,u3],[unit1,u2,u3]]

            get neighboring empty units of last in each path
            '''
            print('Tree Branches',len(Tree_Paths))
            if len(Tree_Paths) == 0:
                print('no possible paths')


    pygame.display.update()
    screen.fill(Colours.WHITE)
