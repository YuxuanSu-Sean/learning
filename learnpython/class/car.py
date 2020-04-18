class Car():

    def __init__(self, make, model, year):
        self.make  = make
        self.model = model
        self.year = year
        self.odometer = 0

    def get_descriptive_name(self):
        long_name = str(self.year) + ' ' + self.make + ' ' + self.model
        return long_name.title()

    def read_odometer(self):
        print("This car has " + str(self.odometer) + " miles on it.")

    def update_odometer(self, mileage):
        if mileage >= self.odometer:
            self.odometer = mileage
        else:
            print("you can't roll back an odometer!")

    def increase_odometer(self, miles):
        self.odometer += miles

my_new_car = Car('audi', 'a4', '2020')
print(my_new_car.get_descriptive_name())
my_new_car.odometer = 23
my_new_car.read_odometer()
my_new_car.update_odometer(22)
my_new_car.increase_odometer(2)
my_new_car.read_odometer()
