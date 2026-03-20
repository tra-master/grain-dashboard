html_path = 'c:/Users/56531/WorkBuddy/20260315144604/grain-research-dashboard/dashboard/spreads.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '        // ===== 通用图表颜色 ====='
end_marker = '        // 初始化由 DOMContentLoaded 触发'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

# 新的图表JS代码
new_chart_js = r"""        // ===== 图表颜色（每年一条线） =====
        const YEAR_COLORS = [
            '#58a6ff','#3fb950','#f85149','#d29922','#a371f7',
            '#79c0ff','#ffa657','#ff7b72','#56d364','#e3b341',
            '#bc8cff','#39d353','#ff6e96','#40c8c8','#ffd700',
            '#ff9500','#a0c4ff','#b5ead7'
        ];

        // ===== 通用：渲染多年季节图 =====
        function renderSeasonalCharts(containerId, seasonalData, titlePrefix) {
            var container = document.getElementById(containerId);
            if (!container || !seasonalData || !seasonalData.datasets) return;

            container.innerHTML = '';

            var spreadNames = Object.keys(seasonalData.datasets);
            var labels = seasonalData.labels; // MM-DD 数组，01-01 ~ 12-31

            spreadNames.forEach(function(spreadName, idx) {
                var yearDataMap = seasonalData.datasets[spreadName]; // { "2009": [...], "2010": [...], ... }
                var years = Object.keys(yearDataMap).sort();

                var safeId = containerId + '-chart-' + idx;
                var chartDiv = document.createElement('div');
                chartDiv.className = 'chart-card half-width';
                chartDiv.innerHTML =
                    '<div class="chart-header">' +
                    '  <h3 class="chart-title">' + titlePrefix + spreadName + ' 季节图</h3>' +
                    '  <div style="font-size:11px;color:var(--text-secondary);margin-top:2px">X轴: 月-日（01-01 ~ 12-31），每条线代表一年</div>' +
                    '</div>' +
                    '<div class="chart-container" style="height:320px">' +
                    '  <canvas id="' + safeId + '"></canvas>' +
                    '</div>';
                container.appendChild(chartDiv);

                // 构建每年的 dataset
                var datasets = years.map(function(yr, i) {
                    var values = yearDataMap[yr];
                    var isCurrent = (yr === String(new Date().getFullYear()));
                    return {
                        label: yr,
                        data: values,
                        borderColor: YEAR_COLORS[i % YEAR_COLORS.length],
                        backgroundColor: 'transparent',
                        tension: 0.3,
                        pointRadius: 0,
                        borderWidth: isCurrent ? 2.5 : 1.2,
                        borderDash: isCurrent ? [] : [],
                        spanGaps: false
                    };
                });

                new Chart(document.getElementById(safeId), {
                    type: 'line',
                    data: { labels: labels, datasets: datasets },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: { mode: 'index', intersect: false },
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                                labels: {
                                    color: '#8b949e',
                                    boxWidth: 20,
                                    padding: 8,
                                    font: { size: 11 }
                                }
                            },
                            tooltip: {
                                backgroundColor: '#21262d',
                                borderColor: '#30363d',
                                borderWidth: 1,
                                titleColor: '#8b949e',
                                bodyColor: '#f0f6fc',
                                callbacks: {
                                    title: function(items) { return '日期: ' + items[0].label; }
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: { color: '#30363d' },
                                ticks: {
                                    color: '#8b949e',
                                    maxTicksLimit: 12,
                                    callback: function(val, idx, ticks) {
                                        // 只显示月份标签（01-01, 02-01 ...）
                                        var label = labels[val];
                                        if (label && label.endsWith('-01')) {
                                            return label.substring(0, 2) + '月';
                                        }
                                        return '';
                                    }
                                }
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

        // ===== 更新总览卡片 =====
        function updateOverviewCards() {
            var dceCards = document.getElementById('dce-spread-cards');
            var dceLatest = spreadData.latest_dce_spreads;
            if (dceLatest && dceCards) {
                dceCards.innerHTML = '';
                Object.entries(dceLatest).forEach(function([key, val]) {
                    if (val !== null && !isNaN(val)) {
                        var isPos = val >= 0;
                        dceCards.innerHTML +=
                            '<div class="stat-card">' +
                            '  <div class="stat-label">DCE ' + key + '</div>' +
                            '  <div class="stat-value" style="color:' + (isPos ? 'var(--accent-green)' : 'var(--accent-red)') + '">' + val.toFixed(0) + '</div>' +
                            '  <div class="stat-change ' + (isPos ? 'positive' : 'negative') + '">' + (isPos ? '↑ 正基差' : '↓ 负基差') + '</div>' +
                            '</div>';
                    }
                });
            }

            var cbotCards = document.getElementById('cbot-dce-cards');
            var cbotLatest = spreadData.latest_cbot_dce_spreads;
            if (cbotLatest && cbotCards) {
                cbotCards.innerHTML = '';
                Object.entries(cbotLatest).forEach(function([key, val]) {
                    if (val !== null && !isNaN(val)) {
                        var isPos = val >= 0;
                        cbotCards.innerHTML +=
                            '<div class="stat-card">' +
                            '  <div class="stat-label">' + key + '</div>' +
                            '  <div class="stat-value" style="color:' + (isPos ? 'var(--accent-green)' : 'var(--accent-red)') + '">' + val.toFixed(0) + '</div>' +
                            '  <div class="stat-change ' + (isPos ? 'positive' : 'negative') + '">' + (isPos ? '溢价' : '折价') + '</div>' +
                            '</div>';
                    }
                });
            }

            var wheatCards = document.getElementById('wheat-corn-cards');
            var wheatLatest = spreadData.latest_wheat_corn_spreads;
            if (wheatLatest && wheatCards) {
                wheatCards.innerHTML = '';
                Object.entries(wheatLatest).forEach(function([key, val]) {
                    if (val !== null && !isNaN(val)) {
                        var isPos = val >= 0;
                        wheatCards.innerHTML +=
                            '<div class="stat-card">' +
                            '  <div class="stat-label">' + key + '</div>' +
                            '  <div class="stat-value" style="color:' + (isPos ? 'var(--accent-green)' : 'var(--accent-red)') + '">' + val.toFixed(0) + '</div>' +
                            '  <div class="stat-change ' + (isPos ? 'positive' : 'negative') + '">' + (isPos ? '↑ 小麦溢价' : '↓ 玉米溢价') + '</div>' +
                            '</div>';
                    }
                });
            }

            var fobCards = document.getElementById('fob-cards');
            var fobData = spreadData.fob_basis;
            if (fobData && fobCards) {
                fobCards.innerHTML = '';
                Object.entries(fobData).forEach(function([region, data]) {
                    if (data && data.fob_price !== undefined) {
                        var isPos = data.change >= 0;
                        fobCards.innerHTML +=
                            '<div class="fob-card">' +
                            '  <div class="fob-name">' + data.name + '</div>' +
                            '  <div class="fob-price">' + data.fob_price.toFixed(0) + ' <small style="font-size:14px;color:var(--text-secondary)">USD/mt</small></div>' +
                            '  <div class="fob-change ' + (isPos ? 'positive' : 'negative') + '">' + (isPos ? '+' : '') + data.change.toFixed(2) + '</div>' +
                            '</div>';
                    }
                });
            }
        }

        function initDCECharts() {
            renderSeasonalCharts('dce-spreads-charts', spreadData.dce_spreads_seasonal, 'DCE ');
        }
        function initCBTDCharts() {
            renderSeasonalCharts('cbot-dce-charts', spreadData.cbot_dce_spreads_seasonal, '');
        }
        function initWheatCharts() {
            renderSeasonalCharts('wheat-corn-charts', spreadData.wheat_corn_spreads_seasonal, '');
        }

        function initFOB() {
            var fobData = spreadData.fob_basis;
            if (!fobData) return;
            ['brazil', 'us', 'ukraine'].forEach(function(region) {
                var data = fobData[region];
                if (!data) return;
                var priceEl = document.getElementById('fob-' + region + '-price');
                var changeEl = document.getElementById('fob-' + region + '-change');
                var dateEl   = document.getElementById('fob-update-date');
                if (priceEl) priceEl.textContent = data.fob_price.toFixed(0);
                if (changeEl) {
                    var isPos = data.change >= 0;
                    changeEl.innerHTML = '<span class="' + (isPos ? 'positive' : 'negative') + '">' + (isPos ? '+' : '') + data.change.toFixed(2) + '</span>';
                }
                if (dateEl) dateEl.textContent = data.last_update;
            });
        }

"""

old_block = html[start_idx:end_idx]
html = html[:start_idx] + new_chart_js + html[end_idx:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('JS图表函数替换完成，文件大小:', len(html)//1024, 'KB')
