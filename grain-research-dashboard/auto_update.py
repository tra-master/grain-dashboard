"""
自动化更新脚本
流程：
  1. 用 Python 直接复制源数据文件到"筛选后研究数据"（替代 复制.bat，自动覆盖，无任何询问）
  2. 重新生成 spread_data.json（export_data.py）
  3. 将 JSON 内嵌到 spreads.html
  4. 复制 spreads.html → gh-deploy/index.html
  5. git add / commit / push → 更新 GitHub Pages
"""

import subprocess
import sys
import os
import shutil
import re
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'auto_update.log')

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

# ── 路径配置 ──────────────────────────────────────────────
DST_DIR       = r'E:\化学家云盘同步\sscpcnV2\粮化部\筛选后研究数据'
DASHBOARD_DIR = r'C:\Users\56531\WorkBuddy\20260315144604\grain-research-dashboard'
SPREADS_HTML  = os.path.join(DASHBOARD_DIR, 'dashboard', 'spreads.html')
JSON_FILE     = os.path.join(DASHBOARD_DIR, 'dashboard', 'data', 'spread_data.json')
GH_DEPLOY_DIR = r'C:\Users\56531\WorkBuddy\gh-deploy'
GH_INDEX_HTML = os.path.join(GH_DEPLOY_DIR, 'index.html')

# 需要复制的源文件列表（与 复制.bat 完全一致）
COPY_FILES = [
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\部分宏观进口和饲料替代的年度月度数据-周报(冲突文件-李洋洋).xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\Part1-玉米02-利润与库存-lyy周报.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\usda销售进度和装船量-周报.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\美国乙醇数据-周报.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\恢复-历史-基差月差套-lyy周报 - 副本.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\Part6-生猪03-生猪现货养殖利润-lyy周报xin.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\钢联数据淀粉周度数据-周报.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\东北深加工收购量.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\美国巴西玉米\frieght dVT-Dl.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\美国巴西玉米\高粱大麦.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\美国巴西玉米\路透高粱usda数据更新-1.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\周报数据\美国巴西玉米\路透玉米usda数据更新-1.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\CBOT和usda数据\CBOT新.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\小麦数据\钢联普麦-dce价差.xlsx',
    r'E:\化学家云盘同步\sscpcnV2\粮化部\玉米研究\需求数据\钢联数据_玉米：深加工企业：早间剩余车辆：山东（日）_2025-1-9_1736404789117.xlsx',
]
# ──────────────────────────────────────────────────────────


def step1_copy_files():
    """直接用 Python 复制所有源文件到目标目录，自动覆盖，无任何交互"""
    log('=== Step 1: 复制源数据文件 ===')
    os.makedirs(DST_DIR, exist_ok=True)
    ok, skip, fail = 0, 0, 0
    for src in COPY_FILES:
        fname = os.path.basename(src)
        dst = os.path.join(DST_DIR, fname)
        if not os.path.exists(src):
            log(f'  [SKIP] 源文件不存在: {fname}')
            skip += 1
            continue
        try:
            shutil.copy2(src, dst)   # copy2 保留时间戳，自动覆盖，无任何询问
            log(f'  [OK]   {fname}')
            ok += 1
        except Exception as e:
            log(f'  [FAIL] {fname}: {e}')
            fail += 1
    log(f'  复制完成: 成功={ok}, 跳过={skip}, 失败={fail}')
    if fail > 0:
        log('  WARNING: 有文件复制失败，但继续后续步骤')


def step2_export_json():
    """重新生成 spread_data.json"""
    log('=== Step 2: 重新生成 JSON 数据 ===')
    result = subprocess.run(
        [sys.executable, 'src/export_data.py'],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        cwd=DASHBOARD_DIR
    )
    log(f'  stdout: {result.stdout.strip()[-500:]}')
    if result.returncode != 0:
        log(f'  stderr: {result.stderr.strip()[-500:]}')
        raise RuntimeError('export_data.py 执行失败')
    if not os.path.exists(JSON_FILE):
        raise RuntimeError(f'JSON 文件未生成: {JSON_FILE}')
    log(f'  JSON 已生成: {os.path.getsize(JSON_FILE) // 1024} KB')


def step3_embed_json():
    """将 spread_data.json 内嵌到 spreads.html 的 EMBEDDED_DATA 变量"""
    log('=== Step 3: 内嵌 JSON 到 HTML ===')
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        json_str = f.read()

    with open(SPREADS_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # 替换 const EMBEDDED_DATA = {...};
    pattern = r'const EMBEDDED_DATA\s*=\s*\{[\s\S]*?\}(?=\s*;)'
    new_data = f'const EMBEDDED_DATA = {json_str}'
    new_html, count = re.subn(pattern, new_data, html, count=1)

    if count == 0:
        raise RuntimeError('未找到 EMBEDDED_DATA 替换位置，HTML 结构可能已变化')

    with open(SPREADS_HTML, 'w', encoding='utf-8') as f:
        f.write(new_html)
    log(f'  HTML 已更新，大小: {len(new_html) // 1024} KB')


def step4_copy_to_deploy():
    """复制 spreads.html → gh-deploy/index.html"""
    log('=== Step 4: 复制到部署目录 ===')
    os.makedirs(GH_DEPLOY_DIR, exist_ok=True)
    shutil.copy2(SPREADS_HTML, GH_INDEX_HTML)
    log(f'  已复制: {os.path.getsize(GH_INDEX_HTML) // 1024} KB')


def step5_git_push():
    """git add / commit / push"""
    log('=== Step 5: 推送到 GitHub Pages ===')
    today = datetime.now().strftime('%Y-%m-%d %H:%M')

    def git(args):
        r = subprocess.run(
            ['git'] + args,
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            cwd=GH_DEPLOY_DIR
        )
        out = (r.stdout + r.stderr).strip()
        if out:
            log(f'  git {args[0]}: {out[:300]}')
        return r

    git(['add', 'index.html'])
    r = git(['commit', '-m', f'auto update {today}'])
    if 'nothing to commit' in (r.stdout + r.stderr):
        log('  数据无变化，无需推送')
        return
    r = git(['push', 'origin', 'main'])
    if r.returncode != 0:
        raise RuntimeError(f'git push 失败: {r.stderr}')
    log('  推送成功！https://tra-master.github.io/grain-dashboard/')


def main():
    log('======== 自动更新开始 ========')
    try:
        step1_copy_files()
        step2_export_json()
        step3_embed_json()
        step4_copy_to_deploy()
        step5_git_push()
        log('======== 自动更新完成 ========')
    except Exception as e:
        log(f'[ERROR] 更新失败: {e}')
        import traceback
        log(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
