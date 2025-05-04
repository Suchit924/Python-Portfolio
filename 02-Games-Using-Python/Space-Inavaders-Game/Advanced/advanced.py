import turtle
import time
import random

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.setup(width=800, height=600)
wn.tracer(0)

# Global variables
score = 0
lives = 3
enemy_speed = 10
enemy_move_down = 20
bullet_speed = 20
bullet_cooldown = 0.3
last_bullet_time = 0
start_time = time.time()

# Create player
player = turtle.Turtle()
player.color("white")
player.shape("triangle")
player.penup()
player.goto(0, -250)
player.setheading(90)
player_speed = 20

# Score display
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-350, 260)

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}  Lives: {lives}", font=("Courier", 14, "normal"))

update_score()

# Game over text
game_over_text = turtle.Turtle()
game_over_text.color("red")
game_over_text.penup()
game_over_text.hideturtle()
game_over_text.goto(0, 0)

# Create enemies
enemies = []
enemy_rows = 3
enemy_cols = 6
alien_shapes = ["circle", "square", "triangle"]

for row in range(enemy_rows):
    for col in range(enemy_cols):
        enemy = turtle.Turtle()
        enemy.color("green")
        enemy.shape(random.choice(alien_shapes))
        enemy.penup()
        x = -300 + (col * 80)
        y = 180 - (row * 60)
        enemy.goto(x, y)
        enemies.append(enemy)

# Create barriers with health
barriers = []
barrier_positions = [-200, 0, 200]
for pos in barrier_positions:
    barrier = turtle.Turtle()
    barrier.shape("square")
    barrier.color("blue")
    barrier.penup()
    barrier.goto(pos, -150)
    barriers.append({"obj": barrier, "health": 3})

# Bullets list
bullets = []

# Functions
def move_left():
    x = player.xcor() - player_speed
    if x < -370:
        x = -370
    player.setx(x)

def move_right():
    x = player.xcor() + player_speed
    if x > 370:
        x = 370
    player.setx(x)

def fire_bullet():
    global last_bullet_time
    if time.time() - last_bullet_time > bullet_cooldown:
        bullet = turtle.Turtle()
        bullet.color("yellow")
        bullet.shape("square")
        bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
        bullet.penup()
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullets.append(bullet)
        last_bullet_time = time.time()

def is_collision(t1, t2):
    return t1.distance(t2) < 20

def move_enemies():
    global enemy_speed
    for enemy in enemies:
        x = enemy.xcor() + enemy_speed
        enemy.setx(x)

    edge_hit = any(enemy.xcor() > 360 or enemy.xcor() < -360 for enemy in enemies)
    if edge_hit:
        for enemy in enemies:
            y = enemy.ycor() - enemy_move_down
            enemy.sety(y)
        enemy_speed *= -1

# Restart game function
def restart_game():
    global score, lives, bullets, enemies, barriers, enemy_speed, bullet_cooldown, start_time, game_running

    # Reset values
    score = 0
    lives = 3
    enemy_speed = 10
    bullet_cooldown = 0.3
    start_time = time.time()
    bullets.clear()
    for b in wn.turtles():
        if b not in [player, score_display, game_over_text]:
            b.hideturtle()
    enemies.clear()
    barriers.clear()
    game_running = True
    game_over_text.clear()

    # Recreate enemies
    for row in range(3):
        for col in range(6):
            enemy = turtle.Turtle()
            enemy.color("green")
            enemy.shape(random.choice(["circle", "square", "triangle"]))
            enemy.penup()
            x = -300 + (col * 80)
            y = 180 - (row * 60)
            enemy.goto(x, y)
            enemies.append(enemy)

    # Recreate barriers
    for pos in [-200, 0, 200]:
        barrier = turtle.Turtle()
        barrier.shape("square")
        barrier.color("blue")
        barrier.penup()
        barrier.goto(pos, -150)
        barriers.append({"obj": barrier, "health": 3})

    update_score()

# Key bindings
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")
wn.onkeypress(restart_game, "r")

# Main game loop
game_running = True
last_enemy_move = time.time()

while game_running:
    wn.update()

    # Bullet movement
    for bullet in bullets[:]:
        y = bullet.ycor() + bullet_speed
        bullet.sety(y)

        # Bullet off screen
        if y > 300:
            bullet.hideturtle()
            bullets.remove(bullet)

    # Bullet collision with enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if is_collision(bullet, enemy):
                bullet.hideturtle()
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemy.goto(1000, 1000)
                score += 10
                update_score()
                break

    # Bullet collision with barriers
    for bullet in bullets[:]:
        for barrier in barriers[:]:
            if is_collision(bullet, barrier["obj"]):
                bullet.hideturtle()
                bullets.remove(bullet)
                barrier["health"] -= 1
                if barrier["health"] == 2:
                    barrier["obj"].color("lightblue")
                elif barrier["health"] == 1:
                    barrier["obj"].color("gray")
                elif barrier["health"] <= 0:
                    barrier["obj"].hideturtle()
                    barriers.remove(barrier)
                break

    # Enemy collision with player or barriers
    for enemy in enemies[:]:
        if is_collision(enemy, player) or enemy.ycor() < -220:
            lives -= 1
            update_score()
            enemies.remove(enemy)
            enemy.hideturtle()
            if lives == 0:
                game_over_text.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
                game_running = False
            break
        for barrier in barriers[:]:
            if is_collision(enemy, barrier["obj"]):
                barrier["health"] -= 1
                if barrier["health"] == 2:
                    barrier["obj"].color("lightblue")
                elif barrier["health"] == 1:
                    barrier["obj"].color("gray")
                elif barrier["health"] <= 0:
                    barrier["obj"].hideturtle()
                    barriers.remove(barrier)
                break

    # Move enemies every second
    if time.time() - last_enemy_move > 1:
        move_enemies()
        last_enemy_move = time.time()

    # Check for win
    if len(enemies) == 0 and game_running:
        game_over_text.color("lime")
        game_over_text.write("YOU WON! Press 'R' to Restart", align="center", font=("Courier", 24, "bold"))
        game_running = False

    # Increase difficulty over time
    elapsed = time.time() - start_time
    if int(elapsed) % 10 == 0:
        if abs(enemy_speed) < 30:
            enemy_speed *= 1.05
        if bullet_cooldown > 0.1:
            bullet_cooldown -= 0.01

wn.mainloop()
