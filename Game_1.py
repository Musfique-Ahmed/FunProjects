print("Welcome to the guessing game!")

number = 36

guess = int(input("Enter your guess: "))

while guess != number:
    if guess > number:
        print("Too high, try again")
    else:
        print("Too low, try again")

    guess = int(input("Enter your guess: "))

print("You win!")
