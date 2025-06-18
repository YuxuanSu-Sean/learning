users = ['suyuxuan', 'lifengfeng', 'zhuxiaoqing', 'wangyingzhou', 'yangzhenyu', 'yanlihua', 'admin']
# users = []
user = 'suyuxuan'


if users:
    for user in users:
        if user == 'admin':
            print("Hello admin, would you like to see a status report?")
        else:
            print("Hello " + user +", thank you for login in again")

else:
    print("We need to find some users!")