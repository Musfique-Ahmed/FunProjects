def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")

choice = int(input("Enter choice(1/2/3/4): "))


if choice>= 1 and choice<=4:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == '1':
        print(f"Answer = {add(num1,num2)}")

    elif choice == '2':
        print(f"Answer = {num1 - num2}")

    elif choice == '3':
        print(f"Answer = {num1 * num2}")

    elif choice == '4':
        print(f"Answer = {num1 / num2}")
else:
    print("Invalid Input")
