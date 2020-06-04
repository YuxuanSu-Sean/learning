with open('pi_digits.txt') as file_object:
    # contents = file_object.read()
    # print(contents.rsplit())
    lines = file_object.readlines()
    print(lines)
    for line in lines:
        print(line.rstrip())