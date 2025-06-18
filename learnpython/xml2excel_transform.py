import xml.etree.ElementTree as ET
import pandas as pd

# 解析 XML 文件
tree = ET.parse('/Users/suyuxuan/Downloads/ems_8.1.2.0.xml')
root = tree.getroot()

# 存储数据的列表
data = []

# 遍历菜单
for menu in root.findall('.//menu'):
    menu_name = menu.get('name')
    route = menu.get('route')
    # 遍历权限
    for permission in menu.findall('.//permission'):
        permission_name = permission.get('name')
        front = permission.get('front')
        depend = permission.get('depend')
        # 遍历资源
        for resource in permission.findall('.//resource'):
            service = resource.get('service')
            method = resource.get('method')
            url = resource.get('url')
            # 将数据添加到列表中
            data.append([menu_name, route, permission_name, front, depend, service, method, url])

# 创建 DataFrame
df = pd.DataFrame(data, columns=['菜单名称', '路由', '权限名称', '前端标识', '依赖权限', '服务名称', '请求方法', 'URL'])

# 保存为 Excel 文件
df.to_excel('/Users/suyuxuan/Downloads/ems_8.1.2.0.xlsx', index=False)

print('XML 文件已成功转换为 Excel 文件。')