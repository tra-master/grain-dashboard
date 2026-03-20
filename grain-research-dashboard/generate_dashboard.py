"""
生成包含嵌入式数据的HTML看板
"""
import json
import os

# 读取数据
data_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'data', 'spread_data.json')
with open(data_path, 'r', encoding='utf-8') as f:
    spread_data = json.load(f)

# 转换为JavaScript格式
data_js = json.dumps(spread_data, ensure_ascii=False, indent=2)

html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>谷物期现价差分析看板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        .bg-pattern {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(88, 166, 255, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(163, 113, 247, 0.06) 0%, transparent 50%),
                linear-gradient(180deg, var(--bg-primary) 0%, #0a0e14 100%);
            z-index: -1;
        }
        
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
            flex-wrap: wrap;
            gap: 16px;
        }
        
        .logo { display: flex; align-items: center; gap: 12px; }
        
        .logo-icon {
            width: 36px; height: 36px;
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
            flex-wrap: wrap;
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
        
        .nav-tab:hover { color: var(--text-primary); background: var(--bg-card); }
        
        .nav-tab.active {
            background: var(--accent-blue);
            color: white;
        }
        
        .main-content {
            max-width: 1600px;
            margin: 0 auto;
            padding: 24px;
        }
        
        .page-header { margin-bottom: 24px; }
        
        .page-title {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .page-subtitle {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 600;
            margin: 32px 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .section-title:first-child { margin-top: 0; }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        
        .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        
        .stat-value {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 6px;
        }
        
        .stat-change {
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .stat-change.positive { color: var(--accent-green); }
        .stat-change.negative { color: var(--accent-red); }
        
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
        
        .chart-card.full-width { grid-column: 1 / -1; }
        .chart-card.half-width { grid-column: span 1; }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .chart-title { font-size: 16px; font-weight: 600; }
        
        .chart-container { position: relative; height: 300px; }
        
        .fob-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .fob-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        
        .fob-name {
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }
        
        .fob-price {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .fob-change {
            font-size: 14px;
        }
        
        .fob-change.positive { color: var(--accent-green); }
        .fob-change.negative { color: var(--accent-red); }
        
        .footer {
            text-align: center;
            padding: 24px;
            color: var(--text-secondary);
            font-size: 13px;
            border-top: 1px solid var(--border-color);
            margin-top: 24px;
        }
        
        .page { display: block; }
        .page.hidden { display: none; }
        
        @media (max-width: 1024px) {
            .charts-grid { grid-template-columns: 1fr; }
            .navbar-content { flex-direction: column; align-items: flex-start; }
            .nav-tabs { width: 100%; }
            .fob-grid { grid-template-columns: 1fr; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-in { animation: fadeIn 0.4s ease-out forwards; }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <nav class="navbar">
        <div class="navbar-content">
            <div class="logo">
                <div class="logo-icon">G</div>
                <span class="logo-text">谷物期现价差分析看板</span>
            </div>
            <div class="nav-tabs">
                <button class="nav-tab active" onclick="showPage('overview', event)">总览</button>
                <button class="nav-tab" onclick="showPage('dce-spreads', event)">DCE月间价差</button>
                <button class="nav-tab" onclick="showPage('cbot-dce', event)">CBOT-DCE价差</button>
                <button class="nav-tab" onclick="showPage('wheat-corn', event)">小麦-玉米价差</button>
                <button class="nav-tab" onclick="showPage('fob', event)">FOB基差</button>
            </div>
        </div>
    </nav>
    
    <div class="main-content">
        <!-- 总览页面 -->
        <div id="page-overview" class="page">
            <div class="page-header">
                <h1 class="page-title">价差数据总览</h1>
                <p class="page-subtitle">谷物期现交易关键价差指标实时监控</p>
            </div>
            
            <h3 class="section-title">DCE玉米期货月间价差 (最新)</h3>
            <div class="stats-grid" id="dce-spread-cards"></div>
            
            <h3 class="section-title">CBOT-DCE价差 (最新)</h3>
            <p class="page-subtitle" style="margin-bottom: 16px;">CBOT×0.3937×(X+2)月汇率-DCE(X+2)月</p>
            <div class="stats-grid" id="cbot-dce-cards"></div>
            
            <h3 class="section-title">周口小麦-玉米期货价差 (最新)</h3>
            <div class="stats-grid" id="wheat-corn-cards"></div>
            
            <h3 class="section-title">国际玉米FOB价格 (美元/吨)</h3>
            <div class="fob-grid" id="fob-cards"></div>
        </div>
        
        <!-- DCE月间价差页面 -->
        <div id="page-dce-spreads" class="page hidden">
            <div class="page-header">
                <h1 class="page-title">DCE玉米期货月间价差</h1>
                <p class="page-subtitle">季节图展示 - 按月-日展示多年均值</p>
            </div>
            <div class="charts-grid" id="dce-spreads-charts"></div>
        </div>
        
        <!-- CBOT-DCE价差页面 -->
        <div id="page-cbot-dce" class="page hidden">
            <div class="page-header">
                <h1 class="page-title">CBOT-DCE价差分析</h1>
                <p class="page-subtitle">CBOT玉米X月价格 × 0.3937 × (X+2)月份汇率 - DCE玉米(X+2)月期货价格</p>
            </div>
            <div class="charts-grid" id="cbot-dce-charts"></div>
        </div>
        
        <!-- 小麦-玉米价差页面 -->
        <div id="page-wheat-corn" class="page hidden">
            <div class="page-header">
                <h1 class="page-title">周口小麦-玉米期货价差</h1>
                <p class="page-subtitle">周口小麦现货价格 - DCE玉米各合约期货价格</p>
            </div>
            <div class="charts-grid" id="wheat-corn-charts"></div>
        </div>
        
        <!-- FOB基差页面 -->
        <div id="page-fob" class="page hidden">
            <div class="page-header">
                <h1 class="page-title">国际玉米FOB基差</h1>
                <p class="page-subtitle">巴西、美国、乌克兰玉米FOB价格</p>
            </div>
            <div class="fob-grid">
                <div class="fob-card">
                    <div class="fob-name">巴西(帕拉纳瓜港)</div>
                    <div class="fob-price" id="fob-brazil-price">--</div>
                    <div class="fob-change" id="fob-brazil-change">--</div>
                </div>
                <div class="fob-card">
                    <div class="fob-name">美国(墨西哥湾NOLA)</div>
                    <div class="fob-price" id="fob-us-price">--</div>
                    <div class="fob-change" id="fob-us-change">--</div>
                </div>
                <div class="fob-card">
                    <div class="fob-name">乌克兰(黑海)</div>
                    <div class="fob-price" id="fob-ukraine-price">--</div>
                    <div class="fob-change" id="fob-ukraine-change">--</div>
                </div>
            </div>
            
            <div class="chart-card full-width">
                <div class="chart-header">
                    <h3 class="chart-title">FOB基差计算说明</h3>
                </div>
                <div style="padding: 20px; color: var(--text-secondary); line-height: 1.8;">
                    <p>• FOB价格数据来源: GrainsPrices.com</p>
                    <p>• 数据更新日期: <span id="fob-update-date">--</span></p>
                    <p>• CBOT换算: CBOT(美分/蒲式耳) × 100 / 25.4 = USD/吨</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        数据最后更新: <span id="last-update">--</span>
    </div>
    
    <script>
        // 嵌入式数据
        const spreadData = DATA_PLACEHOLDER;
        
        // 颜色配置
        const chartColors = [
            '#58a6ff', '#3fb950', '#f85149', '#d29922', '#a371f7', 
            '#79c0ff', '#56d364', '#ff7b72', '#e3b341', '#bc8cff'
        ];
        
        // 初始化
        function init() {
            console.log('Initializing with data...');
            console.log('Keys:', Object.keys(spreadData));
            
            updateOverviewCards();
            initDCECharts();
            initCBTDCharts();
            initWheatCharts();
            initFOB();
            
            document.getElementById('last-update').textContent = new Date().toLocaleString('zh-CN');
        }
        
        // 更新总览卡片
        function updateOverviewCards() {
            // DCE月间价差
            const dceLatest = spreadData.latest_dce_spreads;
            if (dceLatest) {
                let html = '';
                for (const [key, val] of Object.entries(dceLatest)) {
                    if (val !== null && !isNaN(val) && key !== 'year') {
                        const isPositive = val >= 0;
                        html += \`
                            <div class="stat-card">
                                <div class="stat-label">DCE \${key}</div>
                                <div class="stat-value">\${val.toFixed(0)}</div>
                                <div class="stat-change \${isPositive ? 'positive' : 'negative'}">
                                    \${isPositive ? '↑' : '↓'} \${Math.abs(val).toFixed(0)}
                                </div>
                            </div>\`;
                    }
                }
                document.getElementById('dce-spread-cards').innerHTML = html;
            }
            
            // CBOT-DCE价差
            const cbotLatest = spreadData.latest_cbot_dce_spreads;
            if (cbotLatest) {
                let html = '';
                for (const [key, val] of Object.entries(cbotLatest)) {
                    if (val !== null && !isNaN(val)) {
                        const isPositive = val >= 0;
                        html += \`
                            <div class="stat-card">
                                <div class="stat-label">\${key}</div>
                                <div class="stat-value">\${val.toFixed(0)}</div>
                                <div class="stat-change \${isPositive ? 'positive' : 'negative'}">
                                    \${isPositive ? '溢价' : '折价'}
                                </div>
                            </div>\`;
                    }
                }
                document.getElementById('cbot-dce-cards').innerHTML = html;
            }
            
            // 周口小麦-玉米
            const wheatLatest = spreadData.latest_wheat_corn_spreads;
            if (wheatLatest) {
                let html = '';
                for (const [key, val] of Object.entries(wheatLatest)) {
                    if (val !== null && !isNaN(val) && key !== 'year') {
                        const isPositive = val >= 0;
                        html += \`
                            <div class="stat-card">
                                <div class="stat-label">\${key}</div>
                                <div class="stat-value">\${val.toFixed(0)}</div>
                                <div class="stat-change \${isPositive ? 'positive' : 'negative'}">
                                    \${isPositive ? '↑' : '↓'}
                                </div>
                            </div>\`;
                    }
                }
                document.getElementById('wheat-corn-cards').innerHTML = html;
            }
        }
        
        // DCE月间价差季节图
        function initDCECharts() {
            const container = document.getElementById('dce-spreads-charts');
            const seasonalData = spreadData.dce_spreads_seasonal;
            
            if (!seasonalData || !seasonalData.datasets) {
                console.log('No DCE seasonal data');
                return;
            }
            
            const spreadNames = Object.keys(seasonalData.datasets).filter(k => k !== 'year');
            
            spreadNames.forEach((spreadName, idx) => {
                const chartDiv = document.createElement('div');
                chartDiv.className = 'chart-card half-width';
                chartDiv.innerHTML = \`
                    <div class="chart-header">
                        <h3 class="chart-title">DCE \${spreadName} 季节图</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="dce-chart-\${spreadName}"></canvas>
                    </div>\`;
                container.appendChild(chartDiv);
                
                const values = seasonalData.datasets[spreadName];
                const labels = seasonalData.labels;
                
                const validData = [];
                const validLabels = [];
                labels.forEach((label, i) => {
                    if (values[i] !== null && !isNaN(values[i])) {
                        validLabels.push(label);
                        validData.push(values[i]);
                    }
                });
                
                new Chart(document.getElementById(\`dce-chart-\${spreadName}\`), {
                    type: 'line',
                    data: {
                        labels: validLabels,
                        datasets: [{
                            label: spreadName,
                            data: validData,
                            borderColor: chartColors[idx % chartColors.length],
                            backgroundColor: 'transparent',
                            tension: 0.3,
                            pointRadius: 1,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            x: { 
                                grid: { color: '#30363d' },
                                ticks: { color: '#8b949e', maxTicksLimit: 12 }
                            },
                            y: { 
                                grid: { color: '#30363d' },
                                ticks: { color: '#8b949e' }
                            }
                        }
                    }
                });
            });
        }
        
        // CBOT-DCE价差季节图
        function initCBTDCharts() {
            const container = document.getElementById('cbot-dce-charts');
            const seasonalData = spreadData.cbot_dce_spreads_seasonal;
            
            if (!seasonalData || !seasonalData.datasets) {
                console.log('No CBOT-DCE seasonal data');
                return;
            }
            
            const spreadNames = Object.keys(seasonalData.datasets).filter(k => k !== 'year');
            
            spreadNames.forEach((spreadName, idx) => {
                const chartDiv = document.createElement('div');
                chartDiv.className = 'chart-card half-width';
                chartDiv.innerHTML = \`
                    <div class="chart-header">
                        <h3 class="chart-title">\${spreadName} 季节图</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="cbotdce-chart-\${idx}"></canvas>
                    </div>\`;
                container.appendChild(chartDiv);
                
                const values = seasonalData.datasets[spreadName];
                const labels = seasonalData.labels;
                
                const validData = [];
                const validLabels = [];
                labels.forEach((label, i) => {
                    if (values[i] !== null && !isNaN(values[i])) {
                        validLabels.push(label);
                        validData.push(values[i]);
                    }
                });
                
                new Chart(document.getElementById(\`cbotdce-chart-\${idx}\`), {
                    type: 'line',
                    data: {
                        labels: validLabels,
                        datasets: [{
                            label: spreadName,
                            data: validData,
                            borderColor: chartColors[idx % chartColors.length],
                            backgroundColor: 'transparent',
                            tension: 0.3,
                            pointRadius: 1,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            x: { 
                                grid: { color: '#30363d' },
                                ticks: { color: '#8b949e', maxTicksLimit: 12 }
                            },
                            y: { 
                                grid: { color: '#30363d' },
                                ticks: { color: '#8b949e' }
                            }
                        }
                    }
                });
            });
        }
        
        // 小麦-玉米价差季节图
        function initWheatCharts() {
            const container = document.getElementById('wheat-corn-charts');
            const seasonalData = spreadData.wheat_corn_spreads_seasonal;
            
            if (!seasonalData || !seasonalData.datasets) {
                console.log('No Wheat-Corn seasonal data');
                return;
            }
            
            const spreadNames = Object.keys(seasonalData.datasets).filter(k => k !== 'year');
            
            spreadNames.forEach((spreadName, idx) => {
                const chartDiv = document.createElement('div');
                chartDiv.className = 'chart-card half-width';
                chartDiv.innerHTML = \`
                    <div class="chart-header">
                        <h3 class="chart-title">\${spreadName} 季节图</h3>
                    </div>
                    <div class="chart-container">
                        <canvas id="wheat-chart-\${idx}"></canvas>
                    </div>\`;
                container.appendChild(chartDiv);
                
                const values = seasonalData.datasets[spreadName];
                const labels = seasonalData.labels;
                
                const validData = [];
                const validLabels = [];
                labels.forEach((label, i) => {
                    if (values[i] !== null && !isNaN(values[i])) {
                        validLabels.push(label);
                        validData.push(values[i]);
                    }
                });
                
                new Chart(document.getElementById(\`wheat-chart-\${idx}\`), {
                    type: 'line',
                    data: {
                        labels: validLabels,
                        datasets: [{
                            label: spreadName,
                            data: validData,
                            borderColor: chartColors[idx % chartColors.length],
                            backgroundColor: 'transparent',
                            tension: 0.3,
                            pointRadius: 1,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            x: { 
                                grid: { color: '#30363d' },
                                ticks: { color: '#8b949e', maxTicksLimit: 12 }
                            },
                            y: { 
                                grid: { color: '#30363d' },
                                ticks: { color: '#8b949e' }
                            }
                        }
                    }
                });
            });
        }
        
        // FOB数据
        function initFOB() {
            const fobData = spreadData.fob_basis;
            if (!fobData) return;
            
            const regions = ['brazil', 'us', 'ukraine'];
            regions.forEach(region => {
                const data = fobData[region];
                if (data) {
                    document.getElementById(\`fob-\${region}-price\`).textContent = data.fob_price.toFixed(0);
                    const changeClass = data.change >= 0 ? 'positive' : 'negative';
                    const changeSymbol = data.change >= 0 ? '+' : '';
                    document.getElementById(\`fob-\${region}-change\`).innerHTML = 
                        \`<span class="\${changeClass}">\${changeSymbol}\${data.change.toFixed(2)}</span>\`;
                    document.getElementById('fob-update-date').textContent = data.last_update;
                }
            });
        }
        
        // 页面切换
        function showPage(pageId, evt) {
            document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
            document.getElementById('page-' + pageId).classList.remove('hidden');
            
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            if (evt && evt.target) {
                evt.target.classList.add('active');
            }
        }
        
        // 启动
        init();
    </script>
</body>
</html>
'''

# 替换数据占位符
html_content = html_template.replace('DATA_PLACEHOLDER', data_js)

# 保存文件
output_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'spreads_embedded.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Generated: {output_path}')
