class Restaurant():

    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print("\nThis restaurant's name is " + self.restaurant_name.title() + "!")
        print("\nAnd it's cuisine type is " + self.cuisine_type.title() + "!")

    def open_restaurant(self):
        print("\nThis restaurant is open for business.")

my_restaurant = Restaurant('haidilao', 'chuan')
my_restaurant.describe_restaurant()
my_restaurant.open_restaurant()