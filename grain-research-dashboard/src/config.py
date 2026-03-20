# 谷物期现交易研究看板配置文件
# 数据源路径配置
DATA_SOURCE_PATH = r"E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据"

# 数据文件映射
DATA_FILES = {
    "cbot_futures": "CBOT新.xlsx",
    "corn_basis": "恢复-历史-基差月差套-lyy周报 - 副本.xlsx",
    "corn_inventory": "Part1-玉米02-利润与库存-lyy周报.xlsx",
    "wheat_spread": "钢联普麦-dce价差.xlsx",
    "sorghum_barley": "高粱大麦.xlsx",
    "import_data": "部分宏观进口和饲料替代的年度月度数据-周报(冲突文件-李洋洋).xlsx",
    "usda_sales": "usda销售进度和装船量-周报.xlsx",
    "usda_corn": "路透玉米usda数据更新-1.xlsx",
    "usda_sorghum": "路透高粱usda数据更新-1.xlsx",
    "hog_profit": "Part6-生猪03-生猪现货养殖利润-lyy周报xin.xlsx",
    "starch_weekly": "钢联数据淀粉周度数据-周报.xlsx",
    "ethanol": "美国乙醇数据-周报.xlsx",
    "corn_procured": "东北深加工收购量.xlsx",
}

# 输出配置
OUTPUT_PATH = "output"
DAILY_REPORT_PATH = "output/daily"
WEEKLY_REPORT_PATH = "output/weekly"

# 看报配置
DASHBOARD_PATH = "dashboard"
