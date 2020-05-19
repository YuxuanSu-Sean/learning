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


suyuxuan = User('yuxuan', 'su', 'good morning')
suyuxuan.describe_user()
suyuxuan.greet_user()
suyuxuan.describe_user()
suyuxuan.increment_login_attempts()
suyuxuan.describe_user()
suyuxuan.reset_login_attempts()