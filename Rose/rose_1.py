import turtle
import math

def draw_petal(t, radius, angle):
    """Draws a petal using circular arcs."""
    for _ in range(2):  # Two arcs forming a petal
        t.circle(radius, angle)
        t.left(180 - angle)

def draw_flower():
    """Draws a flower with multiple petals."""
    turtle.speed(0)
    turtle.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)
    t.color("red")
    t.width(2)

    t.penup()
    t.goto(0, -100)  # Move to start position
    t.pendown()

    for _ in range(8):  # 8 petals
        draw_petal(t, 100, 60)
        t.left(45)  # Rotate to next petal

    t.hideturtle()

def draw_stem():
    """Draws the stem of the flower."""
    stem = turtle.Turtle()
    stem.color("green")
    stem.width(5)
    stem.speed(0)

    stem.penup()
    stem.goto(0, -100)
    stem.pendown()
    stem.setheading(-90)  # Face downward
    stem.forward(200)  # Stem length

    stem.hideturtle()

def draw_leaf(x, y, angle):
    """Draws a leaf at a given position and angle."""
    leaf = turtle.Turtle()
    leaf.color("green")
    leaf.speed(0)
    
    leaf.penup()
    leaf.goto(x, y)
    leaf.setheading(angle)
    leaf.pendown()

    for _ in range(2):
        leaf.circle(30, 90)
        leaf.left(90)
        leaf.circle(30, 90)
        leaf.left(90)

    leaf.hideturtle()

def draw_rose():
    """Draws the complete rose with petals, stem, and leaves."""
    draw_flower()
    draw_stem()
    draw_leaf(-30, -150, -45)  # Left leaf
    draw_leaf(30, -180, 45)    # Right leaf

    turtle.done()

draw_rose()
