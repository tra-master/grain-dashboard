"""
数据导出模块
将计算好的价差数据导出为JSON供前端使用
"""
import sys
import json
import os
from datetime import datetime

sys.path.insert(0, 'src')
from data_loader_new import load_all_spread_data

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'data')


def export_to_json():
    """导出所有价差数据到JSON文件"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Loading data...")
    data = load_all_spread_data()
    
    export_data = {}
    
    # 1. DCE月间价差 - 时间序列
    if data.get('dce_spreads') is not None:
        df = data['dce_spreads'].tail(365)
        export_data['dce_spreads'] = {
            'labels': [d.strftime('%Y-%m-%d') for d in df.index],
            'datasets': {}
        }
        for col in df.columns:
            export_data['dce_spreads']['datasets'][col] = df[col].tolist()
    
    # 2. DCE月间价差 - 季节图（按年分组，每年一条线）
    if data.get('dce_spreads') is not None:
        import pandas as pd
        import numpy as np
        df_all = data['dce_spreads']
        # 生成完整 MM-DD 坐标轴（01-01 ~ 12-31，去掉02-29）
        all_days = pd.date_range('2000-01-01', '2000-12-31', freq='D')
        all_days = [d.strftime('%m-%d') for d in all_days if d.strftime('%m-%d') != '02-29']
        export_data['dce_spreads_seasonal'] = {'labels': all_days, 'datasets': {}}
        df_all = df_all.copy()
        df_all['month_day'] = df_all.index.strftime('%m-%d')
        df_all['year'] = df_all.index.year
        years = sorted(df_all['year'].unique())
        for spread_col in [c for c in df_all.columns if c not in ('month_day', 'year')]:
            export_data['dce_spreads_seasonal']['datasets'][spread_col] = {}
            for yr in years:
                yr_df = df_all[df_all['year'] == yr][['month_day', spread_col]].set_index('month_day')
                row = []
                for day in all_days:
                    if day in yr_df.index:
                        v = yr_df.loc[day, spread_col]
                        row.append(None if (v is None or (isinstance(v, float) and np.isnan(v))) else round(float(v), 2))
                    else:
                        row.append(None)
                export_data['dce_spreads_seasonal']['datasets'][spread_col][str(yr)] = row
    
    # 3. CBOT-DCE价差 - 时间序列
    if data.get('cbot_dce_spreads') is not None:
        df = data['cbot_dce_spreads'].tail(365)
        export_data['cbot_dce_spreads'] = {
            'labels': [d.strftime('%Y-%m-%d') for d in df.index],
            'datasets': {}
        }
        for col in df.columns:
            vals = df[col].dropna().tolist()
            dates = [d.strftime('%Y-%m-%d') for d in df[col].dropna().index]
            export_data['cbot_dce_spreads']['datasets'][col] = {
                'dates': dates,
                'values': vals
            }
    
    # 4. CBOT-DCE价差 - 季节图（按年分组）
    if data.get('cbot_dce_spreads') is not None:
        import pandas as pd
        import numpy as np
        df_all = data['cbot_dce_spreads']
        all_days = pd.date_range('2000-01-01', '2000-12-31', freq='D')
        all_days = [d.strftime('%m-%d') for d in all_days if d.strftime('%m-%d') != '02-29']
        export_data['cbot_dce_spreads_seasonal'] = {'labels': all_days, 'datasets': {}}
        df_all = df_all.copy()
        df_all['month_day'] = df_all.index.strftime('%m-%d')
        df_all['year'] = df_all.index.year
        years = sorted(df_all['year'].unique())
        for spread_col in [c for c in df_all.columns if c not in ('month_day', 'year')]:
            export_data['cbot_dce_spreads_seasonal']['datasets'][spread_col] = {}
            for yr in years:
                yr_df = df_all[df_all['year'] == yr][['month_day', spread_col]].set_index('month_day')
                row = []
                for day in all_days:
                    if day in yr_df.index:
                        v = yr_df.loc[day, spread_col]
                        row.append(None if (v is None or (isinstance(v, float) and np.isnan(v))) else round(float(v), 2))
                    else:
                        row.append(None)
                export_data['cbot_dce_spreads_seasonal']['datasets'][spread_col][str(yr)] = row
    
    # 5. 周口小麦-玉米价差 - 时间序列
    if data.get('wheat_corn_spreads') is not None:
        df = data['wheat_corn_spreads'].tail(365)
        export_data['wheat_corn_spreads'] = {
            'labels': [d.strftime('%Y-%m-%d') for d in df.index],
            'datasets': {}
        }
        for col in df.columns:
            vals = df[col].dropna().tolist()
            dates = [d.strftime('%Y-%m-%d') for d in df[col].dropna().index]
            export_data['wheat_corn_spreads']['datasets'][col] = {
                'dates': dates,
                'values': vals
            }
    
    # 6. 周口小麦-玉米价差 - 季节图（按年分组）
    if data.get('wheat_corn_spreads') is not None:
        import pandas as pd
        import numpy as np
        df_all = data['wheat_corn_spreads']
        all_days = pd.date_range('2000-01-01', '2000-12-31', freq='D')
        all_days = [d.strftime('%m-%d') for d in all_days if d.strftime('%m-%d') != '02-29']
        export_data['wheat_corn_spreads_seasonal'] = {'labels': all_days, 'datasets': {}}
        df_all = df_all.copy()
        df_all['month_day'] = df_all.index.strftime('%m-%d')
        df_all['year'] = df_all.index.year
        years = sorted(df_all['year'].unique())
        for spread_col in [c for c in df_all.columns if c not in ('month_day', 'year')]:
            export_data['wheat_corn_spreads_seasonal']['datasets'][spread_col] = {}
            for yr in years:
                yr_df = df_all[df_all['year'] == yr][['month_day', spread_col]].set_index('month_day')
                row = []
                for day in all_days:
                    if day in yr_df.index:
                        v = yr_df.loc[day, spread_col]
                        row.append(None if (v is None or (isinstance(v, float) and np.isnan(v))) else round(float(v), 2))
                    else:
                        row.append(None)
                export_data['wheat_corn_spreads_seasonal']['datasets'][spread_col][str(yr)] = row
    
    # 7. FOB基差数据
    export_data['fob_basis'] = data.get('fob_basis', {})
    
    # 8. 最新价差数据(用于卡片展示)
    if data.get('dce_spreads') is not None:
        latest = data['dce_spreads'].iloc[-1].to_dict()
        export_data['latest_dce_spreads'] = latest
    
    if data.get('cbot_dce_spreads') is not None:
        latest = data['cbot_dce_spreads'].iloc[-1].to_dict()
        export_data['latest_cbot_dce_spreads'] = latest
    
    if data.get('wheat_corn_spreads') is not None:
        latest = data['wheat_corn_spreads'].iloc[-1].to_dict()
        export_data['latest_wheat_corn_spreads'] = latest
    
    # 写入JSON文件
    output_file = os.path.join(OUTPUT_DIR, 'spread_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"Data exported to: {output_file}")
    return export_data


if __name__ == "__main__":
    export_to_json()
