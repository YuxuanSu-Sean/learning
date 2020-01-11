def make_car(manufacturer, type, **car_info):
    car = {}
    car['manufacturer'] = manufacturer
    car['type'] = type
    for key, value in car_info.items():
        car[key] = value
    return car

car = make_car('subaru', 'outback', color='blue', tow_package=True, driver='suyuxuan')
print(car)