def build_person(first_name, last_name):
    person = {'first': first_name, 'last': last_name}
    return person

# musician = build_person('jimi', 'hendrix')
# print(musician)


while True:
    print("\nPlease tell me your name: ")
    f_name = input("First_name: ")
    if f_name == 'q':
        break
    l_name = input("Last_name: ")
    if l_name == 'q':
        break

    person = build_person(f_name, l_name)
    print(person)