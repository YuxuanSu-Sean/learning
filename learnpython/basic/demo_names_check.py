current_names = ['suyuxuan', 'lifengfeng', 'zhuxiaoqing', 'wangyingzhou', 'yangzhenyu']
new_names = ['liuhui', 'yanlihua', 'lifengfeng', 'zhangying', 'wangzhanghua', 'ZHUXIAOQING']

for name in new_names:
    if name.lower() in current_names:
        # 使用lower()，对大小写不做区分ß
        print("The name " + name + " has been occupied, you need to enter another name!")
    else:
        print("This name " + name + " is not used!")