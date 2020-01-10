def print_magician(magicians):
    for magician in magicians:
        print(magician)

def make_great(magicians, great_magicians):
    while magicians:
        current_name = "the great " + magicians.pop()
        great_magicians.append(current_name)
    # print_magician()
    print(great_magicians)

magicians = ['david', 'jim', 'tom']
# print_magician(magicians)
# print(magicians)

make_great(magicians[:], [])
print(magicians)