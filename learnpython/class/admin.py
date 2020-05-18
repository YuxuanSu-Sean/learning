class User():

    def __init__(self, first_name, last_name, user_info):
        self.first_name = first_name
        self.last_name = last_name
        self.user_info = user_info
        self.login_attempts = 0

    def describe_user(self):
        print(self.user_info.title())
        print(self.login_attempts)

    def greet_user(self):
        print("\nHello " + self.first_name.title() + " " + self.last_name.title() + "! Welcome to here!")

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0
        print(self.login_attempts)

class Privileges():

    def __init__(self):
        self.privileges = ["can add post", "can delete post", "can ban user"]

    def show_privileges(self, num):
        n = num
        print(self.privileges[n])

class Admin(User):

    def __init__(self, first_name, last_name, user_info):
        super().__init__(first_name, last_name, user_info)
        self.privileges = Privileges()

        # self.privileges = ["can add post", "can delete post", "can ban user"]

    # def show_privileges(self, num):
    #     n = num
    #     print(self.privileges[n])


#模拟实物类，将属性单独列出维护，实物类单独引用属性，并可以调用其方法



a = Admin("yuxuan", "su", "hello")
a.privileges.show_privileges(2)















