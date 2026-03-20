import pandas as pd
import os

data_path = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

# 周口小麦-玉米主力详细数据
wheat_file = os.path.join(data_path, "钢联普麦-dce价差.xlsx")
df = pd.read_excel(wheat_file, sheet_name="周口小麦-玉米主力", nrows=30)
print("=== 周口小麦-玉米主力 ===")
print(df.iloc[:10, :8])

# 基差月差数据
basis_file = os.path.join(data_path, "恢复-历史-基差月差套-lyy周报 - 副本.xlsx")
xl = pd.ExcelFile(basis_file)
print("\n=== 基差月差 sheets ===")
print(xl.sheet_names[:15])

for sheet in xl.sheet_names[:5]:
    print(f"\n--- {sheet} ---")
    df = pd.read_excel(basis_file, sheet_name=sheet, nrows=15)
    print(df)
