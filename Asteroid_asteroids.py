import random
import math
from PIL import Image, ImageTk

class Asteroid:
    def __init__(self, canvas):
        self.canvas = canvas
        try:
            image = Image.open("C:\\Users\\marac\\OneDrive\\Изображения\\Импорт с камеры\\Снимок экрана 2024-11-18 173847.png").resize((50, 50))
            self.image = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Ошибка загрузки изображения астероида: {e}")
            self.image = None

        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(1, 2 * 2)

        if self.image:
            self.id = self.canvas.create_image(self.x, self.y, image=self.image)
        else:
            self.id = self.canvas.create_oval(self.x - 25, self.y - 25, 
                                              self.x + 25, self.y + 25, fill="gray")

    def move(self):
        self.x = (self.x + self.speed * math.cos(math.radians(self.angle))) % 800
        self.y = (self.y + self.speed * math.sin(math.radians(self.angle))) % 600

        if self.image:
            self.canvas.coords(self.id, self.x, self.y)
        else:
            self.canvas.coords(self.id, self.x - 25, self.y - 25, 
                               self.x + 25, self.y + 25)
