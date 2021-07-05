filename = 'pi_digits.txt'

with open(filename) as file_object:
    lines = file_object.readlines()

print(lines)

pi_string = ''
# 创建了一个变量——pi_string，用于存储圆周率的值
for line in lines:
    pi_string += line.strip()

print(pi_string)
print(len(pi_string))