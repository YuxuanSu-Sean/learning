# 编写一个函数，接受一座城市的名字以及该城市所属的国家。这个函数应该打印一个简单的句子，给用于存储国家的形参指定默认值。
# 为三座不同的城市调用这个函数，且其中至少有一座城市不属于默认国家。


def describe_city(city_name, country_name = 'China'):
    print("\nI lived in " + city_name + " and it belong to " + country_name + " !")

describe_city('nanjing')
describe_city('newyork', 'USA')
