import pandas as pd
import os

data_path = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

# 检查基差月差数据文件
basis_file = os.path.join(data_path, "恢复-历史-基差月差套-lyy周报 - 副本.xlsx")
xl = pd.ExcelFile(basis_file)
print("=== 基差月差 ALL sheets ===")
for s in xl.sheet_names:
    print(f"  - {s}")

# 查看是否有FOB相关
fob_sheets = [s for s in xl.sheet_names if 'fob' in s.lower() or '基差' in s]
print("\n=== FOB相关sheets ===")
for s in fob_sheets:
    print(f"--- {s} ---")
    df = pd.read_excel(basis_file, sheet_name=s, nrows=10)
    print(df)
    print()
