print("Welcome to the Adventure Game!")

def start_game():
    name = input("Enter your name: ")
    print("Hello, " + name + "! You are on a quest to retrieve the lost treasure. You are standing at the entrance of a dark cave.")
    choice = input("Do you want to go inside the cave? (yes/no) ")
    if choice == "yes":
        print("You walk inside the cave and come across a fork in the road.")
        fork_in_road()
    else:
        print("You decide to turn back. Better luck next time!")

def fork_in_road():
    choice = input("Do you want to go left or right? (left/right) ")
    if choice == "left":
        print("You find yourself in a room filled with treasure! Congratulations, you have retrieved the lost treasure.")
    else:
        print("You fall into a pit filled with snakes. Game over.")

start_game()
