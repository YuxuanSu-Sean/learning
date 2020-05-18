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

# my_new_car = Car('audi', 'a4', '2020')
# print(my_new_car.get_descriptive_name())
# my_new_car.odometer = 23
# my_new_car.read_odometer()
# my_new_car.update_odometer(22)
# my_new_car.increase_odometer(2)
# my_new_car.read_odometer()

class Battery():
    def __init__(self, battery_size=70):
        self.battery_size = battery_size

    def describe_battery(self):
        print("This car has a " + str(self.battery_size) + "-KWh battery.")

    def get_range(self):
        if self.battery_size == 70:
            range = 240
        elif self.battery_size == 85:
            range = 270

        message = "This car can go approximately " + str(range)
        message += " miles on a full charge."
        print(message)


    def upgrade_battery(self):
        if self.battery_size != 85:
            self.battery_size = 85



class ElectricCar(Car):



    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        # self.battery_size = 70
        self.battery = Battery()

    # def descriptive_battery(self):
    #     print("This car has a " + str(self.battery_size) + '-KWh battery.')

# my_tesla = ElectricCar('teska', 'model s', 2016)
# print(my_tesla.get_descriptive_name())
# my_tesla.battery.describe_battery()
# my_tesla.battery.get_range()

my_tesla = ElectricCar('teska', 'model s', 2016)
my_tesla.battery.upgrade_battery()
my_tesla.battery.get_range()