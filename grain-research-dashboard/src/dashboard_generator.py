"""
HTML看板生成模块
生成谷物期现交易研究可视化看板
"""
import os
import json
from datetime import datetime


def generate_html_header():
    """生成HTML头部"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>谷物期现交易研究看板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --border-color: #30363d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-red: #f85149;
            --accent-yellow: #d29922;
            --accent-purple: #a371f7;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        /* 背景效果 */
        .bg-pattern {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(88, 166, 255, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(163, 113, 247, 0.06) 0%, transparent 50%),
                linear-gradient(180deg, var(--bg-primary) 0%, #0a0e14 100%);
            z-index: -1;
        }
        
        /* 导航栏 */
        .navbar {
            background: rgba(22, 27, 34, 0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .navbar-content {
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 18px;
        }
        
        .logo-text {
            font-size: 20px;
            font-weight: 600;
            background: linear-gradient(90deg, var(--text-primary), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-tabs {
            display: flex;
            gap: 4px;
            background: var(--bg-secondary);
            padding: 4px;
            border-radius: 8px;
        }
        
        .nav-tab {
            padding: 8px 16px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.2s;
            font-size: 14px;
            font-weight: 500;
        }
        
        .nav-tab:hover {
            color: var(--text-primary);
            background: var(--bg-card);
        }
        
        .nav-tab.active {
            background: var(--accent-blue);
            color: white;
        }
        
        /* 主内容区 */
        .main-content {
            max-width: 1600px;
            margin: 0 auto;
            padding: 24px;
        }
        
        /* 标题区 */
        .page-header {
            margin-bottom: 24px;
        }
        
        .page-title {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .page-subtitle {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        /* 统计卡片 */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        
        .stat-label {
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .stat-change {
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .stat-change.positive {
            color: var(--accent-green);
        }
        
        .stat-change.negative {
            color: var(--accent-red);
        }
        
        /* 图表网格 */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            margin-bottom: 24px;
        }
        
        .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }
        
        .chart-card.full-width {
            grid-column: 1 / -1;
        }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .chart-title {
            font-size: 16px;
            font-weight: 600;
        }
        
        .chart-actions {
            display: flex;
            gap: 8px;
        }
        
        .chart-btn {
            padding: 4px 12px;
            border: 1px solid var(--border-color);
            background: transparent;
            color: var(--text-secondary);
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }
        
        .chart-btn:hover {
            border-color: var(--accent-blue);
            color: var(--accent-blue);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
        }
        
        /* 数据表格 */
        .data-table-container {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .table-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .table-title {
            font-size: 16px;
            font-weight: 600;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .data-table th,
        .data-table td {
            padding: 12px 20px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        .data-table th {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 13px;
        }
        
        .data-table td {
            font-size: 14px;
        }
        
        .data-table tr:hover td {
            background: rgba(88, 166, 255, 0.05);
        }
        
        /* 标签 */
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .tag-blue {
            background: rgba(88, 166, 255, 0.15);
            color: var(--accent-blue);
        }
        
        .tag-green {
            background: rgba(63, 185, 80, 0.15);
            color: var(--accent-green);
        }
        
        .tag-red {
            background: rgba(248, 81, 73, 0.15);
            color: var(--accent-red);
        }
        
        .tag-yellow {
            background: rgba(210, 153, 34, 0.15);
            color: var(--accent-yellow);
        }
        
        /* 页脚 */
        .footer {
            text-align: center;
            padding: 24px;
            color: var(--text-secondary);
            font-size: 13px;
            border-top: 1px solid var(--border-color);
            margin-top: 24px;
        }
        
        /* 响应式 */
        @media (max-width: 1024px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
            
            .navbar-content {
                flex-direction: column;
                gap: 16px;
            }
            
            .nav-tabs {
                flex-wrap: wrap;
                justify-content: center;
            }
        }
        
        /* 动画 */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-in {
            animation: fadeIn 0.4s ease-out forwards;
        }
        
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.2s; }
        .delay-3 { animation-delay: 0.3s; }
        .delay-4 { animation-delay: 0.4s; }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="navbar-content">
            <div class="logo">
                <div class="logo-icon">G</div>
                <span class="logo-text">谷物期现交易研究看板</span>
            </div>
            <div class="nav-tabs">
                <button class="nav-tab active" data-page="dashboard">总览</button>
                <button class="nav-tab" data-page="futures">期货</button>
                <button class="nav-tab" data-page="basis">基差月差</button>
                <button class="nav-tab" data-page="inventory">库存利润</button>
                <button class="nav-tab" data-page="import">进口数据</button>
                <button class="nav-tab" data-page="usda">USDA</button>
                <button class="nav-tab" data-page="hog">养殖利润</button>
            </div>
        </div>
    </nav>
    
    <!-- 主内容 -->
    <main class="main-content">
        <!-- 总览页面 -->
        <div id="page-dashboard" class="page">
            <div class="page-header">
                <h1 class="page-title">市场总览</h1>
                <p class="page-subtitle">谷物期现市场关键指标实时监控 | 更新日期：''' + datetime.now().strftime('%Y-%m-%d %H:%M') + '''</p>
            </div>
            
            <!-- 关键指标卡片 -->
            <div class="stats-grid">
                <div class="stat-card animate-in delay-1">
                    <div class="stat-label">
                        <span>🌽 CBOT玉米期货</span>
                    </div>
                    <div class="stat-value" id="corn-price">--</div>
                    <div class="stat-change positive" id="corn-change">
                        <span>↑</span> <span>--</span>
                    </div>
                </div>
                
                <div class="stat-card animate-in delay-2">
                    <div class="stat-label">
                        <span>🌾 CBOT小麦期货</span>
                    </div>
                    <div class="stat-value" id="wheat-price">--</div>
                    <div class="stat-change negative" id="wheat-change">
                        <span>↓</span> <span>--</span>
                    </div>
                </div>
                
                <div class="stat-card animate-in delay-3">
                    <div class="stat-label">
                        <span>📊 玉米基差</span>
                    </div>
                    <div class="stat-value" id="basis-corn">--</div>
                    <div class="stat-change" id="basis-corn-change">--</div>
                </div>
                
                <div class="stat-card animate-in delay-4">
                    <div class="stat-label">
                        <span>📈 深加工库存</span>
                    </div>
                    <div class="stat-value" id="inventory">--</div>
                    <div class="stat-change" id="inventory-change">--</div>
                </div>
            </div>
            
            <!-- 图表区 -->
            <div class="charts-grid">
                <div class="chart-card full-width">
                    <div class="chart-header">
                        <h3 class="chart-title">CBOT期货价格走势</h3>
                        <div class="chart-actions">
                            <button class="chart-btn">1M</button>
                            <button class="chart-btn">3M</button>
                            <button class="chart-btn active">6M</button>
                            <button class="chart-btn">1Y</button>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="cbotChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title">玉米基差走势</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="basisChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title">深加工库存趋势</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="inventoryChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 期货页面 -->
        <div id="page-futures" class="page" style="display: none;">
            <div class="page-header">
                <h1 class="page-title">期货市场</h1>
                <p class="page-subtitle">CBOT玉米、小麦期货价格走势分析</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-card full-width">
                    <div class="chart-header">
                        <h3 class="chart-title">CBOT期货价格对比</h3>
                    </div>
                    <div class="chart-container" style="height: 400px;">
                        <canvas id="futuresCompareChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 基差月差页面 -->
        <div id="page-basis" class="page" style="display: none;">
            <div class="page-header">
                <h1 class="page-title">基差月差分析</h1>
                <p class="page-subtitle">玉米、小麦基差与月差走势</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title">玉米基差</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="cornBasisChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title">玉米月差</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="cornSpreadChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 库存利润页面 -->
        <div id="page-inventory" class="page" style="display: none;">
            <div class="page-header">
                <h1 class="page-title">库存与利润</h1>
                <p class="page-subtitle">深加工企业库存及利润变化</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">当前库存</div>
                    <div class="stat-value" id="inv-current">--</div>
                    <div class="stat-change" id="inv-change">--</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">加工利润</div>
                    <div class="stat-value" id="profit-current">--</div>
                    <div class="stat-change" id="profit-change">--</div>
                </div>
            </div>
            
            <div class="charts-grid">
                <div class="chart-card full-width">
                    <div class="chart-header">
                        <h3 class="chart-title">库存与利润走势</h3>
                    </div>
                    <div class="chart-container" style="height: 350px;">
                        <canvas id="inventoryProfitChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 进口数据页面 -->
        <div id="page-import" class="page" style="display: none;">
            <div class="page-header">
                <h1 class="page-title">进口数据</h1>
                <p class="page-subtitle">高粱、大麦等替代品进口量价分析</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title">高粱进口</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="sorghumChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-card">
                    <div class="chart-header">
                        <h3 class="chart-title">大麦进口</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="barleyChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- USDA页面 -->
        <div id="page-usda" class="page" style="display: none;">
            <div class="page-header">
                <h1 class="page-title">USDA供需报告</h1>
                <p class="page-subtitle">USDA销售进度与供需平衡表</p>
            </div>
            
            <div class="data-table-container">
                <div class="table-header">
                    <h3 class="table-title">USDA销售进度</h3>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>品种</th>
                            <th>年度</th>
                            <th>销售进度</th>
                            <th>装船进度</th>
                            <th>更新日期</th>
                        </tr>
                    </thead>
                    <tbody id="usda-sales-table">
                        <tr>
                            <td>玉米</td>
                            <td>2025/26</td>
                            <td><span class="tag tag-green">75%</span></td>
                            <td><span class="tag tag-blue">45%</span></td>
                            <td>''' + datetime.now().strftime('%Y-%m-%d') + '''</td>
                        </tr>
                        <tr>
                            <td>小麦</td>
                            <td>2025/26</td>
                            <td><span class="tag tag-green">82%</span></td>
                            <td><span class="tag tag-blue">55%</span></td>
                            <td>''' + datetime.now().strftime('%Y-%m-%d') + '''</td>
                        </tr>
                        <tr>
                            <td>高粱</td>
                            <td>2025/26</td>
                            <td><span class="tag tag-yellow">60%</span></td>
                            <td><span class="tag tag-blue">38%</span></td>
                            <td>''' + datetime.now().strftime('%Y-%m-%d') + '''</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 养殖利润页面 -->
        <div id="page-hog" class="page" style="display: none;">
            <div class="page-header">
                <h1 class="page-title">养殖利润</h1>
                <p class="page-subtitle">生猪现货与养殖利润分析</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-card full-width">
                    <div class="chart-header">
                        <h3 class="chart-title">生猪养殖利润走势</h3>
                    </div>
                    <div class="chart-container" style="height: 350px;">
                        <canvas id="hogProfitChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <p>谷物期现交易研究看板 | 数据来源：钢联数据、USDA、路透 | 更新时间：''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
    </footer>
    
    <script>
        // Chart.js 全局配置
        Chart.defaults.color = '#8b949e';
        Chart.defaults.borderColor = '#30363d';
        
        // 模拟数据 - 实际使用时由Python脚本生成真实数据
        const mockData = {
            cbot: {
                corn: generateTimeSeries(180, 420, 480),
                wheat: generateTimeSeries(180, 580, 650)
            },
            basis: generateTimeSeries(180, -50, 50),
            inventory: generateTimeSeries(180, 8000, 15000),
            profit: generateTimeSeries(180, -100, 300)
        };
        
        function generateTimeSeries(days, min, max) {
            const data = [];
            let value = (min + max) / 2;
            const now = new Date();
            
            for (let i = days; i >= 0; i--) {
                const date = new Date(now);
                date.setDate(date.getDate() - i);
                value += (Math.random() - 0.5) * (max - min) * 0.1;
                value = Math.max(min, Math.min(max, value));
                data.push({
                    x: date.toISOString().split('T')[0],
                    y: Math.round(value * 100) / 100
                });
            }
            return data;
        }
        
        // 初始化图表
        let cbotChart, basisChart, inventoryChart;
        
        function initCharts() {
            // CBOT期货图表
            const cbotCtx = document.getElementById('cbotChart').getContext('2d');
            cbotChart = new Chart(cbotCtx, {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: '玉米',
                            data: mockData.cbot.corn,
                            borderColor: '#f9a825',
                            backgroundColor: 'rgba(249, 168, 37, 0.1)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 0,
                            pointHoverRadius: 4
                        },
                        {
                            label: '小麦',
                            data: mockData.cbot.wheat,
                            borderColor: '#ffa726',
                            backgroundColor: 'rgba(255, 167, 38, 0.1)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 0,
                            pointHoverRadius: 4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'month'
                            },
                            grid: {
                                color: '#21262d'
                            }
                        },
                        y: {
                            grid: {
                                color: '#21262d'
                            },
                            title: {
                                display: true,
                                text: '美分/蒲式耳'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'top'
                        },
                        tooltip: {
                            backgroundColor: '#21262d',
                            borderColor: '#30363d',
                            borderWidth: 1
                        }
                    }
                }
            });
            
            // 基差图表
            const basisCtx = document.getElementById('basisChart').getContext('2d');
            basisChart = new Chart(basisCtx, {
                type: 'line',
                data: {
                    datasets: [{
                        label: '基差',
                        data: mockData.basis,
                        borderColor: '#58a6ff',
                        backgroundColor: 'rgba(88, 166, 255, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { type: 'time', time: { unit: 'month' } },
                        y: { grid: { color: '#21262d' } }
                    }
                }
            });
            
            // 库存图表
            const invCtx = document.getElementById('inventoryChart').getContext('2d');
            inventoryChart = new Chart(invCtx, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: '库存',
                        data: mockData.inventory,
                        backgroundColor: 'rgba(163, 113, 247, 0.6)',
                        borderColor: '#a371f7',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { type: 'time', time: { unit: 'month' } },
                        y: { grid: { color: '#21262d' } }
                    }
                }
            });
        }
        
        // 页面切换
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', function() {
                // 更新标签状态
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // 显示对应页面
                const pageId = 'page-' + this.dataset.page;
                document.querySelectorAll('.page').forEach(page => {
                    page.style.display = 'none';
                });
                document.getElementById(pageId).style.display = 'block';
            });
        });
        
        // 初始化
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            updateStats();
        });
        
        function updateStats() {
            // 更新关键指标
            const cornData = mockData.cbot.corn;
            const wheatData = mockData.cbot.wheat;
            
            if (cornData.length > 0) {
                const latest = cornData[cornData.length - 1];
                const prev = cornData[cornData.length - 2];
                document.getElementById('corn-price').textContent = latest.y.toFixed(2);
                
                const change = latest.y - prev.y;
                const changeEl = document.getElementById('corn-change');
                if (change >= 0) {
                    changeEl.className = 'stat-change positive';
                    changeEl.innerHTML = '<span>↑</span> <span>+' + change.toFixed(2) + '</span>';
                } else {
                    changeEl.className = 'stat-change negative';
                    changeEl.innerHTML = '<span>↓</span> <span>' + change.toFixed(2) + '</span>';
                }
            }
            
            if (wheatData.length > 0) {
                const latest = wheatData[wheatData.length - 1];
                const prev = wheatData[wheatData.length - 2];
                document.getElementById('wheat-price').textContent = latest.y.toFixed(2);
                
                const change = latest.y - prev.y;
                const changeEl = document.getElementById('wheat-change');
                if (change >= 0) {
                    changeEl.className = 'stat-change positive';
                    changeEl.innerHTML = '<span>↑</span> <span>+' + change.toFixed(2) + '</span>';
                } else {
                    changeEl.className = 'stat-change negative';
                    changeEl.innerHTML = '<span>↓</span> <span>' + change.toFixed(2) + '</span>';
                }
            }
        }
    </script>
</body>
</html>
'''


def generate_daily_report(data):
    """生成每日跟踪报告"""
    html = generate_html_header()
    # 添加每日报告特定内容
    return html


def generate_weekly_report(data):
    """生成周度复盘报告"""
    html = generate_html_header()
    # 添加周度报告特定内容
    return html


def save_dashboard(html_content, output_path="dashboard/index.html"):
    """保存看板HTML文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Dashboard saved to {output_path}")


if __name__ == "__main__":
    print("Generating dashboard...")
    html = generate_html_header()
    save_dashboard(html)
    print("Done!")
