# 定时任务设置脚本
# 运行此脚本创建每日自动更新任务

import os
import subprocess

# 任务配置
TASK_NAME = "谷物期现交易看板更新"
SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_dashboard.bat")
SCHEDULE_TIME = "07:00"  # 每天早上7点更新

def create_scheduled_task():
    """创建Windows定时任务"""
    # 创建任务命令
    cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "{SCRIPT_PATH}" /sc daily /st {SCHEDULE_TIME} /f'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ 定时任务创建成功!")
            print(f"  任务名称: {TASK_NAME}")
            print(f"  执行时间: 每天 {SCHEDULE_TIME}")
            print(f"  执行脚本: {SCRIPT_PATH}")
        else:
            print(f"✗ 创建失败: {result.stderr}")
    except Exception as e:
        print(f"✗ 错误: {e}")

def delete_scheduled_task():
    """删除定时任务"""
    cmd = f'schtasks /delete /tn "{TASK_NAME}" /f'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ 定时任务已删除")
        else:
            print(f"删除失败: {result.stderr}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        delete_scheduled_task()
    else:
        print("=" * 50)
        print("谷物期现交易看板 - 定时任务设置")
        print("=" * 50)
        print(f"\n任务配置:")
        print(f"  名称: {TASK_NAME}")
        print(f"  时间: 每天 {SCHEDULE_TIME}")
        print(f"  脚本: {SCRIPT_PATH}")
        print("\n正在创建定时任务...")
        create_scheduled_task()
        print("\n提示: 运行 'python setup_task.py delete' 可删除任务")
