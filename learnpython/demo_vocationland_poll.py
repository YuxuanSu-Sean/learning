#调查用户梦想的度假胜地

responses = {}

polling_active = True

while polling_active:
    name = input("\nWhat's your name?")
    reponse = input("\nIf you could visit one place in the world, where would you go?")
    responses[name] = reponse

    repeat = input("\nContinue? (yes/ no)")
    if repeat == 'no':
        polling_active = False

print(responses)
print("\n---Poll Results ---")
for name, reponse in responses.items():
    print(name + " would like to visit " + reponse + ".")