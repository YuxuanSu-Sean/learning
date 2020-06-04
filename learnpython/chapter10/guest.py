file_name = 'guest.txt'

guest_name = input('Please enter your name...\n')

with open(file_name, 'a') as file_object:
    file_object.write(guest_name + '\n')