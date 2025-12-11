import pymysql
import pandas as pd
import math

# ======================== 核心配置区（可根据需求修改） ========================
# 1. 数据源配置（二选一：选MySQL则填MySQL信息，选Excel则填Excel信息）
DATA_SOURCE_TYPE = "Excel"  # 可选："MySQL" / "Excel"
# MySQL配置（仅当DATA_SOURCE_TYPE="MySQL"时生效）
MYSQL_CONFIG = {
    "host": "localhost",        # 数据库地址
    "port": 3306,               # 端口
    "user": "root",             # 用户名
    "password": "123456",       # 密码
    "db": "your_db_name",       # 数据库名
    "table": "your_table",      # 表名
    "score_column": "月实际归集平均时间",    # 分数列名
    "filter_column": "委办名称",    # 筛选列名（比如部门列：dept）
    "filter_value": "区城运中心"    # 筛选值（比如只选销售部："销售部"）
}
# Excel配置（仅当DATA_SOURCE_TYPE="Excel"时生效）
EXCEL_CONFIG = {
    "file_path": "/Users/suyuxuan/Downloads/数据质检结果最终汇总表.xlsx",  # Excel文件路径
    "sheet_name": "202509",               # 工作表名
    "score_column": "月实际归集平均时间",              # 分数列名
    "filter_column": "委办名称",              # 筛选列名（比如部门列：dept）
    "filter_value": "区城运中心"              # 筛选值（比如只选销售部："销售部"）
}

# 2. 公式参数配置（可自定义）
OFFSET = 0.5          # 偏移量（可选：0.25 / 0.5 或其他值）
WEIGHT = 10           # 权重（可选：10 / 15 或其他值）
LOG_BASE = 10         # 对数底数（10=常用对数，math.e=自然对数）

# ======================== 核心函数定义 ========================
def read_data_from_mysql(config):
    """从MySQL读取指定筛选条件的分数数组"""
    try:
        # 连接MySQL
        conn = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            db=config["db"],
            charset="utf8"
        )
        cursor = conn.cursor()
        # 构造带筛选条件的SQL（参数化查询避免SQL注入）
        sql = f"""
            SELECT {config['score_column']} 
            FROM {config['table']} 
            WHERE {config['score_column']} IS NOT NULL 
            AND {config['filter_column']} = %s
        """
        # 执行查询（传入筛选值）
        cursor.execute(sql, (config["filter_value"],))
        # 提取数据并转换为浮点数数组
        data = [float(row[0]) for row in cursor.fetchall()]
        conn.close()
        print(f"✅ 从MySQL读取【{config['filter_column']}={config['filter_value']}】的分数数组：{data}")
        return data
    except Exception as e:
        print(f"❌ MySQL读取失败：{str(e)}")
        return []

def read_data_from_excel(config):
    """从Excel读取指定筛选条件的分数数组"""
    try:
        # 读取Excel
        df = pd.read_excel(config["file_path"], sheet_name=config["sheet_name"])
        # 筛选指定列的值（先处理空值，避免筛选失败）
        df_filtered = df[
            (df[config["filter_column"]] == config["filter_value"]) & 
            (df[config["score_column"]].notna())
        ]
        # 提取分数列并转换为浮点数
        data = df_filtered[config["score_column"]].astype(float).tolist()
        print(f"✅ 从Excel读取【{config['filter_column']}={config['filter_value']}】的分数数组：{data}")
        return data
    except Exception as e:
        print(f"❌ Excel读取失败：{str(e)}")
        return []

def preprocess_data(raw_data):
    """预处理数据：去除原始数组的最大值和最小值，返回剩余数组+剩余值的min/max"""
    if len(raw_data) < 3:
        print(f"⚠️ 筛选后数组长度{len(raw_data)}，不足3个值，无法去除极值！")
        return [], None, None
    
    # 去除最大值和最小值
    raw_data_sorted = sorted(raw_data)
    processed_data = raw_data_sorted[1:-1]  # 去掉第一个（最小）和最后一个（最大）
    # 计算剩余值的极值
    processed_min = min(processed_data)
    processed_max = max(processed_data)
    
    print(f"📊 筛选后原始数组：{raw_data}")
    print(f"📊 去除极值（max={max(raw_data)}, min={min(raw_data)}）后数组：{processed_data}")
    print(f"📊 剩余值的极值：min={processed_min}, max={processed_max}")
    return processed_data, processed_min, processed_max

def calculate_final_score(x, processed_min, processed_max, offset, weight, log_base):
    """根据公式计算单个分数的最终得分"""
    try:
        # 步骤1：平移（避免log(0)）
        x_shift = x + 1
        min_shift = processed_min + 1
        max_shift = processed_max + 1
        
        # 步骤2：对数变换
        log_x = math.log(x_shift, log_base)
        log_min = math.log(min_shift, log_base)
        log_max = math.log(max_shift, log_base)
        
        # 步骤3：min-max归一化（避免除以0）
        if log_max - log_min == 0:
            norm_value = 0.5  # 极值相等时默认0.5
        else:
            norm_value = (log_x - log_min) / (log_max - log_min)
        
        # 步骤4：缩放+偏移 + 权重（公式：(归一化值×偏移量 + 偏移量) × 权重）
        final_score = (norm_value * offset + offset) * weight
        return round(final_score, 4)  # 保留4位小数
    except Exception as e:
        print(f"❌ 计算分数{x}失败：{str(e)}")
        return None

# ======================== 主执行流程 ========================
if __name__ == "__main__":
    # 1. 读取数据源（带筛选条件）
    if DATA_SOURCE_TYPE == "MySQL":
        raw_data = read_data_from_mysql(MYSQL_CONFIG)
    elif DATA_SOURCE_TYPE == "Excel":
        raw_data = read_data_from_excel(EXCEL_CONFIG)
    else:
        print("❌ 数据源类型错误！仅支持MySQL/Excel")
        raw_data = []
    
    if not raw_data:
        print(f"❌ 【{MYSQL_CONFIG.get('filter_value', EXCEL_CONFIG.get('filter_value'))}】无有效分数数据，程序退出")
        exit()
    
    # 2. 预处理数据（去极值）
    processed_data, p_min, p_max = preprocess_data(raw_data)
    if not processed_data or p_min is None or p_max is None:
        print("❌ 数据预处理失败，程序退出")
        exit()
    
    # 3. 计算每个分数的最终得分
    final_result = []
    for score in processed_data:
        final_score = calculate_final_score(score, p_min, p_max, OFFSET, WEIGHT, LOG_BASE)
        final_result.append({
            "原始分数": score,
            "最终得分": final_score
        })
    
    # 4. 输出结果
    print("\n==================== 最终计算结果 ====================")
    for item in final_result:
        print(f"原始分数：{item['原始分数']} → 最终得分：{item['最终得分']}")
    
    # 可选：输出汇总信息
    valid_final_scores = [item["最终得分"] for item in final_result if item["最终得分"] is not None]
    if valid_final_scores:
        avg_final_score = sum(valid_final_scores) / len(valid_final_scores)
        print(f"\n📈 汇总：【{MYSQL_CONFIG.get('filter_value', EXCEL_CONFIG.get('filter_value'))}】去极值后共{len(processed_data)}个分数，最终得分平均值：{round(avg_final_score, 4)}")
    else:
        print("\n📈 汇总：无有效最终得分")