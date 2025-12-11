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
    "filter_value": "区城运中心",         # 筛选维度值
    "target_column": "最终得分",          # 要写入得分的列名
    "primary_key": "id"                  # MySQL主键列（用于精准更新行）
}

# Excel配置（仅当DATA_SOURCE_TYPE="Excel"时生效）
EXCEL_CONFIG = {
    "file_path": "/Users/suyuxuan/Downloads/数据质检结果最终汇总表.xlsx",
    "sheet_name": "202509",
    "score_column": "月实际归集平均时间",
    "filter_column": "委办名称",
    "filter_value": "区城运中心",
    "target_column": "最终得分",          # 要写入得分的列名
    "save_mode": "new",                  # 保存模式：new=保存为新文件，overwrite=覆盖原文件
    "new_file_suffix": "_带最终得分"      # 新文件后缀（save_mode=new时生效）
}

# 2. 公式参数配置
OFFSET = 0.5          # 基础偏移量（使归一化值从0.5开始）
WEIGHT = 10           # 得分权重（放大最终结果）
LOG_BASE = 10         # 对数底数（10=常用对数，math.e=自然对数，需>1）
MIN_DATA_LENGTH = 3   # 去极值的最小数据量要求

# ======================== 工具函数（参数校验/辅助） ========================
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
    if DATA_SOURCE_TYPE == "MySQL" and not MYSQL_CONFIG["primary_key"]:
        errors.append("MySQL模式必须指定主键列（primary_key），如'id'")
    
    if errors:
        print("❌ 参数校验失败：")
        for err in errors:
            print(f"  - {err}")
        return False
    return True

def get_mysql_column_names(config: Dict) -> List[str]:
    """获取MySQL表的所有列名（用于校验目标列是否存在）"""
    try:
        conn = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            db=config["db"],
            charset="utf8mb4"  # 支持emoji/特殊字符
        )
        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE {config['table']}")
            columns = [row[0] for row in cursor.fetchall()]
        conn.close()
        return columns
    except Exception as e:
        print(f"❌ 获取MySQL列名失败：{str(e)}")
        return []

# ======================== 数据读取函数（保留完整数据集） ========================
def read_data_from_mysql(config: Dict) -> Tuple[List[float], pd.DataFrame]:
    """从MySQL读取数据：返回分数数组 + 完整筛选后的DataFrame（含主键）"""
    try:
        conn = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            db=config["db"],
            charset="utf8mb4"
        )
        # 读取筛选后的完整数据（含主键，用于后续精准更新）
        sql = f"""
            SELECT {config['primary_key']}, {config['score_column']} 
            FROM {config['table']} 
            WHERE {config['score_column']} IS NOT NULL 
            AND {config['filter_column']} = %s
        """
        df = pd.read_sql(sql, conn, params=(config["filter_value"],))
        conn.close()
        
        # 提取分数数组（确保为浮点数）
        data = df[config["score_column"]].astype(float).tolist()
        print(f"✅ MySQL读取成功：【{config['filter_column']}={config['filter_value']}】共{len(data)}条有效数据")
        return data, df
    except pymysql.MySQLError as e:
        print(f"❌ MySQL读取失败（数据库错误）：{e.args[0]} - {e.args[1]}")
        return [], pd.DataFrame()
    except Exception as e:
        print(f"❌ MySQL读取失败（其他错误）：{str(e)}")
        return [], pd.DataFrame()

def read_data_from_excel(config: Dict) -> Tuple[List[float], pd.DataFrame]:
    """从Excel读取数据：返回分数数组 + 完整DataFrame（含所有列）"""
    try:
        # 读取完整Excel数据（指定引擎兼容新版Excel）
        df = pd.read_excel(
            config["file_path"], 
            sheet_name=config["sheet_name"],
            engine="openpyxl"
        )
        
        # 校验列是否存在
        if config["filter_column"] not in df.columns:
            print(f"❌ Excel中无筛选列【{config['filter_column']}】，请检查列名是否正确")
            return [], pd.DataFrame()
        if config["score_column"] not in df.columns:
            print(f"❌ Excel中无分数列【{config['score_column']}】，请检查列名是否正确")
            return [], pd.DataFrame()
        
        # 筛选目标数据（保留完整行）
        df_filtered = df[
            (df[config["filter_column"]] == config["filter_value"]) & 
            (df[config["score_column"]].notna())
        ].copy()
        
        # 提取分数数组（处理字符串格式的数值）
        data = df_filtered[config["score_column"]].apply(
            lambda x: float(x) if str(x).replace('.','').isdigit() else None
        ).dropna().tolist()
        
        print(f"✅ Excel读取成功：【{config['filter_column']}={config['filter_value']}】共{len(data)}条有效数据")
        return data, df  # 返回完整df，用于后续写入所有行
    except FileNotFoundError:
        print(f"❌ Excel文件不存在：{config['file_path']}，请检查文件路径")
        return [], pd.DataFrame()
    except Exception as e:
        print(f"❌ Excel读取失败：{str(e)}")
        return [], pd.DataFrame()

# ======================== 数据预处理 + 得分计算 ========================
def preprocess_data(raw_data: List[float]) -> Tuple[List[float], Optional[float], Optional[float]]:
    """预处理数据：去除极值，返回处理后数组+其最小/最大值（增强容错）"""
    if len(raw_data) < MIN_DATA_LENGTH:
        print(f"⚠️ 有效数据量{len(raw_data)} < 最小要求{MIN_DATA_LENGTH}，无法去极值！直接使用原始数据")
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
    """计算单个数值的最终得分（分步计算，避免log(0)）"""
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
        return round(final_score, 4)  # 保留4位小数
    except Exception as e:
        print(f"❌ 计算数值{x}的得分失败：{str(e)}")
        return None

# ======================== 写入得分到指定列（按行/主键精准写入） ========================
def write_score_to_mysql(config: Dict, df: pd.DataFrame, score_index_map: Dict):
    """将最终得分写入MySQL指定列（按主键映射，保留重复行）"""
    try:
        # 校验目标列是否存在，不存在则创建
        columns = get_mysql_column_names(config)
        if config["target_column"] not in columns:
            print(f"⚠️ MySQL表中无目标列【{config['target_column']}】，自动创建（类型：FLOAT）")
            conn = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                db=config["db"],
                charset="utf8mb4"
            )
            with conn.cursor() as cursor:
                cursor.execute(f"ALTER TABLE {config['table']} ADD COLUMN {config['target_column']} FLOAT")
            conn.commit()
            conn.close()
        
        # 批量更新得分（按主键精准更新）
        conn = pymysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            db=config["db"],
            charset="utf8mb4"
        )
        with conn.cursor() as cursor:
            update_count = 0
            for primary_key, final_score in score_index_map.items():
                if final_score is None:
                    continue
                sql = f"""
                    UPDATE {config['table']} 
                    SET {config['target_column']} = %s 
                    WHERE {config['primary_key']} = %s
                """
                cursor.execute(sql, (final_score, primary_key))
                update_count += 1
        conn.commit()
        conn.close()
        print(f"✅ MySQL写入成功：共更新{update_count}行【{config['target_column']}】列")
    except Exception as e:
        print(f"❌ MySQL写入失败：{str(e)}")

def write_score_to_excel(config: Dict, df: pd.DataFrame, score_index_map: Dict):
    """将最终得分写入Excel指定列（按行索引映射，保留重复行）"""
    try:
        # 初始化目标列（不存在则创建）
        if config["target_column"] not in df.columns:
            df[config["target_column"]] = None
            print(f"⚠️ Excel中无目标列【{config['target_column']}】，自动创建")
        
        # 按行索引写入得分
        update_count = 0
        for idx, final_score in score_index_map.items():
            if final_score is not None:
                df.loc[idx, config["target_column"]] = final_score
                update_count += 1
        
        # 保存文件（区分覆盖/新建）
        if config["save_mode"] == "overwrite":
            save_path = config["file_path"]
            print(f"⚠️ 启用覆盖模式，将修改原文件：{save_path}")
        else:
            # 生成新文件路径（避免覆盖原数据）
            file_name, ext = config["file_path"].rsplit(".", 1)
            save_path = f"{file_name}{config['new_file_suffix']}.{ext}"
        
        df.to_excel(save_path, sheet_name=config["sheet_name"], index=False, engine="openpyxl")
        print(f"✅ Excel写入成功：共更新{update_count}行【{config['target_column']}】列，文件保存至【{save_path}】")
    except Exception as e:
        print(f"❌ Excel写入失败：{str(e)}")

# ======================== 主执行流程（核心逻辑） ========================
def main():
    """主执行函数：读取数据→预处理→计算得分→写入指定列→输出结果"""
    # 1. 参数校验
    if not validate_params():
        return
    
    # 2. 读取数据（保留完整数据集）
    raw_data = []
    df_original = pd.DataFrame()
    if DATA_SOURCE_TYPE == "MySQL":
        raw_data, df_original = read_data_from_mysql(MYSQL_CONFIG)
    elif DATA_SOURCE_TYPE == "Excel":
        raw_data, df_original = read_data_from_excel(EXCEL_CONFIG)
    
    if not raw_data or df_original.empty:
        print(f"❌ 无有效数据（筛选值：{MYSQL_CONFIG.get('filter_value', EXCEL_CONFIG.get('filter_value'))}），程序退出")
        return
    
    # 3. 预处理数据（去极值）
    processed_data, p_min, p_max = preprocess_data(raw_data)
    if not processed_data or p_min is None or p_max is None:
        print("❌ 数据预处理后无有效数据，程序退出")
        return
    
    # 4. 计算最终得分（按行/主键映射，保留重复值）
    final_result = []
    score_index_map = {}  # key:行索引（Excel）/主键（MySQL），value:最终得分
    
    if DATA_SOURCE_TYPE == "MySQL":
        # MySQL：按主键映射
        filtered_df = df_original[
            (df_original[MYSQL_CONFIG["filter_column"]] == MYSQL_CONFIG["filter_value"]) & 
            (df_original[MYSQL_CONFIG["score_column"]].notna())
        ]
        for _, row in filtered_df.iterrows():
            raw_score = row[MYSQL_CONFIG["score_column"]]
            if raw_score not in processed_data:  # 跳过被去除的极值
                continue
            final_score = calculate_final_score(raw_score, p_min, p_max)
            final_result.append({"原始分数": raw_score, "最终得分": final_score})
            score_index_map[row[MYSQL_CONFIG["primary_key"]]] = final_score
    
    elif DATA_SOURCE_TYPE == "Excel":
        # Excel：按行索引映射
        filtered_mask = (
            (df_original[EXCEL_CONFIG["filter_column"]] == EXCEL_CONFIG["filter_value"]) & 
            (df_original[EXCEL_CONFIG["score_column"]].notna())
        )
        filtered_indices = df_original[filtered_mask].index
        for idx in filtered_indices:
            raw_score = df_original.loc[idx, EXCEL_CONFIG["score_column"]]
            if raw_score not in processed_data:  # 跳过被去除的极值
                continue
            final_score = calculate_final_score(raw_score, p_min, p_max)
            final_result.append({"原始分数": raw_score, "最终得分": final_score})
            score_index_map[idx] = final_score
    
    # 5. 输出计算结果
    print("\n==================== 最终计算结果 ====================")
    for idx, item in enumerate(final_result, 1):
        print(f"[{idx}] 原始分数：{item['原始分数']} → 最终得分：{item['最终得分']}")
    
    # 6. 写入最终得分到指定列
    if DATA_SOURCE_TYPE == "MySQL":
        write_score_to_mysql(MYSQL_CONFIG, df_original, score_index_map)
    elif DATA_SOURCE_TYPE == "Excel":
        write_score_to_excel(EXCEL_CONFIG, df_original, score_index_map)
    
    # 7. 汇总统计（保留重复值）
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

# ======================== 程序入口 ========================
if __name__ == "__main__":
    main()