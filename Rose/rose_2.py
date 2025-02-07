import turtle
import math

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Beautiful Rose")

# Create a turtle
rose_turtle = turtle.Turtle()
rose_turtle.speed(0)
rose_turtle.color("red")
rose_turtle.pensize(2)

# Function to draw a rose using parametric equations
def draw_rose(turtle, a, k, step=0.01):
    turtle.penup()
    for theta in range(0, 360 * 5, 1):  # Loop through angles (5 full rotations)
        theta_rad = math.radians(theta)  # Convert degrees to radians
        r = a * math.cos(k * theta_rad)  # Calculate radius
        x = r * math.cos(theta_rad)      # Convert polar to Cartesian coordinates
        y = r * math.sin(theta_rad)
        turtle.goto(x, y)                # Move turtle to the calculated position
        turtle.pendown()

# Draw the rose
draw_rose(rose_turtle, a=100, k=5)  # a = size, k = number of petals

# Add a stem
rose_turtle.penup()
rose_turtle.goto(0, -100)
rose_turtle.pendown()
rose_turtle.color("green")
rose_turtle.pensize(5)
rose_turtle.setheading(270)  # Point the turtle downward
rose_turtle.forward(200)     # Draw the stem

# Add leaves
def draw_leaf(turtle, size):
    turtle.begin_fill()
    turtle.circle(size, 70)
    turtle.left(110)
    turtle.circle(size, 70)
    turtle.end_fill()

rose_turtle.penup()
rose_turtle.goto(20, -200)
rose_turtle.pendown()
rose_turtle.color("darkgreen")
draw_leaf(rose_turtle, 30)  # Draw the first leaf

rose_turtle.penup()
rose_turtle.goto(-20, -200)
rose_turtle.pendown()
draw_leaf(rose_turtle, 30)  # Draw the second leaf

# Hide the turtle and display the result
rose_turtle.hideturtle()
turtle.done()