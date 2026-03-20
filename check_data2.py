import pandas as pd
import os

data_path = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

cbot_file = os.path.join(data_path, "CBOT新.xlsx")
xl = pd.ExcelFile(cbot_file)

# 查找包含DCE、玉米、汇率等关键词的工作表
target_sheets = [s for s in xl.sheet_names if any(k in s.lower() for k in ['cbot玉米', 'cbt', 'dce', '玉米', '汇率', 'wind'])]
print("=== 目标工作表 ===")
for s in target_sheets:
    print(f"  - {s}")

print("\n=== 查看关键工作表 ===")

# 汇率
print("\n--- 汇率 ---")
df = pd.read_excel(cbot_file, sheet_name="汇率", nrows=20)
print(df)

# CBOT玉米收盘价
print("\n--- WIND-CBOT玉米收盘价 ---")
df = pd.read_excel(cbot_file, sheet_name="WIND-CBOT玉米收盘价", nrows=20)
print(df)
