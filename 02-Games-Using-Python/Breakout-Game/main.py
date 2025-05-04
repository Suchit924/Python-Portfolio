import turtle
import random

# Screen Setup
wn = turtle.Screen()
wn.title("Breakout Clone")
wn.bgcolor("black")
wn.setup(width=1000, height=800)
wn.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -350)

# Ball
ball = turtle.Turtle()
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, -330)
ball_speed = 0.25
ball.dx = ball_speed
ball.dy = ball_speed

# Bricks
bricks = []
brick_colors = ["red", "green", "blue", "yellow", "purple", "orange"]
brick_width = 80
brick_height = 30

# Score
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 360)
score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

# Game over and win display
text_display = turtle.Turtle()
text_display.speed(0)
text_display.color("white")
text_display.penup()
text_display.hideturtle()

# Create bricks in heart shape
def create_heart_shape():
    global bricks
    for brick in bricks:
        brick.hideturtle()
    bricks.clear()

    heart_coordinates = [
        (-180, 100), (-120, 100), (0, 100), (120, 100), (180, 100),
        (-150, 60), (-90, 60), (0, 60), (90, 60), (150, 60),
        (-120, 30), (-60, 30), (0, 30), (60, 30), (120, 30),
        (-90, 0), (0, 0), (90, 0)
    ]

    for x, y in heart_coordinates:
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(random.choice(brick_colors))
        brick.penup()
        brick.goto(x, y)
        bricks.append(brick)

create_heart_shape()

# Paddle movement
def move_left():
    x = paddle.xcor()
    if x > -450:
        paddle.setx(x - 20)

def move_right():
    x = paddle.xcor()
    if x < 450:
        paddle.setx(x + 20)

# Reset game
def reset_game():
    global score, ball_speed
    score = 0
    ball_speed = 0.25
    ball.goto(0, -330)
    ball.dx = ball_speed
    ball.dy = ball_speed
    score_display.clear()
    score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
    text_display.clear()
    create_heart_shape()

# Keyboard bindings
wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(reset_game, "r")

# Remove brick
def remove_brick(brick):
    brick.hideturtle()
    bricks.remove(brick)

# Game Loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border collisions
    if ball.xcor() > 490:
        ball.setx(490)
        ball.dx *= -1
    if ball.xcor() < -490:
        ball.setx(-490)
        ball.dx *= -1
    if ball.ycor() > 390:
        ball.sety(390)
        ball.dy *= -1
    if ball.ycor() < -390:
        # Game Over
        text_display.goto(0, 0)
        text_display.write("GAME OVER! Press 'r' to restart", align="center", font=("Courier", 24, "normal"))
        ball.dx = 0
        ball.dy = 0
        continue

    # Paddle collision
    if (paddle.ycor() + 10 < ball.ycor() < paddle.ycor() + 20) and (paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60):
        ball.sety(paddle.ycor() + 20)
        ball.dy *= -1

    # Brick collision
    for brick in bricks[:]:  # iterate over a copy
        if (brick.xcor() - 40 < ball.xcor() < brick.xcor() + 40) and (brick.ycor() - 15 < ball.ycor() < brick.ycor() + 15):
            ball.dy *= -1
            remove_brick(brick)
            score += 10
            score_display.clear()
            score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
            break

    # Win check
    if not bricks:
        ball.goto(0, 0)
        ball.dx = 0
        ball.dy = 0
        text_display.goto(0, 0)
        text_display.write("YOU WIN! Press 'r' to restart", align="center", font=("Courier", 24, "normal"))

    turtle.delay(5)
