# 谷物期现交易研究看板

基于本地Excel数据源的谷物期现交易研究每日跟踪及周度复盘看板系统

## 功能特性

- 📊 **每日跟踪**: 实时更新期货价格、基差、月差、库存、利润等关键指标
- 📈 **周度复盘**: 每周汇总分析USDA供需报告、进口数据、养殖利润等维度
- 🎨 **可视化看板**: 使用Chart.js生成交互式图表，深色主题专业金融风格
- ⚙️ **自动化**: 支持Windows定时任务每日自动更新数据

## 数据源

数据来源: `E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据`

包含以下数据文件:
- CBOT期货价格数据
- 玉米/小麦基差月差数据
- 深加工企业库存与利润
- 高粱、大麦进口数据
- USDA销售进度与供需报告
- 生猪养殖利润数据
- 淀粉周度数据
- 美国乙醇数据

## 看板页面

1. **总览**: 关键指标卡片 + 期货走势概览图
2. **期货市场**: CBOT玉米/小麦价格走势图
3. **基差月差**: 基差、月差实时对比图表
4. **库存利润**: 深加工库存和利润趋势
5. **进口数据**: 高粱大麦进口量价图表
6. **USDA专区**: 供需报告和销售进度
7. **养殖利润**: 生猪养殖利润走势

## 快速开始

### 1. 查看看板

直接在浏览器中打开:
```
dashboard/index.html
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行数据更新

```bash
python src/main.py
```

### 4. 设置每日自动更新

```bash
python setup_task.py
```

## 项目结构

```
grain-research-dashboard/
├── data/
│   └── raw/                    # 原始Excel数据(可配置链接)
├── src/
│   ├── config.py               # 配置文件
│   ├── data_loader.py           # 数据读取模块
│   ├── data_processor.py        # 数据处理模块
│   ├── dashboard_generator.py   # HTML生成模块
│   └── main.py                 # 主入口
├── dashboard/
│   └── index.html              # 看板主页面
├── output/
│   ├── daily/                  # 每日报告
│   └── weekly/                 # 周度报告
├── run_dashboard.bat          # Windows运行脚本
├── setup_task.py              # 定时任务设置
├── requirements.txt           # Python依赖
└── README.md                  # 说明文档
```

## 技术栈

- **数据处理**: Python + Pandas + OpenPyXL
- **可视化**: HTML5 + Chart.js + Bootstrap
- **自动化**: Windows定时任务

## 注意事项

- Excel文件较大，首次加载可能需要等待
- 数据源为本地文件，需确保文件路径稳定
- 建议使用Chrome或Edge浏览器查看看板

## 更新日志

### v1.0 (2025-03-15)
- 初始版本
- 支持7个看板页面
- 包含模拟数据展示
- 支持定时任务自动更新
