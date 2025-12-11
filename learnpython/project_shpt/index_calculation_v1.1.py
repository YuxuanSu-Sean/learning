import pymysql
import pandas as pd
import math
from typing import List, Tuple, Optional, Dict

# ======================== 核心配置区（可根据需求修改） ========================
# 1. 数据源配置（二选一：选MySQL则填MySQL信息，选Excel则填Excel信息）
DATA_SOURCE_TYPE = "Excel"  # 可选："MySQL" / "Excel"

# MySQL配置（仅当DATA_SOURCE_TYPE="MySQL"时生效）
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "db": "your_db_name",
    "table": "your_table",
    "score_column": "月实际归集平均时间",  # 待计算的数值列
    "filter_column": "委办名称",          # 筛选维度列
    "filter_value": "区城运中心"          # 筛选维度值
}

# Excel配置（仅当DATA_SOURCE_TYPE="Excel"时生效）
EXCEL_CONFIG = {
    "file_path": "/Users/suyuxuan/Downloads/数据质检结果最终汇总表.xlsx",
    "sheet_name": "202509",
    "score_column": "月实际归集平均时间",
    "filter_column": "委办名称",
    "filter_value": "区城运中心"
}

# 2. 公式参数配置（附业务含义注释）
OFFSET = 0.5          # 基础偏移量（使归一化值从0.5开始）
WEIGHT = 10           # 得分权重（放大最终结果，如0.5→5分）
LOG_BASE = 10         # 对数底数（10=常用对数，math.e=自然对数，需>1）
MIN_DATA_LENGTH = 3   # 去极值的最小数据量要求

# ======================== 工具函数（参数校验） ========================
def validate_params() -> bool:
    """校验核心参数合法性，避免运行时错误"""
    errors = []
    if LOG_BASE <= 1:
        errors.append(f"对数底数LOG_BASE={LOG_BASE}需大于1（避免对数无意义）")
    if OFFSET < 0:
        errors.append(f"偏移量OFFSET={OFFSET}不能为负数")
    if WEIGHT <= 0:
        errors.append(f"权重WEIGHT={WEIGHT}需大于0")
    if DATA_SOURCE_TYPE not in ["MySQL", "Excel"]:
        errors.append(f"数据源类型{DATA_SOURCE_TYPE}无效，仅支持MySQL/Excel")
    
    if errors:
        print("❌ 参数校验失败：")
        for err in errors:
            print(f"  - {err}")
        return False
    return True

# ======================== 核心函数（保持原有逻辑+增强提示） ========================
def read_data_from_mysql(config: Dict) -> List[float]:
    """从MySQL读取指定筛选条件的数值数组（参数化查询防注入）"""
    try:
        conn = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            db=config["db"],
            charset="utf8mb4"  # 升级为utf8mb4支持emoji等特殊字符
        )
        with conn.cursor() as cursor:
            sql = f"""
                SELECT {config['score_column']} 
                FROM {config['table']} 
                WHERE {config['score_column']} IS NOT NULL 
                AND {config['filter_column']} = %s
            """
            cursor.execute(sql, (config["filter_value"],))
            data = [float(row[0]) for row in cursor.fetchall() if row[0] is not None]
        
        conn.close()
        print(f"✅ MySQL读取成功：【{config['filter_column']}={config['filter_value']}】共{len(data)}条有效数据")
        return data
    except pymysql.MySQLError as e:
        print(f"❌ MySQL读取失败（数据库错误）：{e.args[0]} - {e.args[1]}")
        return []
    except Exception as e:
        print(f"❌ MySQL读取失败（其他错误）：{str(e)}")
        return []

def read_data_from_excel(config: Dict) -> List[float]:
    """从Excel读取指定筛选条件的数值数组（处理空值/类型异常）"""
    try:
        # 读取Excel（指定engine避免编码问题）
        df = pd.read_excel(
            config["file_path"], 
            sheet_name=config["sheet_name"],
            engine="openpyxl"  # 推荐引擎，支持.xlsx格式
        )
        
        # 校验列是否存在
        if config["filter_column"] not in df.columns:
            print(f"❌ Excel中无筛选列【{config['filter_column']}】")
            return []
        if config["score_column"] not in df.columns:
            print(f"❌ Excel中无分数列【{config['score_column']}】")
            return []
        
        # 筛选有效数据（排除空值+匹配筛选值）
        df_filtered = df[
            (df[config["filter_column"]] == config["filter_value"]) & 
            (df[config["score_column"]].notna())
        ]
        
        # 强制转换为浮点数（处理整数/字符串格式的数值）
        data = df_filtered[config["score_column"]].apply(lambda x: float(x) if str(x).replace('.','').isdigit() else None).dropna().tolist()
        print(f"✅ Excel读取成功：【{config['filter_column']}={config['filter_value']}】共{len(data)}条有效数据")
        return data
    except FileNotFoundError:
        print(f"❌ Excel文件不存在：{config['file_path']}")
        return []
    except Exception as e:
        print(f"❌ Excel读取失败：{str(e)}")
        return []

def preprocess_data(raw_data: List[float]) -> Tuple[List[float], Optional[float], Optional[float]]:
    """预处理数据：去除极值，返回处理后数组+其最小/最大值（增强容错）"""
    if len(raw_data) < MIN_DATA_LENGTH:
        print(f"⚠️ 有效数据量{len(raw_data)} < 最小要求{MIN_DATA_LENGTH}，无法去极值！")
        return raw_data, min(raw_data) if raw_data else None, max(raw_data) if raw_data else None
    
    # 去极值（排序后去掉首尾）
    sorted_data = sorted(raw_data)
    processed_data = sorted_data[1:-1]
    processed_min = min(processed_data) if processed_data else None
    processed_max = max(processed_data) if processed_data else None
    
    print(f"\n📊 数据预处理详情：")
    print(f"  - 原始数据：{raw_data}")
    print(f"  - 去除极值（最大值={sorted_data[-1]}, 最小值={sorted_data[0]}）")
    print(f"  - 处理后数据：{processed_data}")
    print(f"  - 处理后数据极值：min={processed_min}, max={processed_max}")
    return processed_data, processed_min, processed_max

def calculate_final_score(
    x: float, 
    processed_min: float, 
    processed_max: float, 
    offset: float = OFFSET, 
    weight: float = WEIGHT, 
    log_base: float = LOG_BASE
) -> Optional[float]:
    """计算单个数值的最终得分（分步打印便于调试）"""
    try:
        # 步骤1：平移（避免log(0)）
        x_shift = x + 1
        min_shift = processed_min + 1
        max_shift = processed_max + 1
        
        # 步骤2：对数变换
        log_x = math.log(x_shift, log_base)
        log_min = math.log(min_shift, log_base)
        log_max = math.log(max_shift, log_base)
        
        # 步骤3：Min-Max归一化（避免除以0）
        log_diff = log_max - log_min
        norm_value = 0.5 if log_diff == 0 else (log_x - log_min) / log_diff
        
        # 步骤4：缩放+偏移
        final_score = (norm_value * offset + offset) * weight
        
        # 调试用（可选开启）
        # print(f"  调试：x={x} → 平移={x_shift} → 对数={log_x:.4f} → 归一化={norm_value:.4f} → 最终得分={final_score:.4f}")
        
        return round(final_score, 4)
    except Exception as e:
        print(f"❌ 计算数值{x}的得分失败：{str(e)}")
        return None

# ======================== 主执行流程（结构化+容错） ========================
def main():
    """主执行函数（解耦逻辑，便于复用）"""
    # 1. 参数校验
    if not validate_params():
        return
    
    # 2. 读取数据
    if DATA_SOURCE_TYPE == "MySQL":
        raw_data = read_data_from_mysql(MYSQL_CONFIG)
    elif DATA_SOURCE_TYPE == "Excel":
        raw_data = read_data_from_excel(EXCEL_CONFIG)
    else:
        raw_data = []
    
    if not raw_data:
        print(f"❌ 无有效数据（筛选值：{MYSQL_CONFIG.get('filter_value', EXCEL_CONFIG.get('filter_value'))}），程序退出")
        return
    
    # 3. 预处理数据
    processed_data, p_min, p_max = preprocess_data(raw_data)
    if not processed_data or p_min is None or p_max is None:
        print("❌ 数据预处理后无有效数据，程序退出")
        return
    
    # 4. 计算最终得分
    final_result = []
    for score in processed_data:
        final_score = calculate_final_score(score, p_min, p_max)
        final_result.append({
            "原始分数": score,
            "最终得分": final_score
        })
    
    # 5. 输出结果（美化格式）
    print("\n==================== 最终计算结果 ====================")
    for idx, item in enumerate(final_result, 1):
        print(f"[{idx}] 原始分数：{item['原始分数']} → 最终得分：{item['最终得分']}")
    
    # 6. 汇总统计
    valid_scores = [item["最终得分"] for item in final_result if item["最终得分"] is not None]
    if valid_scores:
        avg_score = sum(valid_scores) / len(valid_scores)
        print(f"\n📈 汇总统计：")
        print(f"  - 有效得分数量：{len(valid_scores)}")
        print(f"  - 得分平均值：{round(avg_score, 4)}")
        print(f"  - 得分最大值：{round(max(valid_scores), 4)}")
        print(f"  - 得分最小值：{round(min(valid_scores), 4)}")
    else:
        print("\n📈 汇总统计：无有效得分")

if __name__ == "__main__":
    main()