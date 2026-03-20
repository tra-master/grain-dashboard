import pandas as pd
import os

data_path = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"
cbot_file = os.path.join(data_path, "CBOT新.xlsx")

# 直接读取看原始列名
df = pd.read_excel(cbot_file, sheet_name="WIND-CBOT玉米收盘价", nrows=5)
print("=== Original CBOT columns ===")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")
