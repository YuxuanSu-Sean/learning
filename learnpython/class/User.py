class User():

    def __init__(self, first_name, last_name, user_info):
        self.first_name = first_name
        self.last_name = last_name
        self.user_info = user_info


    def describe_user(self):
        print(self.user_info.title())

    def greet_user(self):
        print("\nHello " + self.first_name.title() + " " + self.last_name.title() + "! Welcome to here!")


suyuxuan = User('yuxuan', 'su', 'good morning')
suyuxuan.describe_user()
suyuxuan.greet_user()