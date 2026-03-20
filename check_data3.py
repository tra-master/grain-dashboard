import pandas as pd
import os

data_path = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

# wind-dce玉米
cbot_file = os.path.join(data_path, "CBOT新.xlsx")
print("=== wind-dce玉米 ===")
df = pd.read_excel(cbot_file, sheet_name="wind-dce玉米", nrows=25)
print(df)
print("\nColumns:", df.columns.tolist())

# 钢联普麦-dce价差.xlsx
wheat_file = os.path.join(data_path, "钢联普麦-dce价差.xlsx")
xl = pd.ExcelFile(wheat_file)
print("\n=== 钢联普麦 sheets ===")
print(xl.sheet_names)

for sheet in xl.sheet_names[:2]:
    print(f"\n--- {sheet} ---")
    df = pd.read_excel(wheat_file, sheet_name=sheet, nrows=20)
    print(df)
