"""
数据读取模块
从Excel源文件读取谷物交易相关数据
"""
import os
import pandas as pd
from pathlib import Path

# 配置
DATA_SOURCE_PATH = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

DATA_FILES = {
    "cbot": "CBOT新.xlsx",
    "basis_spread": "恢复-历史-基差月差套-lyy周报 - 副本.xlsx",
    "corn_inventory": "Part1-玉米02-利润与库存-lyy周报.xlsx",
    "wheat_spread": "钢联普麦-dce价差.xlsx",
    "sorghum_barley": "高粱大麦.xlsx",
    "import_data": "部分宏观进口和饲料替代的年度月度数据-周报(冲突文件-李洋洋).xlsx",
    "usda_sales": "usda销售进度和装船量-周报.xlsx",
    "usda_corn": "路透玉米usda数据更新-1.xlsx",
    "usda_sorghum": "路透高粱usda数据更新-1.xlsx",
    "hog_profit": "Part6-生猪03-生猪现货养殖利润-lyy周报xin.xlsx",
    "starch": "钢联数据淀粉周度数据-周报.xlsx",
    "ethanol": "美国乙醇数据-周报.xlsx",
    "procured": "东北深加工收购量.xlsx",
}


def load_excel_file(filename, sheet_name=0):
    """加载单个Excel文件"""
    filepath = os.path.join(DATA_SOURCE_PATH, filename)
    if not os.path.exists(filepath):
        return None
    try:
        return pd.read_excel(filepath, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None


def load_all_data():
    """加载所有数据文件"""
    data = {}
    for key, filename in DATA_FILES.items():
        df = load_excel_file(filename)
        if df is not None:
            data[key] = df
            print(f"Loaded {filename}: {df.shape}")
        else:
            print(f"Failed to load {filename}")
    return data


def get_cbot_data():
    """获取CBOT期货数据"""
    df = load_excel_file(DATA_FILES["cbot"])
    if df is not None:
        # 返回数据供后续处理
        return df
    return None


def get_basis_spread_data():
    """获取基差月差数据"""
    df = load_excel_file(DATA_FILES["basis_spread"])
    return df


def get_inventory_profit_data():
    """获取库存利润数据"""
    df = load_excel_file(DATA_FILES["corn_inventory"])
    return df


def get_import_data():
    """获取进口数据"""
    df = load_excel_file(DATA_FILES["import_data"])
    return df


def get_usda_data():
    """获取USDA数据"""
    corn = load_excel_file(DATA_FILES["usda_corn"])
    sorghum = load_excel_file(DATA_FILES["usda_sorghum"])
    sales = load_excel_file(DATA_FILES["usda_sales"])
    return {"corn": corn, "sorghum": sorghum, "sales": sales}


def get_hog_profit_data():
    """获取生猪养殖利润数据"""
    df = load_excel_file(DATA_FILES["hog_profit"])
    return df


if __name__ == "__main__":
    print("Loading all data...")
    data = load_all_data()
    print(f"\nTotal files loaded: {len(data)}")
