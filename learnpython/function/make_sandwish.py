def make_sandwish(name, *ingredients):
    print("\nMake a " + str(name) + " sandwish with the following ingredients:")
    for ingredient in ingredients:
        print("- " + ingredient)

make_sandwish('tuna', 'tuna', 'lettcue')