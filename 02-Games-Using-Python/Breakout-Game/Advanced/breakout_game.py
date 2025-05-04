import turtle
import random
import time

# --- Screen Setup ---
wn = turtle.Screen()
wn.title("Breakout Arcade - Enhanced")
wn.bgcolor("black")
wn.setup(width=1000, height=800)
wn.tracer(0)

# --- Global Flags ---
paused = False
lives = 3
score = 0
level = 1

# --- Paddle ---
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -350)

# --- Ball ---
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, -330)
ball_speed = 0.25
ball.dx = ball_speed
ball.dy = ball_speed

# --- Bricks ---
bricks = []
brick_colors = ["red", "green", "blue", "yellow", "purple", "orange"]

# --- Power-ups ---
power_ups = []
powerup_types = ["expand", "shrink", "slow", "fast"]

# --- HUD ---
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 360)

text_display = turtle.Turtle()
text_display.color("white")
text_display.penup()
text_display.hideturtle()

# --- Start Screen ---
def show_start_screen():
    text_display.clear()
    text_display.goto(0, 0)
    text_display.write("BREAKOUT ARCADE\nPress SPACE to start", align="center", font=("Courier", 24, "normal"))
    wn.listen()
    wn.onkey(start_game, "space")
    wn.mainloop()

def start_game():
    text_display.clear()
    create_bricks(level_patterns[level])
    update_score()
    game_loop()

# --- Levels ---
def level_1():
    return [(x, y) for x in range(-320, 340, 80) for y in range(100, 220, 40)]

def level_2():
    return [(i * 80, 180 - j * 40) for i in range(-4, 5) for j in range(abs(i), 5)]

level_patterns = {1: level_1, 2: level_2}

def create_bricks(pattern_func):
    global bricks
    for brick in bricks:
        brick.hideturtle()
    bricks.clear()
    for x, y in pattern_func():
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(random.choice(brick_colors))
        brick.penup()
        brick.goto(x, y)
        bricks.append(brick)

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}  Level: {level}  Lives: {lives}", align="center", font=("Courier", 24, "normal"))

# --- Paddle Controls ---
def move_left():
    if paddle.xcor() > -450:
        paddle.setx(paddle.xcor() - 20)

def move_right():
    if paddle.xcor() < 450:
        paddle.setx(paddle.xcor() + 20)

def toggle_pause():
    global paused
    paused = not paused

# --- Power-up ---
def spawn_powerup(x, y):
    p = turtle.Turtle()
    p.shape("triangle")
    p.color("cyan")
    p.penup()
    p.goto(x, y)
    p.type = random.choice(powerup_types)
    power_ups.append(p)

def check_powerups():
    global ball_speed
    for p in power_ups[:]:
        p.sety(p.ycor() - 5)
        if p.distance(paddle) < 40:
            p.hideturtle()
            power_ups.remove(p)
            if p.type == "expand":
                paddle.shapesize(stretch_len=8)
            elif p.type == "shrink":
                paddle.shapesize(stretch_len=3)
            elif p.type == "slow":
                ball_speed = max(0.15, ball_speed - 0.05)
            elif p.type == "fast":
                ball_speed += 0.05
            ball.dx = ball_speed * (1 if ball.dx > 0 else -1)
            ball.dy = ball_speed * (1 if ball.dy > 0 else -1)

# --- Level Transition ---
def next_level():
    global level, ball_speed
    level += 1
    if level in level_patterns:
        create_bricks(level_patterns[level])
        ball_speed += 0.05
        ball.dx = ball_speed
        ball.dy = ball_speed
        ball.goto(0, -330)
    else:
        text_display.goto(0, 0)
        text_display.write("YOU BEAT THE GAME! Press 'r' to restart", align="center", font=("Courier", 24, "normal"))
        ball.dx = 0
        ball.dy = 0

def reset_game():
    global score, level, ball_speed, lives
    score = 0
    level = 1
    ball_speed = 0.25
    lives = 3
    ball.goto(0, -330)
    ball.dx = ball_speed
    ball.dy = ball_speed
    text_display.clear()
    create_bricks(level_patterns[level])
    update_score()

wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(reset_game, "r")
wn.onkey(toggle_pause, "p")

def remove_brick(brick):
    if random.random() < 0.25:
        spawn_powerup(brick.xcor(), brick.ycor())
    brick.hideturtle()
    bricks.remove(brick)

# --- Game Loop ---
def game_loop():
    global lives, score
    while True:
        wn.update()
        if paused:
            time.sleep(0.1)
            continue

        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        if ball.xcor() > 490 or ball.xcor() < -490:
            ball.dx *= -1
        if ball.ycor() > 390:
            ball.dy *= -1
        if ball.ycor() < -390:
            lives -= 1
            update_score()
            if lives > 0:
                ball.goto(0, -330)
                ball.dx = ball_speed
                ball.dy = ball_speed
            else:
                text_display.goto(0, 0)
                text_display.write("GAME OVER! Press 'r' to restart", align="center", font=("Courier", 24, "normal"))
                ball.dx = 0
                ball.dy = 0
                break

        if (paddle.ycor() + 10 < ball.ycor() < paddle.ycor() + 20) and (paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60):
            ball.sety(paddle.ycor() + 20)
            ball.dy *= -1

        for brick in bricks[:]:
            if (brick.xcor() - 40 < ball.xcor() < brick.xcor() + 40) and (brick.ycor() - 15 < ball.ycor() < brick.ycor() + 15):
                ball.dy *= -1
                remove_brick(brick)
                score += 10
                update_score()
                break

        if not bricks:
            next_level()

        check_powerups()
        turtle.delay(5)

# --- Start the Game ---
show_start_screen()