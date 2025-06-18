person = {}

person['first_name'] = 'yuxuan'
person['last_name'] = 'su'
person['age'] = 31
person['city'] = 'nanjing'
print(person)

for key, value in person.items():
    print(key)
    print(value)

for key in person.keys():
    print("\n" + key)