discounts_1 = {
    'pushti oil': 77, 
    'rupchada oil': 53, 
    'fresh milk powder': 95, 
    'marks milk poeder': 60, 
    'dairy milk': 30, 
    'muri': 5, 
    'chanacur': 20, 
    'clegs corn flex': 200, 
    'fresh salt': 7, 
    'dabur honey': 80, 
    'chinigura chal': 17,
    'coffee': 100, 
    'cha': 50, 
    'surf excel': 41, 
    'dove soap': 31, 
    'tooth paste': 30, 
    'dish wash liquid': 26, 
    'diapper': 390, 
    'tresemme shampo': 150, 
    'vaseline': 30, 
    'farm powder milk': 70, 
    'tomato sauce': 99, 
    'nutrilife jiuce': 30, 
    'oats': 50, 
    'shopno honey': 100, 
    'pringles chips': 70, 
    'aci pure toast': 10, 
    'shorishar tel': 70, 
    'rice brown oil': 100, 
    'holud moricher gura': 20, 
    'chinigura chal': 140, 
    'nivea body lotion': 400, 
    'nivea soft cream': 75,
    'oliv oil': 45, 
    'petroleum jelly': 20,
    'baby lotion': 200, 
    'head and shoulders shampo': 120, 
    'pantene shampo': 120, 
    'ponds cold cream': 20, 
    'meril baby lotion': 30, 
    'aci aerosol': 61, 
    'hit aerosol': 91, 
    'lofeboy handwash': 20, 
    'hair oil': 50, 
    }

total = 0
items = []
prices = []
a = map(int, input("How many items have you purchased? => "))
print(a)
b = 0
while b < (a+1):
#for i in range(a):
    item = input("Enter the item name: ")
    items.append(item.lower())
    price = int(input("Price of the item: "))
    prices.append(price)
    b += 1
price = 0

print(f"Here is your purchased items with discount list: ")
for i in range(len(items)):
    for it, disc in discounts_1:
        if it == item[i]:
            print(f"Podect: {it} \n     Discount: {disc}")
            price = prices[i]
            price -= disc
            total += price
        price = 0

 