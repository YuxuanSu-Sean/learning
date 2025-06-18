#创建一个名为sandwich_orders的列表，在其中包含各种三明治的名字；再创建一个名为finish_sandwiches的空列表。
# 遍历列表sandwich_orders，对于其中的每种三明治，都打印一条消息，并将其移到列表finished_sandwiches。所有三明治都制作好，打印一条消息，将这些三明治都列出来。

#第二步，删除所有pastrami sandwich

sandwich_orders = ['tuna sandwich', 'pastrami sandwich', 'baconic sandwich', 'pastrami sandwich', 'cheese sandwich', 'pastrami sandwich']
finish_sandwiches = []

for sandwich_order in sandwich_orders:
    # print(sandwich_order.title())
    while 'pastrami sandwich' in sandwich_orders:
        sandwich_orders.remove('pastrami sandwich')
        print(sandwich_orders)
    finish_sandwiches.append(sandwich_order)

print(finish_sandwiches)