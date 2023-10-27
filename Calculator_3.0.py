import math

def calculate():
    """The main function that implements the calculator"""
    while True:
        try:
            expression = input("Enter your expression (or press q to quit): ")
            if expression == "q":
                break
            result = eval(expression)
            print("Result:", result)
        except:
            print("Invalid expression.")

if __name__ == "__main__":
    calculate()
