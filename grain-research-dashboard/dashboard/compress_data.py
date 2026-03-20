#!/usr/bin/env python3
"""
压缩 spreads.html 中的 EMBEDDED_DATA 数据
将年份数组中的 null 值移除，只保留有效数据点和其索引
"""

import re
import json
import sys

def compress_seasonal_data(data):
    """压缩季节性数据，移除 null 值"""
    if not isinstance(data, dict):
        return data
    
    result = {}
    
    # 检查是否是季节性格式的数据（有 labels 和 datasets）
    if 'labels' in data and 'datasets' in data:
        labels = data['labels']
        datasets = data['datasets']
        
        result['labels'] = labels
        result['datasets'] = {}
        
        for spread_name, year_data in datasets.items():
            result['datasets'][spread_name] = {}
            
            for year, values in year_data.items():
                if isinstance(values, list):
                    # 提取非null值及其索引
                    compressed = [[i, v] for i, v in enumerate(values) if v is not None]
                    result['datasets'][spread_name][year] = compressed
                else:
                    result['datasets'][spread_name][year] = values
        
        return result
    
    # 递归处理其他字段
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = compress_seasonal_data(value)
        else:
            result[key] = value
    
    return result

def extract_and_compress_html(input_file, output_file):
    """提取HTML中的EMBEDDED_DATA，压缩后放回"""
    
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 EMBEDDED_DATA 的开始和结束
    # 格式: const EMBEDDED_DATA = { ... };
    pattern = r'(const EMBEDDED_DATA = )(\{[\s\S]*?\n\});'
    match = re.search(pattern, content)
    
    if not match:
        print("错误: 未找到 EMBEDDED_DATA")
        return False
    
    prefix = match.group(1)  # "const EMBEDDED_DATA = "
    json_str = match.group(2)  # JSON数据
    
    print(f"原始JSON长度: {len(json_str)} 字符")
    
    # 解析JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return False
    
    # 压缩数据
    print("正在压缩数据...")
    compressed_data = compress_seasonal_data(data)
    
    # 重新序列化为JSON
    compressed_json = json.dumps(compressed_data, ensure_ascii=False, separators=(',', ':'))
    print(f"压缩后JSON长度: {len(compressed_json)} 字符")
    print(f"压缩率: {100 - 100*len(compressed_json)/len(json_str):.1f}%")
    
    # 替换内容
    new_content = content[:match.start()] + prefix + compressed_json + content[match.end():]
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已保存到: {output_file}")
    return True

if __name__ == '__main__':
    # 使用绝对路径
    input_file = r'C:\Users\administer\WorkBuddy\20260315144604\grain-research-dashboard\dashboard\spreads.html'
    output_file = r'C:\Users\administer\WorkBuddy\20260315144604\grain-research-dashboard\dashboard\spreads_compressed.html'
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    success = extract_and_compress_html(input_file, output_file)
    sys.exit(0 if success else 1)
