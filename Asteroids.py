import tkinter as tk
import random
import math
from PIL import Image, ImageTk, ImageDraw
from Ship_asteroids import Ship
from Asteroid_asteroids import Asteroid
import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SHIP_SPEED = 5
ASTEROID_SPEED = 2
ROCKET_SPEED = 10
LIVES = 3
SCORE = 0
SHIP_SIZE = 40
ASTEROID_SIZE = 50
ROCKET_LIFETIME = 80
ASTEROID_SPAWN_INTERVAL = 5000  

class Rocket:
    def __init__(self, canvas, ship_x, ship_y, angle):
        self.canvas = canvas
        self.angle = angle
        self.x = ship_x
        self.y = ship_y
        self.id = self.canvas.create_oval(self.x - 2, self.y - 2, self.x + 2, self.y + 2, fill='red')
        self.speed = ROCKET_SPEED
        self.lifetime = ROCKET_LIFETIME  

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.canvas.coords(self.id, self.x - 2, self.y - 2, self.x + 2, self.y + 2)

        self.lifetime -= 1 
        if self.lifetime <= 0:
            self.canvas.delete(self.id)  
            return False  
        return True

class AsteroidGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        pygame.mixer.init()
        try:
            pygame.mixer.music.load("C:\\Users\\marac\\Downloads\\Telegram Desktop\\audio_2024-12-19_15-07-27.ogg")
            pygame.mixer.music.play(-1)  
        except Exception as e:
            print(f"Ошибка загрузки саундтрека: {e}")

        self.game_running = True

        self.start_frame = tk.Frame(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.start_frame.place(x=0, y=0)
        self.start_frame.lift()  

        self.start_overlay = self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black", stipple="gray75")

        self.start_button = tk.Button(self.start_frame, text="Начать", font=("Arial", 20), command=self.start_game)
        self.start_button.place(relx=0.5, rely=0.4, anchor="center")

        self.quit_button = tk.Button(self.start_frame, text="Выйти из игры", font=("Arial", 20), command=self.root.destroy)
        self.quit_button.place(relx=0.5, rely=0.6, anchor="center")

    def start_game(self):
        self.start_frame.destroy()  
        self.canvas.delete(self.start_overlay) 
        self.initialize_game()

    def initialize_game(self):
        self.ship = Ship(self.canvas)
        self.asteroids = [Asteroid(self.canvas) for _ in range(5)]
        self.rockets = []
        self.lives = LIVES
        self.score = SCORE

        self.score_text = self.canvas.create_text(50, 20, text=f"Очки: {self.score}", fill="white", font=("Arial", 16))
        self.lives_text = self.canvas.create_text(750, 20, text=f"Жизни: {self.lives}", fill="white", font=("Arial", 16))

        self.root.bind("w", lambda e: self.ship.move())  # W - ускорение
        self.root.bind("s", lambda e: self.ship.decelerate())  # S - замедление
        self.root.bind("a", lambda e: self.ship.rotate(-1))   # A - вращение влево
        self.root.bind("d", lambda e: self.ship.rotate(1))    # D - вращение вправо
        self.root.bind("<space>", lambda e: self.fire_rocket())  # Пробел - выстрел

        self.update_game()
        self.spawn_asteroids()

    def fire_rocket(self):
        x, y = self.ship.x, self.ship.y
        self.rockets.append(Rocket(self.canvas, x, y, self.ship.angle))

    def spawn_asteroids(self):
        if self.game_running:
            self.asteroids.append(Asteroid(self.canvas))
            self.root.after(ASTEROID_SPAWN_INTERVAL, self.spawn_asteroids)

    def update_game(self):
        if self.lives > 0:
            self.ship.move()
            for asteroid in self.asteroids:
                asteroid.move()
            self.rockets = [rocket for rocket in self.rockets if rocket.move()]

            self.check_collisions()
            self.update_interface()
        else:
            self.canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text="GAME OVER", fill="red", font=("Arial", 40))
            self.game_running = False

        self.root.after(30, self.update_game)

    def check_collisions(self):
        for asteroid in self.asteroids[:]:
            if self.check_overlap(self.ship.id, asteroid.id):
                self.lives -= 1
                self.canvas.delete(asteroid.id)
                self.asteroids.remove(asteroid)
                self.ship = Ship(self.canvas) 

        for rocket in self.rockets[:]:
            for asteroid in self.asteroids[:]:
                if self.check_overlap(rocket.id, asteroid.id):
                    self.score += 1
                    if self.canvas.find_withtag(rocket.id):
                        self.canvas.delete(rocket.id)
                        self.rockets.remove(rocket)
                    if self.canvas.find_withtag(asteroid.id):
                        self.canvas.delete(asteroid.id)
                        self.asteroids.remove(asteroid)
                    break

    def check_overlap(self, id1, id2):
        bbox1 = self.canvas.bbox(id1)
        bbox2 = self.canvas.bbox(id2)
        if bbox1 is None or bbox2 is None:
            return False
        return (bbox1[0] < bbox2[2] and bbox1[2] > bbox2[0] and
                bbox1[1] < bbox2[3] and bbox1[3] > bbox2[1])

    def update_interface(self):
        self.canvas.itemconfig(self.score_text, text=f"Очки: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Жизни: {self.lives}")

root = tk.Tk()
root.title("Астероиды")
game = AsteroidGame(root)
root.mainloop()
