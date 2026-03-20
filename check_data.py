import pandas as pd
import os

data_path = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

# 查看CBOT数据
cbot_file = os.path.join(data_path, "CBOT新.xlsx")
xl = pd.ExcelFile(cbot_file)
print("=== CBOT sheets ===")
print(xl.sheet_names)
print()

for sheet in xl.sheet_names[:3]:
    print(f"--- {sheet} ---")
    df = pd.read_excel(cbot_file, sheet_name=sheet, nrows=15)
    print(df)
    print()
