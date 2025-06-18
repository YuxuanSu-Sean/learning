#编写一个循环，提示用户输入一系列的比萨配料，并在用户输入'quit'的时候结束循环。每当用户输入一种配料后，都打印一条消息，说我们会在比萨中添加这种配料。

prompt = "Please Enter a pizza topping!"
prompt += "\n"

while True:
    message = input(prompt)
    if message == 'quit':
        break
    else:
        print(message)