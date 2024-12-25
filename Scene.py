from model import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        self.skybox = SkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # Пол
        n, s = 100, 10
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, tex_id=0, scale=(s, 1, s), pos=(x, -10, z)))
        # Объекты сцены
        count, distance = 5, 20
        for i in range(-50, count * distance - 50, distance):
            add(Umbrella(app, scale=(0.05, 0.05, 0.05), pos=(i+0, -10, -10)))
            add(Beach_Towels(app, scale=(0.05, 0.05, 0.05), pos=(i-3.5, -9, -6.5), rot=(-90, 40+i,0)))
            add(Beach_Ball(app, scale=(0.06, 0.06, 0.06), pos=(i-1, -7.5, -9.5), rot=(40,40+i*2,0)))
        add(Boat(app,  scale=(2.5, 2.5, 2.5), pos=(-25, -9.5, -30), rot=(-5,65,-5)))

    def update(self):
        pass

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()
