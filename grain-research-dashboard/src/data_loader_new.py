"""
数据加载和处理模块
支持谷物期现交易研究看板的所有数据需求
"""
import os
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# 配置
DATA_SOURCE_PATH = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

DATA_FILES = {
    "cbot": "CBOT新.xlsx",
    "basis_spread": "恢复-历史-基差月差套-lyy周报 - 副本.xlsx",
    "wheat_spread": "钢联普麦-dce价差.xlsx",
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


def load_dce_corn_futures():
    """加载DCE玉米期货数据"""
    df = load_excel_file(DATA_FILES["cbot"], sheet_name="wind-dce玉米")
    if df is None:
        return None
    
    df = df.iloc[3:].copy()
    num_cols = len(df.columns)
    
    cols = ['Date', 'C01', 'C03', 'C05', 'C07', 'C09', 'C11', 'C_连续']
    df.columns = cols[:num_cols]
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.set_index('Date')
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.sort_index()


def load_cbot_corn_futures():
    """加载CBOT玉米期货数据"""
    df = load_excel_file(DATA_FILES["cbot"], sheet_name="WIND-CBOT玉米收盘价")
    if df is None:
        return None
    
    df = df.iloc[2:].copy()
    num_cols = len(df.columns)
    
    cols = ['Date', 'C03M.CBT', 'C05M.CBT', 'C07M.CBT', 'C09M.CBT', 'C12M.CBT', 
            'C.CBT'] + [f'Extra_{i}' for i in range(num_cols-7)]
    df.columns = cols[:num_cols]
    
    keep_cols = ['Date', 'C03M.CBT', 'C05M.CBT', 'C07M.CBT', 'C09M.CBT', 'C12M.CBT', 'C.CBT']
    df = df[[c for c in keep_cols if c in df.columns]]
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.set_index('Date')
    
    for col in df.columns:
        if col != 'Date':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.sort_index()


def load_exchange_rate():
    """加载汇率数据"""
    df = load_excel_file(DATA_FILES["cbot"], sheet_name="汇率")
    if df is None:
        return None
    
    df = df.iloc[4:].copy()
    num_cols = len(df.columns)
    
    cols = ['Date', 'USD_CNY'] + [f'Col_{i}' for i in range(num_cols-2)]
    df.columns = cols
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['USD_CNY'] = pd.to_numeric(df['USD_CNY'], errors='coerce')
    df = df.dropna(subset=['Date', 'USD_CNY'])
    df = df.set_index('Date')
    
    return df[['USD_CNY']].sort_index()


def load_zhoukou_wheat():
    """加载周口小麦数据"""
    df = load_excel_file(DATA_FILES["wheat_spread"], sheet_name="周口小麦-玉米主力")
    if df is None:
        return None
    
    df = df.iloc[2:].copy()
    num_cols = len(df.columns)
    
    cols = ['Date', 'Wheat_Price', 'Corn_Price', 'Spread'] + [f'Col_{i}' for i in range(num_cols-4)]
    df.columns = cols
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Wheat_Price'] = pd.to_numeric(df['Wheat_Price'], errors='coerce')
    df['Corn_Price'] = pd.to_numeric(df['Corn_Price'], errors='coerce')
    df['Spread'] = pd.to_numeric(df['Spread'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df = df.set_index('Date')
    
    return df[['Wheat_Price', 'Corn_Price', 'Spread']].sort_index()


def calculate_dce_spreads(dce_df):
    """计算DCE玉米期货月间价差"""
    if dce_df is None or dce_df.empty:
        return None
    
    spreads = pd.DataFrame(index=dce_df.index)
    
    # 月间价差组合 (近月-远月)
    spread_pairs = [
        ('1-3', 'C01', 'C03'),
        ('1-5', 'C01', 'C05'),
        ('3-5', 'C03', 'C05'),
        ('3-7', 'C03', 'C07'),
        ('3-9', 'C03', 'C09'),
        ('5-7', 'C05', 'C07'),
        ('5-9', 'C05', 'C09'),
        ('7-9', 'C07', 'C09'),
        ('9-11', 'C09', 'C11'),
        ('9-1', 'C09', 'C01'),
        ('11-1', 'C11', 'C01'),
    ]
    
    for spread_name, col1, col2 in spread_pairs:
        if col1 in dce_df.columns and col2 in dce_df.columns:
            spreads[spread_name] = dce_df[col1] - dce_df[col2]
    
    return spreads


def calculate_cbot_dce_spread_v2(cbot_df, dce_df, rate_df):
    """
    计算CBOT-DCE价差 (新版本)
    公式: CBOT玉米X月价格 × 0.3937 × (X+2)月份人民币兑美元汇率 - DCE玉米(X+2)月期货价格
    X表示CBOT的合约月份，如果DCE玉米没有X+2月的期货合约，则使用X+3月
    """
    if cbot_df is None or dce_df is None or rate_df is None:
        return None
    
    # CBOT玉米合约月份映射
    cbot_months = {
        '03': 'C03M.CBT',
        '05': 'C05M.CBT',
        '07': 'C07M.CBT',
        '09': 'C09M.CBT',
        '12': 'C12M.CBT',
    }
    
    # DCE对应月份 (X+2), 如果没有则用X+3
    # CBOT 3月 -> DCE 5月 (3+2=5, 3+3=6无, 用5月)
    # CBOT 5月 -> DCE 7月 (5+2=7)
    # CBOT 7月 -> DCE 9月 (7+2=9)
    # CBOT 9月 -> DCE 11月 (9+2=11)
    # CBOT 12月 -> DCE 2月 (12+2=14, 跨年, 用C01)
    dce_months_mapping = {
        '03': ('C05', 'C07'),  # 优先C05, 无则C07
        '05': ('C07', 'C09'),  # 优先C07, 无则C09
        '07': ('C09', 'C11'),  # 优先C09, 无则C11
        '09': ('C11', 'C01'),  # 优先C11, 无则C01
        '12': ('C01', 'C03'),  # 优先C01, 无则C03
    }
    
    result = pd.DataFrame(index=cbot_df.index)
    rate_factor = 0.3937
    
    for cbt_month, cbt_col in cbot_months.items():
        found_col = None
        for col in cbot_df.columns:
            if cbt_month in col:
                found_col = col
                break
        
        if found_col is None:
            continue
        
        # 获取对应的DCE列
        dce_preferred, dce_fallback = dce_months_mapping.get(cbt_month, (None, None))
        
        # 尝试使用首选DCE月份，如果没有则使用备用
        dce_col = dce_preferred if dce_preferred in dce_df.columns else dce_fallback
        if dce_col is None or dce_col not in dce_df.columns:
            continue
        
        spread_name = f'CBOT-{cbt_month}vDCE-{dce_col}'
        
        # 合并数据
        temp = pd.DataFrame({
            'CBOT': cbot_df[found_col],
            'DCE': dce_df[dce_col],
            'Rate': rate_df['USD_CNY']
        }).dropna()
        
        if not temp.empty:
            result[spread_name] = temp['CBOT'] * rate_factor * temp['Rate'] - temp['DCE']
    
    return result


def calculate_wheat_corn_spread(wheat_df, dce_df):
    """计算周口小麦现货-玉米期货价差"""
    if wheat_df is None or dce_df is None:
        return None
    
    spreads = pd.DataFrame(index=wheat_df.index)
    
    corn_cols = ['C01', 'C03', 'C05', 'C07', 'C09', 'C11']
    
    for col in corn_cols:
        if col in dce_df.columns:
            spread_name = f'Wheat-C{col}'
            temp = pd.DataFrame({
                'Wheat': wheat_df['Wheat_Price'],
                'DCE': dce_df[col]
            }).dropna()
            
            if not temp.empty:
                spreads[spread_name] = temp['Wheat'] - temp['DCE']
    
    return spreads


def to_seasonal_data(df):
    """
    将日度数据转换为季节图格式
    按月-日分组，计算多年均值
    """
    if df is None or df.empty:
        return None
    
    # 提取月-日
    df = df.copy()
    df['month_day'] = df.index.strftime('%m-%d')
    df['year'] = df.index.year
    
    # 按月-日分组，计算均值
    seasonal = df.groupby('month_day').mean()
    
    return seasonal


def get_fob_basis_data():
    """获取FOB基差数据 (需要网络获取)"""
    # 这里先返回占位数据，实际使用时需要从网络获取
    # FOB价格 - CBOT价格换算 = 基差
    # CBOT价格单位: 美分/蒲式耳 -> 美元/吨 = CBOT价格 * 100 / 25.4
    return {
        'brazil': {
            'name': '巴西(帕拉纳瓜港)',
            'fob_price': 218.00,
            'unit': 'USD/mt',
            'last_update': '2025-12-15',
            'change': -4.00
        },
        'us': {
            'name': '美国(墨西哥湾NOLA)',
            'fob_price': 213.00,
            'unit': 'USD/mt',
            'last_update': '2025-12-15',
            'change': -1.25
        },
        'ukraine': {
            'name': '乌克兰(黑海)',
            'fob_price': 198.00,
            'unit': 'USD/mt',
            'last_update': '2025-12-15',
            'change': -0.25
        }
    }


def load_all_spread_data():
    """加载并计算所有价差数据"""
    print("Loading DCE corn futures...")
    dce_df = load_dce_corn_futures()
    print(f"  DCE data: {dce_df.shape if dce_df is not None else 'None'}")
    
    print("Loading CBOT corn futures...")
    cbot_df = load_cbot_corn_futures()
    print(f"  CBOT data: {cbot_df.shape if cbot_df is not None else 'None'}")
    
    print("Loading exchange rate...")
    rate_df = load_exchange_rate()
    print(f"  Rate data: {rate_df.shape if rate_df is not None else 'None'}")
    
    print("Loading Zhoukou wheat data...")
    wheat_df = load_zhoukou_wheat()
    print(f"  Wheat data: {wheat_df.shape if wheat_df is not None else 'None'}")
    
    data = {
        'dce_futures': dce_df,
        'cbot_futures': cbot_df,
        'exchange_rate': rate_df,
        'zhoukou_wheat': wheat_df,
    }
    
    # DCE月间价差
    if dce_df is not None:
        print("Calculating DCE spreads...")
        data['dce_spreads'] = calculate_dce_spreads(dce_df)
        # 季节图数据
        data['dce_spreads_seasonal'] = to_seasonal_data(data['dce_spreads'])
    
    # CBOT-DCE价差 (新公式)
    if cbot_df is not None and dce_df is not None and rate_df is not None:
        print("Calculating CBOT-DCE spreads (new formula)...")
        data['cbot_dce_spreads'] = calculate_cbot_dce_spread_v2(cbot_df, dce_df, rate_df)
        data['cbot_dce_spreads_seasonal'] = to_seasonal_data(data['cbot_dce_spreads'])
    
    # 小麦-玉米价差
    if wheat_df is not None and dce_df is not None:
        print("Calculating Wheat-Corn spreads...")
        data['wheat_corn_spreads'] = calculate_wheat_corn_spread(wheat_df, dce_df)
        data['wheat_corn_spreads_seasonal'] = to_seasonal_data(data['wheat_corn_spreads'])
    
    # FOB基差
    data['fob_basis'] = get_fob_basis_data()
    
    return data


if __name__ == "__main__":
    data = load_all_spread_data()
    print("\n=== Data Summary ===")
    for key, val in data.items():
        if val is not None:
            if hasattr(val, 'shape'):
                print(f"{key}: {val.shape}")
            elif isinstance(val, dict):
                print(f"{key}: dict with {len(val)} keys")
            else:
                print(f"{key}: {type(val)}")
