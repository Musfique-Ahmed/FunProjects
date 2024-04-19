print("Musfique Ahmed")
print('0----')
print(' ||||')

price = 30
print(price)
name = 'Mosh'
is_published = True


# Check in a patient named John Smith. He is 20 years old and a new patient.

print("Patient INFO:")
patient_name = "John Smith"
patient_age = 20
new_patient = True
print("Name =", patient_name)
print("Age =", patient_age)
print('New patient =', new_patient)



# Ask some qus and print a msg

name = input('What is your name? ')
colour = input('What is your favourite colour? ')
print('Hi ' + name)
print(name, 'likes', colour , "colour.")
print(name + ' likes ' + colour + ' colour.')


# Make an age calculator

birth_year = input("Birth year: ")
age = 2023 - int(birth_year)
print("Age: " + str(age))


# Convert waight (lb) to (kg)

print('Waigth Convertion')
waight_pound = input('Waight in Pound(lb): ')
waigth_kg = float(waight_pound) / 2.20462262
print('Waight in KG (kg): ', waigth_kg)


# Make a multi-line string

email = '''
Hi Jhon,

This is our first mail to you.

Thankyou, 
Support team.
'''
print(email)


# Square brackets Syntax

course = 'Python for everybody.'
#         012345       ...,-2,-1
print(course[0])
print(course[-1])
print(course[-2])
print(course[2:4])      #2:4 nile 2,3 print hobe. (:)er porer syntex print hoye na.
print(course[3:])       #3 shoho 3 er age porjonto ja ase shgula bad diye baki gula print korbe.
print(course[:4])       #4 er por theke shob bad.
                        #(:)er porer take gunaye dhore na.


#Copy paste kora

another = course[:]
print(another)      #([:])eta use kore copy kora jaye


#Counting down payment of a 1M$ house:
house_price = 1000000
good_credit = False
if good_credit:
    down_payment = float(house_price) * .1
else:
    down_payment = float(house_price) * .2
print(f"Down payment: ${down_payment}")
