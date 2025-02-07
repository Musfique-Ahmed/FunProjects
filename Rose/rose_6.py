# import turtle
# # rose_data is the py file that stores the data
# import rose_data
 
# def draw_line(pix_list):
#     '''According to pix_Pixel data drawing of list'''
#     turtle.penup()
#     turtle.goto(*pix_list[0])
#     turtle.pendown()
#     for pix in pix_list:
#         turtle.goto(*pix)
    
# def draw_pic(pic_data):
#     '''pic_data is a dictionary, each item stores each pixel data'''
#     for i in range(1,len(pic_data)+1):
#         pix_list = pic_data[i]
#     draw_line(pix_list)  
  
# def init():
#     turtle.title('rose')
#     turtle.pensize(2)
#     turtle.speed(0)
#     turtle.hideturtle()
#     turtle.color('red','red')
#     turtle.setup(width=800, height=500, startx=0, starty=0)

# if __name__ =='__main__':
#     init()
#     draw_pic(rose_data.data)
#     turtle.mainloop()


import turtle
# rose_data is the py file that stores the data
import rose_data
 
def draw_line(pix_list):
    '''According to pix_Pixel data drawing of list'''
    turtle.penup()
    turtle.goto(*pix_list[0])
    turtle.pendown()
    for pix in pix_list:
        turtle.goto(*pix)
    
def draw_pic(pic_data):
    '''pic_data is a dictionary, each item stores each pixel data'''
    for i in range(1, len(pic_data) + 1):
        pix_list = pic_data[i]
        draw_line(pix_list)  # Call draw_line for each pix_list
  
def init():
    turtle.title('rose')
    # turtle.speed(0)
    turtle.bgcolor("black")
    turtle.pensize(2)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.color('red', 'red')
    turtle.setup(width=800, height=500, startx=0, starty=0)

if __name__ == '__main__':
    init()
    draw_pic(rose_data.data)
    turtle.mainloop()



# import turtle
# # rose_data is the py file that stores the data
# import rose_data
 
# def draw_line(pix_list):
#     '''According to pix_Pixel data drawing of list'''
#     turtle.penup()
#     turtle.goto(*pix_list[0])
#     turtle.pendown()
#     turtle.begin_fill()  # Start filling
#     for pix in pix_list:
#         turtle.goto(*pix)
#     turtle.end_fill()  # End filling
    
# def draw_pic(pic_data):
#     '''pic_data is a dictionary, each item stores each pixel data'''
#     for i in range(1, len(pic_data) + 1):
#         pix_list = pic_data[i]
#         draw_line(pix_list)  # Call draw_line for each pix_list
  
# def init():
#     turtle.title('rose')
#     turtle.pensize(2)
#     turtle.speed(0)
#     turtle.hideturtle()
#     turtle.color('black', 'red')
#     turtle.setup(width=800, height=500, startx=0, starty=0)

# if __name__ == '__main__':
#     init()
#     draw_pic(rose_data.data)
#     turtle.mainloop()

# import turtle
# import turtle
# # rose_data is the py file that stores the data
# import rose_data

# def draw_line(pix_list, fill_color):
#     '''According to pix_Pixel data drawing of list'''
#     turtle.fillcolor(fill_color)
#     turtle.penup()
#     turtle.goto(*pix_list[0])
#     turtle.pendown()
#     turtle.begin_fill()  # Start filling
#     for pix in pix_list:
#         turtle.goto(*pix)
#     # Ensure the shape is closed by returning to the start
#     turtle.goto(*pix_list[0])
#     turtle.end_fill()  # End filling

# def draw_pic(pic_data, fill_color):
#     '''pic_data is a dictionary, each item stores each pixel data'''
#     for i in range(1, len(pic_data) + 1):
#         pix_list = pic_data[i]
#         draw_line(pix_list, fill_color)  # Call draw_line for each pix_list

# def draw_stem():
#     '''Draw the stem of the rose'''
#     turtle.penup()
#     turtle.goto(0, -200)
#     turtle.pendown()
#     turtle.color('green')
#     turtle.pensize(10)
#     turtle.setheading(90)
#     turtle.forward(200)

# def draw_leaves():
#     '''Draw the leaves of the rose'''
#     turtle.penup()
#     turtle.goto(0, -100)
#     turtle.pendown()
#     turtle.color('green')
#     turtle.pensize(2)
#     turtle.begin_fill()
#     turtle.circle(50, 90)
#     turtle.left(90)
#     turtle.circle(50, 90)
#     turtle.end_fill()
#     turtle.right(180)
#     turtle.penup()
#     turtle.goto(0, -150)
#     turtle.pendown()
#     turtle.begin_fill()
#     turtle.circle(50, 90)
#     turtle.left(90)
#     turtle.circle(50, 90)
#     turtle.end_fill()

# def init():
#     turtle.title('rose')
#     turtle.pensize(2)
#     turtle.speed(0)  # Set speed to maximum
#     turtle.hideturtle()
#     turtle.color('black', 'red')
#     turtle.setup(width=800, height=500, startx=0, starty=0)

# if __name__ == '__main__':
#     init()
#     draw_stem()
#     draw_leaves()
#     draw_pic(rose_data.data, 'red')
#     turtle.mainloop()