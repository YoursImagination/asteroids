import math
from PIL import Image, ImageTk

class Ship:
    def __init__(self, canvas):
        self.canvas = canvas
        try:
            self.image_base = Image.open("C:\\Users\\marac\\OneDrive\\Изображения\\Импорт с камеры\\Снимок экрана 2024-11-18 174013.png").resize((40, 40))
            self.image_tk = ImageTk.PhotoImage(self.image_base)
        except Exception as e:
            print(f"Ошибка загрузки изображения корабля: {e}")
            self.image_tk = None

        self.x = 800 / 2
        self.y = 600 / 2
        self.angle = 0 
        self.velocity_x = 0 
        self.velocity_y = 0 
        self.acceleration = 0.2

        self.id = self.canvas.create_image(self.x, self.y, image=self.image_tk) if self.image_tk else \
                  self.canvas.create_polygon(self.calculate_triangle_points(), fill="blue")

    def calculate_triangle_points(self):
        length = 40 / 2
        points = [
            (self.x + length * math.cos(math.radians(self.angle)), 
             self.y + length * math.sin(math.radians(self.angle))),
            (self.x + length * math.cos(math.radians(self.angle + 120)), 
             self.y + length * math.sin(math.radians(self.angle + 120))),
            (self.x + length * math.cos(math.radians(self.angle + 240)), 
             self.y + length * math.sin(math.radians(self.angle + 240)))
        ]
        return points

    def rotate(self, direction):
        self.angle += direction * 10
        self.angle %= 360

    def accelerate(self):
        self.velocity_x += self.acceleration * math.cos(math.radians(self.angle))
        self.velocity_y += self.acceleration * math.sin(math.radians(self.angle))

    def decelerate(self):
        self.velocity_x -= self.acceleration * math.cos(math.radians(self.angle))
        self.velocity_y -= self.acceleration * math.sin(math.radians(self.angle))

    def move(self):
        self.x = (self.x + self.velocity_x) % 800
        self.y = (self.y + self.velocity_y) % 600
        self.update_position()

        self.velocity_x *= 0.98
        self.velocity_y *= 0.98

    def update_position(self):
        if self.image_tk:
            self.canvas.coords(self.id, self.x, self.y)
            rotated_image = self.image_base.rotate(-self.angle, resample=Image.BICUBIC)
            self.image_tk = ImageTk.PhotoImage(rotated_image)
            self.canvas.itemconfig(self.id, image=self.image_tk)
        else:
            self.canvas.coords(self.id, *sum(self.calculate_triangle_points(), ()))
