"""
谷物期现交易研究看板 - 主入口
整合数据读取、处理和看板生成
"""
import os
import sys
import json
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_all_data
from data_loader_new import load_all_spread_data
from data_processor import process_all_data
from dashboard_generator import generate_html_header, save_dashboard
from export_data import export_to_json
import importlib.util

def main():
    """主函数"""
    print("=" * 50)
    print("谷物期现交易研究看板")
    print("=" * 50)
    
    # 1. 加载数据（旧版）
    print("\n[1/5] 加载数据源...")
    raw_data = load_all_data()
    print(f"成功加载 {len(raw_data)} 个数据文件")
    
    # 2. 处理数据
    print("\n[2/5] 处理数据...")
    processed_data = process_all_data(raw_data)
    print(f"处理完成 {len(processed_data)} 个数据模块")
    
    # 3. 导出新版价差数据
    print("\n[3/5] 导出价差数据...")
    export_to_json()
    
    # 4. 生成嵌入数据的看板
    print("\n[4/5] 生成嵌入式看板...")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gen_script = os.path.join(project_root, 'generate_dashboard.py')
    spec = importlib.util.spec_from_file_location("generate_dashboard", gen_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # 5. 生成旧版看板
    print("\n[5/5] 生成看板...")
    
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, 'dashboard', 'index.html')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 生成HTML
    html_content = generate_html_header()
    save_dashboard(html_content, output_path)
    
    print("\n" + "=" * 50)
    print(f"看板生成完成！")
    print(f"输出路径: {output_path}")
    print(f"价差看板: {os.path.join(project_root, 'dashboard', 'spreads.html')}")
    print("=" * 50)
    
    return output_path


if __name__ == "__main__":
    main()
