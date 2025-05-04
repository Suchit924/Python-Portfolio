import turtle
import time
import random

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.setup(width=800, height=600)
wn.tracer(0)

# Register shapes
alien_shapes = ["circle", "square", "triangle"]
player_shape = "turtle"

# Score
score = 0

# Create player
player = turtle.Turtle()
player.color("white")
player.shape(player_shape)
player.penup()
player.goto(0, -250)
player.setheading(90)
player_speed = 20

# Create bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("square")
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
bullet.penup()
bullet.goto(0, -400)  # Hide initially
bullet_state = "ready"
bullet_speed = 40

# Create enemies
enemies = []
enemy_speed = 10
enemy_move_down = 20

rows = 3
cols = 6
for row in range(rows):
    for col in range(cols):
        enemy = turtle.Turtle()
        enemy.color("green")
        enemy.shape(random.choice(alien_shapes))
        enemy.penup()
        x = -300 + (col * 80)
        y = 180 - (row * 60)
        enemy.goto(x, y)
        enemies.append(enemy)

# Create barriers
barriers = []
for i in range(-200, 201, 200):
    barrier = turtle.Turtle()
    barrier.shape("square")
    barrier.color("blue")
    barrier.penup()
    barrier.goto(i, -150)
    barriers.append(barrier)

# Create game over text
game_over_text = turtle.Turtle()
game_over_text.color("red")
game_over_text.penup()
game_over_text.hideturtle()
game_over_text.goto(0, 0)

# Functions
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -370:
        x = -370
    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x > 370:
        x = 370
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)

def is_collision(t1, t2):
    return t1.distance(t2) < 20

def move_enemies():
    global enemy_speed  # Declare global only once, at the start
    for enemy in enemies:
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

    # Check for edge
    edge_hit = any(enemy.xcor() > 360 or enemy.xcor() < -360 for enemy in enemies)
    if edge_hit:
        for enemy in enemies:
            y = enemy.ycor()
            y -= enemy_move_down
            enemy.sety(y)
        enemy_speed *= -1  # Already declared global, so modify it directly


# Key bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Main game loop
game_running = True
last_enemy_move = time.time()

while game_running:
    wn.update()

    # Move bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

        if y > 300:
            bullet.goto(0, -400)
            bullet_state = "ready"

    # Bullet collision with enemy
    for enemy in enemies:
        if is_collision(bullet, enemy):
            bullet.goto(0, -400)
            bullet_state = "ready"
            enemy.goto(1000, 1000)  # move off screen
            enemies.remove(enemy)
            score += 10

    # Enemy collision with player
    for enemy in enemies:
        if is_collision(enemy, player) or enemy.ycor() < -220:
            game_over_text.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
            game_running = False
            break

    # Bullet collision with barriers
    for barrier in barriers:
        if is_collision(bullet, barrier):
            bullet.goto(0, -400)
            bullet_state = "ready"

    # Enemy collision with barriers
    for enemy in enemies:
        for barrier in barriers:
            if is_collision(enemy, barrier):
                barrier.goto(1000, 1000)
                barriers.remove(barrier)

    # Move enemies every second
    if time.time() - last_enemy_move > 1:
        move_enemies()
        last_enemy_move = time.time()

wn.mainloop()
