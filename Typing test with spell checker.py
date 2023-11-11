line = 'a quick brown fox jumps over the lazy dog'
#check = 'a,quick,brown,fox,jumps,over,the,lazy,dog'
check = list(line.split(" "))
user_input = input(f"Write: ['a quick brown fox jumps over the lazy dog'] to test your typing skills.\n => ")
#user_input = 'a quick brown fox jumps over the lazy dog'
while user_input == line:
    user_input = input(f'You are doing great. Try to do it faster!!!\n => ')
else:
    user = list(user_input.split(" "))
    i = 0
    while i < len(user):
        if user[i] != check[i]:
            wrong = user[i]
            right = check[i]
            break
        i += 1
    print(f"Your typing is wrong! Try again... \nThe word that you typed wrong was '{wrong}', while it should be '{right}'.")
