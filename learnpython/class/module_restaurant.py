class Restaurant():

    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0

    def describe_restaurant(self):
        print("\nThis restaurant's name is " + self.restaurant_name.title() + "!")
        print("\nAnd it's cuisine type is " + self.cuisine_type.title() + "!")

    def open_restaurant(self):
        print("\nThis restaurant is open for business.")

    def read_number_served(self):
        print(self.number_served)

    def update_number_served(self, number):
        if number >= self.number_served:
            self.number_served = number
        else:
            print("the number you've served is wrong!")

    def increase_number_served(self, clients):
        self.number_served += clients