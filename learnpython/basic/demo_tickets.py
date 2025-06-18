#有家电影院根据观众的年龄收取不同的票价：不到3岁的观众免费，3-12岁的观众10美元，超过12岁的观众15美元。请编写一个循环，在其中询问用户的年龄，并指出其票价。

prompt = "\nPlease enter your age: "

while True:
    message = input(prompt)
    if message == 'quit':
        break
    age = int(message)

    if age < 3:
        print("Your age is " + str(age) + ", and we decide to reward you a ticket for free!")
    elif age >= 3 and age <= 12:
        print("Your age is " + str(age) + ", and the price of ticket is $10!")
    elif age > 12:
        print("Your age is " + str(age) + ", and the price of ticket is $15!")
    else:
        continue

