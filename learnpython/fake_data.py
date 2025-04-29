from faker import Faker
import pandas as pd

# 创建 Faker 对象
fake = Faker('zh_CN')

# 定义字段列表
columns = ['法定代表人/经营者姓名(中文)', '统一社会信用码', '法人名称(中文)', '组织机构代码', '法定代表人证件号',
           '纳税人识别号', '经营者住所', '公积金账号', '法人注销原因(中文)', '法定代表人证件类型', '法定代表人联系电话',
           '经营者联系电话', '电子邮箱', '网址', '经营范围(中文)', '企业类型(中文)', '登记机关(中文)', '登记日期',
           '注册资本(万元)', '实缴资本(万元)', '成立日期']

# 创建空的 DataFrame
data = pd.DataFrame(columns=columns)

# 生成 20 条假数据
for _ in range(20):
    fake_data = {
        '法定代表人/经营者姓名(中文)': fake.name(),
        '统一社会信用码': fake.bothify(text='??????????????????', letters='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        '法人名称(中文)': fake.company(),
        '组织机构代码': fake.bothify(text='???????-?', letters='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        '法定代表人证件号': fake.ssn(),
        '纳税人识别号': fake.bothify(text='??????????????????', letters='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        '经营者住所': fake.address(),
        '公积金账号': fake.bothify(text='??????????????????', letters='0123456789'),
        '法人注销原因(中文)': fake.sentence(nb_words=3),
        '法定代表人证件类型': fake.random_element(elements=('身份证', '护照', '军官证')),
        '法定代表人联系电话': fake.phone_number(),
        '经营者联系电话': fake.phone_number(),
        '电子邮箱': fake.email(),
        '网址': fake.url(),
        '经营范围(中文)': fake.sentence(nb_words=10),
        '企业类型(中文)': fake.random_element(elements=('有限责任公司', '股份有限公司', '个人独资企业')),
        '登记机关(中文)': fake.company_suffix(),
        '登记日期': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
        '注册资本(万元)': fake.random_int(min=10, max=1000),
        '实缴资本(万元)': fake.random_int(min=10, max=1000),
        '成立日期': fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
    }
    data = pd.concat([data, pd.DataFrame([fake_data])], ignore_index=True)

# 将数据保存为 CSV 文件
csv_path = '/Users/suyuxuan/Downloads/法人信息项_假数据.csv'
data.to_csv(csv_path, index=False)