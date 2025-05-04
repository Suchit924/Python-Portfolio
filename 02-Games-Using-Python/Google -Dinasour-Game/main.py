import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300
GROUND_HEIGHT = 250
DINO_SIZE = 30
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
JUMP_HEIGHT = 100
JUMP_SPEED = 20
GAME_SPEED = 10

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter T-Rex Game")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack()

        self.restart_button = None  # Will hold the button widget

        self.reset_game()

        self.root.bind("<space>", self.jump_handler)

    def reset_game(self):
        # Clear canvas
        self.canvas.delete("all")
        self.dino = self.canvas.create_rectangle(50, GROUND_HEIGHT - DINO_SIZE, 50 + DINO_SIZE, GROUND_HEIGHT, fill="green")
        self.ground = self.canvas.create_line(0, GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT, fill="black")
        self.score_text = self.canvas.create_text(700, 30, text="Score: 0", font=("Arial", 14), fill="black")

        self.obstacles = []
        self.jump = False
        self.jump_velocity = 0
        self.score = 0
        self.game_over = False

        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None

        self.update()

    def jump_handler(self, event):
        if not self.jump and not self.game_over:
            self.jump = True
            self.jump_velocity = -JUMP_SPEED

    def update_dino(self):
        if self.jump:
            self.canvas.move(self.dino, 0, self.jump_velocity)
            self.jump_velocity += 2  # gravity effect
            coords = self.canvas.coords(self.dino)
            if coords[3] >= GROUND_HEIGHT:
                self.canvas.coords(self.dino, coords[0], GROUND_HEIGHT - DINO_SIZE, coords[2], GROUND_HEIGHT)
                self.jump = False

    def create_obstacle(self):
        obstacle = self.canvas.create_rectangle(
            WINDOW_WIDTH, GROUND_HEIGHT - OBSTACLE_HEIGHT,
            WINDOW_WIDTH + OBSTACLE_WIDTH, GROUND_HEIGHT, fill="red"
        )
        self.obstacles.append(obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, -GAME_SPEED, 0)
        # Remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if self.canvas.coords(obs)[2] > 0]

    def check_collision(self):
        dino_coords = self.canvas.bbox(self.dino)
        for obs in self.obstacles:
            if self.canvas.bbox(obs) and self.intersect(dino_coords, self.canvas.bbox(obs)):
                self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", font=("Arial", 30), fill="red")
                self.game_over = True
                self.show_restart_button()
                return True
        return False

    def intersect(self, box1, box2):
        return not (box1[2] < box2[0] or box1[0] > box2[2] or box1[3] < box2[1] or box1[1] > box2[3])

    def update_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def show_restart_button(self):
        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 14), command=self.reset_game)
        self.restart_button.pack(pady=10)

    def update(self):
        if not self.game_over:
            self.update_dino()

            if random.randint(1, 50) == 1:
                self.create_obstacle()

            self.move_obstacles()
            self.update_score()

            if not self.check_collision():
                self.root.after(30, self.update)

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()
