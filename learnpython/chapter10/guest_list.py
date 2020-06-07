# 编写一个 while 循环，提示用户输入其名字。用户输入其名字后，
# 在屏幕上打印一句问候语，并将一条访问记录添加到文件 guest_book.txt 中。确保这个
# 文件中的每条记录都独占一行。

file_name = 'guest_list.txt'

active = True
while active:
    message = input("Please enter your name on the keyboard...\n")

    if message == '!quit':
        active = False
    else:
        with open(file_name, 'a') as file_ob:
            file_ob.write(message + '\n')
