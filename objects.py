from pygame import Surface
import pygame as pg
class Grid:
    def __init__(self,size: tuple,pixel_per_block: int,screen: Surface,lived_color: tuple, default_color: tuple):
        self._pixel_per_block = pixel_per_block
        self._lived_color = lived_color
        self._default_color = default_color
        self._screen = screen
        self.size = size
        self.grid = self._generate_new_grid()
    
    def _generate_new_grid(self):
        return [[0 for l in range(0,self.size[0]+1)] for i in range(0,self.size[1]+1)]

    def fill_by_mouse(self):
        if pg.mouse.get_pressed(3)[0]:
            x,y = pg.mouse.get_pos()
            self.grid[y//self._pixel_per_block][x//self._pixel_per_block] = 1
        elif pg.mouse.get_pressed(3)[2]:
            x,y = pg.mouse.get_pos()
            self.grid[y//self._pixel_per_block][x//self._pixel_per_block] = 0

    def update(self):
        self.fill_by_mouse()
        self.draw()

    def clear(self):
        self.grid = self._generate_new_grid()

    def draw(self):
        for y,row in enumerate(self.grid,0):
            new_row = []
            for x,cell in enumerate(row,0):
                if cell == 1:
                    pg.draw.rect(self._screen,self._lived_color,(x*self._pixel_per_block,y*self._pixel_per_block,self._pixel_per_block,self._pixel_per_block))
                else:
                    pg.draw.rect(self._screen,self._default_color,(x*self._pixel_per_block,y*self._pixel_per_block,self._pixel_per_block,self._pixel_per_block))

    def next_generation(self) -> list:
        new_array = []
        for y,row in enumerate(self.grid,0):
            new_row = []
            for x,cell in enumerate(row,0):
                value = cell
                nie = self.calculate_neibohr((x,y))
                if value == 1  and nie < 4 and nie > 1:
                    pass
                elif value == 0 and nie == 3:
                    value = 1
                else:
                    value = 0
                new_row.append(value)
            new_array.append(new_row)
        return new_array

    def step(self):
        new_array = self.next_generation()
        self.grid = new_array

    def calculate_neibohr(self,cell: tuple) -> int:
        neigbohrs = [
            (-1,0),
            (1,0),
            (0,1),
            (0,-1),
            (1,1),
            (-1,-1),
            (1,-1),
            (-1,1)
        ]
        x,y = cell
        lvd = 0
        for nie in neigbohrs:
            delta_x,delta_y = x-nie[0], y-nie[1]
            try:
                if self.size[0] < delta_x: delta_x = 0
                if self.size[1] < delta_y: delta_y = 0
                if self.grid[delta_y][delta_x]:
                    lvd += 1
            except: pass
        return lvd
        