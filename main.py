from multiprocessing import Event
from objects import Grid
import pygame as pg
pg.init()
pg.font.init()

class MainApp:
    """
    Functions:
        __init__
    """

    WIDTH = 1280
    HEIGHT = 720
    _stopped = True
    _last_time = 0
    _space_time = 0
    _arrow_time = 0
    def __init__(self, pixel_per_block: int = 10,fps: int = 60) -> None:
        """
        pixel_per_block (int): Сколько пискелей занимет 1 блок.
        Returns:
            None
        """
        #Initalisation
        self._screen = pg.display.set_mode((self.WIDTH,self.HEIGHT))
        self._screen.fill((176, 196, 222))
        self._clock = pg.time.Clock()
        self._pixel_per_block = pixel_per_block
        self.rows = self.WIDTH//pixel_per_block
        self.cols = self.HEIGHT//pixel_per_block
        self._grid = Grid((self.rows,self.cols),pixel_per_block,self._screen,(0,0,0),(176, 196, 222))
        self.draw_net()
        self._fps = fps
        self.__f1 = pg.font.Font(None,50)
        self.__f2 = pg.font.Font(None,27)
        self._generation = 0
        self._time_delay = 1000//10
        
    def fonts_render(self):
        #Render Fonts(текста и ui)
        generation = self.__f1.render(f"Generation: {self._generation}",True,(105, 105, 105))
        stoped = self.__f1.render(f"Stopped: {self._stopped}",True,(105, 105, 105))
        text = """Левая кнопка мыши - создать клетку
        Правая кнопка мыши - уничтожить клетку
        Пробел - запустить\остановить
        С - очистить поле
        Стрелка вправо - следующие поколение
        """
        y = 200
        for row in text.split('\n'):
            instruction = self.__f2.render(row,True,(105, 105, 105))
            self._screen.blit(instruction,(830,y))
            y += 30
        self._screen.blit(stoped,(0,50))
        self._screen.blit(generation,(500,50))
        
    
    def iter(self):
        #Функция итерации
        self.check_events()
        if not self._stopped and pg.time.get_ticks() - self._last_time >= self._time_delay:
            self._grid.step()
            self._generation += 1
            self._last_time = pg.time.get_ticks()

    def draw_net(self):
        #Отрисовка сетки
        x,y = 0,0
        while x < self.WIDTH:
            x += self._pixel_per_block
            pg.draw.line(self._screen,((119, 136, 153)),(x,0),(x,self.HEIGHT))
        while y < self.HEIGHT:
            y += self._pixel_per_block
            pg.draw.line(self._screen,((119, 136, 153)),(0,y),(self.WIDTH,y))

    def clear(self):
        #Метод отчистки поля
        self._stopped = True
        self._generation = 0
        self._grid.clear()

    def check_events(self):
        #проверка нажатий кнопок
        events = pg.key.get_pressed()
        if events[pg.K_SPACE] and pg.time.get_ticks()-self._space_time >= 1000:
            self._stopped = not self._stopped
            self._space_time = pg.time.get_ticks()
        if events[pg.K_c]:
            self.clear()
        if events[pg.K_RIGHT] and pg.time.get_ticks() - self._arrow_time >= 300:
            self._grid.step()
            self._generation += 1
            self._arrow_time = pg.time.get_ticks()

    def update(self):
        #Метод обновления приложения
        self._grid.update()
        self.draw_net()
        self.fonts_render()
        pg.display.flip()
        self.iter()

    def run(self):
        #Запуск
        running = True
        while running:
            for event in pg.event.get():
            # проверить закрытие окна
                if event.type == pg.QUIT:
                    running = False
            self.update()
            self._clock.tick(self._fps)

app = MainApp(20,120)
app.run()

