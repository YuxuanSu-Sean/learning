banned_users = ['andrew', 'carolina', 'david']
print(len(banned_users))
user = 'marie'
banned_users.append(user)

if user not in banned_users:
    print(user.title() + ", you can post a response if you wish.")
else:
    print(banned_users[-1])