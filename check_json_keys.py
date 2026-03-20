html_path = 'c:/Users/56531/WorkBuddy/20260315144604/grain-research-dashboard/dashboard/spreads.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 找到图表函数区块的起止标记
start_marker = '        // ===== 通用图表颜色 ====='
end_marker = '        // 初始化由 DOMContentLoaded 触发'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

print(f'start_idx: {start_idx}')
print(f'end_idx: {end_idx}')
if start_idx >= 0 and end_idx >= 0:
    print('找到区块，长度:', end_idx - start_idx)
    print('区块开头:', html[start_idx:start_idx+100])
    print('区块结尾:', html[end_idx-100:end_idx+50])
