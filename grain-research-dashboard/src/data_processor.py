"""
数据处理模块
清洗、标准化、聚合谷物交易数据
"""
import pandas as pd
import numpy as np
from datetime import datetime


def clean_date_column(df, date_col_name):
    """清洗日期列"""
    if date_col_name in df.columns:
        df[date_col_name] = pd.to_datetime(df[date_col_name], errors='coerce')
    return df


def clean_numeric_column(df, col_name):
    """清洗数值列"""
    if col_name in df.columns:
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    return df


def process_cbot_data(df):
    """处理CBOT期货数据"""
    if df is None:
        return None
    
    result = {}
    # 尝试识别玉米和小麦期货列
    for col in df.columns:
        col_lower = str(col).lower()
        if '玉米' in col or 'corn' in col_lower:
            result['corn'] = df[col]
        elif '小麦' in col or 'wheat' in col_lower:
            result['wheat'] = df[col]
    
    if '日期' in df.columns or 'date' in df.columns.str.lower():
        date_col = [c for c in df.columns if '日期' in c or 'date' in c.lower()][0]
        result['date'] = df[date_col]
    
    return pd.DataFrame(result)


def process_basis_spread(df):
    """处理基差月差数据"""
    if df is None:
        return None
    
    # 提取日期和基差月差数据
    result = {}
    for col in df.columns:
        col_str = str(col)
        if '日期' in col_str:
            result['date'] = df[col]
        elif '基差' in col_str:
            result['basis'] = df[col]
        elif '月差' in col_str:
            result['spread'] = df[col]
    
    return pd.DataFrame(result)


def process_inventory_profit(df):
    """处理库存利润数据"""
    if df is None:
        return None
    
    result = {}
    for col in df.columns:
        col_str = str(col)
        if '日期' in col_str:
            result['date'] = df[col]
        elif '库存' in col_str:
            result['inventory'] = df[col]
        elif '利润' in col_str:
            result['profit'] = df[col]
    
    return pd.DataFrame(result)


def process_import_data(df):
    """处理进口数据"""
    if df is None:
        return None
    
    result = {}
    for col in df.columns:
        col_str = str(col)
        if '日期' in col_str or '月份' in col_str:
            result['date'] = df[col]
        elif '高粱' in col_str:
            result['sorghum'] = df[col]
        elif '大麦' in col_str:
            result['barley'] = df[col]
    
    return pd.DataFrame(result)


def process_usda_data(usda_dict):
    """处理USDA数据"""
    result = {}
    for key, df in usda_dict.items():
        if df is not None:
            result[key] = process_inventory_profit(df)
    return result


def aggregate_to_daily(df, date_col='date', value_cols=None):
    """按日聚合数据"""
    if df is None or date_col not in df.columns:
        return df
    
    df = clean_date_column(df, date_col)
    df = df.dropna(subset=[date_col])
    
    if value_cols:
        for col in value_cols:
            df = clean_numeric_column(df, col)
    
    return df


def aggregate_to_weekly(df, date_col='date', value_cols=None):
    """按周聚合数据"""
    if df is None or date_col not in df.columns:
        return df
    
    df = clean_date_column(df, date_col)
    df = df.dropna(subset=[date_col])
    df['week'] = df[date_col].dt.isocalendar().week
    df['year'] = df[date_col].dt.year
    
    if value_cols:
        for col in value_cols:
            df = clean_numeric_column(df, col)
    
    weekly = df.groupby(['year', 'week']).agg({
        **{col: 'mean' for col in value_cols if col in df.columns},
        **{date_col: 'last'}
    }).reset_index()
    
    return weekly


def generate_summary_stats(df, value_cols=None):
    """生成汇总统计"""
    if df is None or value_cols is None:
        return {}
    
    stats = {}
    for col in value_cols:
        if col in df.columns:
            stats[col] = {
                'latest': df[col].iloc[-1] if len(df) > 0 else None,
                'mean': df[col].mean(),
                'min': df[col].min(),
                'max': df[col].max(),
                'change': df[col].iloc[-1] - df[col].iloc[-2] if len(df) > 1 else 0
            }
    return stats


def process_all_data(raw_data):
    """处理所有原始数据"""
    processed = {}
    
    # 处理各类数据
    if 'cbot' in raw_data:
        processed['cbot'] = process_cbot_data(raw_data['cbot'])
    
    if 'basis_spread' in raw_data:
        processed['basis_spread'] = process_basis_spread(raw_data['basis_spread'])
    
    if 'corn_inventory' in raw_data:
        processed['inventory_profit'] = process_inventory_profit(raw_data['corn_inventory'])
    
    if 'import_data' in raw_data:
        processed['import'] = process_import_data(raw_data['import_data'])
    
    if any(k in raw_data for k in ['usda_corn', 'usda_sorghum', 'usda_sales']):
        usda_dict = {
            'corn': raw_data.get('usda_corn'),
            'sorghum': raw_data.get('usda_sorghum'),
            'sales': raw_data.get('usda_sales')
        }
        processed['usda'] = process_usda_data(usda_dict)
    
    if 'hog_profit' in raw_data:
        processed['hog_profit'] = process_inventory_profit(raw_data['hog_profit'])
    
    return processed


if __name__ == "__main__":
    from data_loader import load_all_data
    
    print("Loading raw data...")
    raw_data = load_all_data()
    
    print("\nProcessing data...")
    processed = process_all_data(raw_data)
    
    print("\nProcessed data keys:", list(processed.keys()))
